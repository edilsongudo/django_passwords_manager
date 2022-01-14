from django.shortcuts import render, redirect
from django.http import FileResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .forms import *
from .models import *
from .utils import *
from cryptography.fernet import InvalidToken
import json
import secrets


# @login_required
def home(request):
    print(request.user.is_authenticated)

    if not request.user.is_authenticated:
        return render(request, 'passmanager/landing_page.html')


    if not request.user.masterpassword.has_defined_a_master_password:
        return redirect('new_master')

    if request.is_ajax():
        masterpassword = request.POST['masterpassword']

        key = generate_key(
            masterpassword,
            request.user.masterpassword.salt
            )

        response = []
        entries = Entry.objects.filter(author=request.user)

        for entry in entries:
            try:
                entry_email = decrypt(
                    encrypted=entry.site_email_used.encode(),
                    key=key.encode())

                entry_password = decrypt(
                    encrypted=entry.site_password_used.encode(),
                    key=key.encode())

                if not entry.is_generated_for_initial_master_pw_check:
                    response.append({
                        'id': entry.pk,
                        'site': entry.site_name,
                        'email': entry_email,
                        'encrypted_password': entry.site_password_used,
                        'decrypted_password': entry_password,
                    })
            except InvalidToken:
                return JsonResponse({'response': response, 'is_masterpass_correct': "false"})

        return JsonResponse({'response': response, 'is_masterpass_correct': "true"})

    return render(request, 'passmanager/index.html')



@login_required
def new(request):
    if request.is_ajax():

        form = EntryForm(request.POST)
        if form.is_valid():
            site_name = form.cleaned_data['entrysite']
            email_used = form.cleaned_data['entryemail']
            password = form.cleaned_data['entrypassword']
            masterpassword = form.cleaned_data['masterpassword']

            key = generate_key(
                masterpassword,
                request.user.masterpassword.salt
                )
            encrypted_email = encrypt(message=email_used, key=key)
            encrypted_password = encrypt(message=password, key=key)

            Entry.objects.create(
                author=request.user,
                site_name=site_name,
                site_email_used=encrypted_email,
                site_password_used=encrypted_password
            )

            response = {
                'status': 'ok',
                'author_username': request.user.username,
                'site': site_name,
                'email_used': email_used,
                'encrypted_password': encrypted_password
            }

            return JsonResponse(response)
        else:
            return JsonResponse({'status': 'fail', 'errors': form.errors})


@login_required
def new_master(request):

    if request.user.masterpassword.has_defined_a_master_password:
        raise PermissionDenied()

    if request.method == 'POST':
        form = MasterCreateForm(request.POST, user=request.user)

        if form.is_valid():

            master = form.cleaned_data['master']
            master_confirm = form.cleaned_data['master_confirm']

            if master != master_confirm:
                messages.error(request, 'Fields New master and New master confirm do not match')
                return render(request, 'passmanager/new_master.html', {'form': form})

            master_key = generate_key(
                master,
                request.user.masterpassword.salt
                )
            print(master)
            site_name = secrets.token_urlsafe()
            email_used = encrypt(message=secrets.token_urlsafe(), key=master_key)
            encrypted_password = encrypt(message=secrets.token_urlsafe(), key=master_key)

            entries = Entry.objects.create(
                author=request.user,
                site_name=site_name,
                site_email_used=email_used,
                site_password_used=encrypted_password,
                is_generated_for_initial_master_pw_check=True,
                )

            request.user.masterpassword.has_defined_a_master_password = True
            request.user.masterpassword.save()

            return redirect('home')

        else:
            return render(request, 'passmanager/new_master.html', {'form': form})


    form = MasterCreateForm()
    return render(request, 'passmanager/new_master.html', {'form': form})


@login_required
def master(request):
    if not request.user.masterpassword.has_defined_a_master_password:
        raise PermissionDenied()

    form = MasterPasswordForm()

    if request.method == 'POST':
        form = MasterPasswordForm(request.POST, user=request.user)

        if form.is_valid():

            key = form.cleaned_data['master']
            key_confirm = form.cleaned_data['master_confirm']

            if key != key_confirm:
                messages.error(request, 'Fields New master and New master confirm do not match')
                return render(request, 'passmanager/new_master.html', {'form': form})

            last_master = form.cleaned_data['last_master']
            print(last_master)
            last_key = generate_key(
                last_master,
                request.user.masterpassword.salt
                )
            new_key = generate_key(
                key,
                request.user.masterpassword.salt
                )

            entries = Entry.objects.filter(author=request.user)

            try:
                for entry in entries:

                    site_email_used = decrypt(
                        encrypted=entry.site_email_used.encode(),
                        key=last_key.encode()
                        )
                    entry.site_email_used = encrypt(
                        message=site_email_used,
                        key=new_key.encode()
                        )

                    site_password_used = decrypt(
                        encrypted=entry.site_password_used.encode(),
                        key=last_key.encode()
                        )
                    entry.site_password_used = encrypt(
                        message=site_password_used,
                        key=new_key.encode()
                        )
                    entry.save()

                messages.success(
                    request, f'Your Master Password was successfully edited.')
                return redirect('home')
            except InvalidToken:
                messages.error(request, 'The last master password you typed is wrong')
                return render(request, 'passmanager/master.html', {'form': form})

        else:
            return render(request, 'passmanager/master.html', {'form': form})


    return render(request, 'passmanager/master.html', {'form': form})


@login_required
def delete(request):
    if request.method == 'POST':
        pk = request.POST['id']
        entry = Entry.objects.get(pk=pk)
        if entry.author == request.user:
            entry.delete()
            print(f'Entry with id {pk} deleted')
            return JsonResponse({'response': "ok"})
    return JsonResponse({'response': "fail"})


def generate_password(request):
    password = generate_secure_password()
    return JsonResponse({'password': password})


def error_404_view(request, *args, **argv):
    response = render(request, 'passmanager/404.html')
    response.status_code = 404
    return response

def error_403_view(request, *args, **argv):
    response = render(request, 'passmanager/403.html')
    response.status_code = 403
    return response

def error_500_view(request, *args, **argv):
    response = render(request, 'passmanager/500.html')
    response.status_code = 500
    return response
