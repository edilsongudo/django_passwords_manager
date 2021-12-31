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

    # TODO PROHIBIT THIS VIEW AFTER A USED AS ALREADY CREATED ONE MASTER PASSWORD

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

        return redirect('home')

    form = MasterCreateForm()
    return render(request, 'passmanager/new_master.html', {'form': form})


@login_required
def master(request):
    if request.method == 'POST':
        form = MasterPasswordForm(
            request.POST, instance=request.user.masterpassword)

        if form.is_valid():

            key = form.cleaned_data['master']
            key2 = form.cleaned_data['master_confirm']
            last_master = form.cleaned_data['last_master']
            last_master2 = generate_key(last_master)
            crypt = hashlib.sha256()
            crypt.update(last_master2.encode())
            last_master2 = crypt.hexdigest()

            if MasterPassword.objects.get(author=request.user).master != '':

                print('last master: ',last_master2[0:3])
                print('request.user.masterpassword.master: ', MasterPassword.objects.get(author=request.user).master)

                if last_master2[0:3] != MasterPassword.objects.get(author=request.user).master:
                    messages.warning(request, 'The last master password you typed is wrong. Let it blank if it the first time creating one.')
                    return render(request, 'passmanager/master.html', {'form': form})


            if key != key2:
                messages.warning(request, 'Fields Master Password and master password confirm do not match')
                return render(request, 'passmanager/master.html', {'form': form})

            key = generate_key(key)
            last_master = generate_key(last_master)

            obj = form.save(commit=False)
            password = form.cleaned_data['master']
            password = generate_key(password)


            entries = Entry.objects.filter(author=request.user)

            for entry in entries:
                entry.site_password_used = decrypt(encrypted=entry.site_password_used.encode() ,key=last_master.encode())
                print(entry.site_password_used)
                entry.site_password_used = encrypt(message=entry.site_password_used, key=key.encode())
                print(entry.site_password_used)
                entry.save()

            crypt = hashlib.sha256()
            crypt.update(password.encode())
            password = crypt.hexdigest()
            obj.master = password[0:3]
            obj.save()

            messages.success(
                request, f'Your Master Password was successfully edited.')
            return redirect('home')
        else:
            return render(request, 'passmanager/master.html', {'form': form})

    form = MasterPasswordForm()
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
