from django.shortcuts import render, redirect
from django.http import FileResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from .utils import *
from .utilsExtra import *
from cryptography.fernet import InvalidToken
import hashlib
import json
import secrets


@login_required
def home(request):

    if request.user.masterpassword.master == '':
        return redirect('new_master')

    if request.is_ajax():

        request_json = json.loads(request.body.decode('utf-8'))
        masterpassword = request_json['masterpassword']
        # is_masterpass_correct = check_if_master_password_is_correct(request, masterpassword)
        key = generate_key(masterpassword)

        response = []
        entries = Entry.objects.filter(author=request.user)

        for entry in entries:
            try:
                entry_password = decrypt(
                    encrypted=entry.site_password_used.encode(),
                    key=key.encode())

                if not entry.is_generated_for_initial_master_pw_check:
                    response.append({
                        'site': entry.site_name,
                        'email': entry.site_email_used,
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
        request_json = json.loads(request.body.decode('utf-8'))

        site_name = request_json['entrysite']
        email_used = request_json['entryemail']
        password = request_json['entrypassword']
        masterpassword = request_json['masterpassword']

        key = generate_key(masterpassword)
        encrypted_password = encrypt(message=password, key=key)

        Entry.objects.create(
            author=request.user,
            site_name=site_name,
            site_email_used=email_used,
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


@login_required
def new_master(request):

    if request.user.masterpassword.master != "":
        raise PermissionDenied()

    if request.method == 'POST':
        form = MasterCreateForm(
            request.POST,
            instance=request.user.masterpassword)

        master = request.POST['master']
        master_confirm = request.POST['master_confirm']

        if master != master_confirm:
            messages.warning(request, 'Fields Master Password and master password confirm do not match')
            return render(request, 'passmanager/master.html', {'form': form})

        obj = form.save(commit=False)
        master_key = generate_key(master)
        password = hash_and_return_first_3_chars(master_key)
        obj.master = password
        obj.save()

        site_name = secrets.token_urlsafe()
        email_used = secrets.token_urlsafe()
        encrypted_password = encrypt(message=secrets.token_urlsafe(), key=master_key)

        entries = Entry.objects.create(
            author=request.user,
            site_name=site_name,
            site_email_used=email_used,
            site_password_used=encrypted_password,
            is_generated_for_initial_master_pw_check=True,
            )

        return redirect('home')

    form = MasterCreateForm()
    return render(request, 'passmanager/new_master.html', {'form': form})


@login_required
def master(request):
    form = MasterPasswordForm()

    if request.method == 'POST':
        form = MasterPasswordForm(
            request.POST, instance=request.user.masterpassword)

        if form.is_valid():

            key = form.cleaned_data['master']
            key_confirm = form.cleaned_data['master_confirm']

            if key != key_confirm:
                messages.warning(request, 'Fields "Master Password" and Master Password Confirm" must be equal')
                return render(request, 'passmanager/master.html', {'form': form})

            last_master = form.cleaned_data['last_master']
            last_key = generate_key(last_master)
            new_key = generate_key(key)

            entries = Entry.objects.filter(author=request.user)

            try:
                for entry in entries:
                    entry.site_password_used = decrypt(
                        encrypted=entry.site_password_used.encode(),
                        key=last_key.encode()
                        )
                    entry.site_password_used = encrypt(
                        message=entry.site_password_used,
                        key=new_key.encode()
                        )
                    entry.save()
                    messages.success(
                        request, f'Your Master Password was successfully edited.')
                    return redirect('home')
            except InvalidToken:
                messages.warning(request, 'The last master password you typed is wrong')
                return render(request, 'passmanager/master.html', {'form': form})

    return render(request, 'passmanager/master.html', {'form': form})



# def delete(request, pk):
#     entry = Entry.objects.get(pk=pk)
#     if request.method == 'POST':
#         entry.delete()
#         print('Deleted')
#         return redirect('mypasswords')
#     return render(request, 'passmanager/delete.html', {'entry': entry})

# def edit(request, pk):
#     entry = Entry.objects.get(pk=pk)
#     form = EntryForm(instance=entry)
#     if request.method == 'POST':
#         form = EntryForm(request.POST, instance=entry)
#         pass
#         # entry.site_name =
#         # entry.site_email_used =
#         # entry.site_password_used =
#         # entry.save()
#         return redirect('mypasswords')
#     return render(request, 'passmanager/edit.html', {'form': form})




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
