import json

from cryptography.fernet import InvalidToken
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from passmanager.forms import *
from passmanager.models import *
from passmanager.utils import *

from .serializers import *


@api_view(['POST'])
def getEntries(request):
    data = request.data
    masterpassword = data['masterpassword']
    key = generate_key(masterpassword, request.user.masterpassword.salt)

    response = []
    entries = Entry.objects.filter(author=request.user)
    for entry in entries:
        try:
            entry_email = decrypt(
                encrypted=entry.site_email_used.encode(), key=key.encode()
            )

            entry_password = decrypt(
                encrypted=entry.site_password_used.encode(),
                key=key.encode(),
            )

            if not entry.is_generated_for_initial_master_pw_check:
                response.append(
                    {
                        'id': entry.pk,
                        'site': entry.site_name,
                        'email': entry_email,
                        'encrypted_password': entry.site_password_used,
                        'decrypted_password': entry_password,
                    }
                )
        except InvalidToken:
            return Response(
                {'response': response, 'is_masterpass_correct': False}
            )
    return Response({'response': response, 'is_masterpass_correct': True})


@api_view(['POST'])
def newEntry(request):
    data = request.data
    form = EntryForm(data)
    if form.is_valid():
        site_name = form.cleaned_data['entrysite']
        email_used = form.cleaned_data['entryemail']
        password = form.cleaned_data['entrypassword']
        masterpassword = form.cleaned_data['masterpassword']

        key = generate_key(masterpassword, request.user.masterpassword.salt)
        encrypted_email = encrypt(message=email_used, key=key)
        encrypted_password = encrypt(message=password, key=key)

        Entry.objects.create(
            author=request.user,
            site_name=site_name,
            site_email_used=encrypted_email,
            site_password_used=encrypted_password,
        )

        response = {
            'status': 'ok',
            'author_username': request.user.username,
            'site': site_name,
            'email_used': email_used,
            'encrypted_password': encrypted_password,
        }

        return Response(response, status=status.HTTP_201_CREATED)
    return Response(
        {'status': 'fail', 'errors': form.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


@api_view(['POST'])
def deleteEntry(request):
    data = request.data
    pk = data['id']
    entry = Entry.objects.get(pk=pk)
    if entry.author == request.user:
        entry.delete()
        return Response({'response': 'ok'})
    return Response({'response': 'fail'})


@api_view(['GET'])
def hasDefinedMasterPassword(request):
    return Response(
        {
            'has_user_defined_a_master_password': request.user.masterpassword.has_defined_a_master_password
        }
    )


@api_view(['POST'])
def newMaster(request):

    if request.user.masterpassword.has_defined_a_master_password:
        return Response(
            {'message': 'User already defined a master password'},
            status=status.HTTP_403_FORBIDDEN,
        )

    data = request.data
    form = MasterCreateForm(data, user=request.user)

    if form.is_valid():
        master = form.cleaned_data['master']
        master_confirm = form.cleaned_data['master_confirm']

        master_key = generate_key(master, request.user.masterpassword.salt)
        site_name = secrets.token_urlsafe()
        email_used = encrypt(message=secrets.token_urlsafe(), key=master_key)
        encrypted_password = encrypt(
            message=secrets.token_urlsafe(), key=master_key
        )

        entries = Entry.objects.create(
            author=request.user,
            site_name=site_name,
            site_email_used=email_used,
            site_password_used=encrypted_password,
            is_generated_for_initial_master_pw_check=True,
        )

        request.user.masterpassword.has_defined_a_master_password = True
        request.user.masterpassword.save()

        return Response({'message': 'created'}, status=status.HTTP_201_CREATED)

    return Response({'message': 'fail'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def editMaster(request):
    if not request.user.masterpassword.has_defined_a_master_password:
        return Response(
            {'message': 'You need to create a master password first'},
            status=status.HTTP_403_FORBIDDEN,
        )

    data = request.data
    form = MasterPasswordForm(data, user=request.user)

    if form.is_valid():

        key = form.cleaned_data['master']
        key_confirm = form.cleaned_data['master_confirm']

        if key != key_confirm:
            return Response(
                {
                    'message': 'Fields New master and New master confirm do not match'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        last_master = form.cleaned_data['last_master']
        last_key = generate_key(last_master, request.user.masterpassword.salt)
        new_key = generate_key(key, request.user.masterpassword.salt)

        entries = Entry.objects.filter(author=request.user)

        try:
            for entry in entries:

                site_email_used = decrypt(
                    encrypted=entry.site_email_used.encode(),
                    key=last_key.encode(),
                )
                entry.site_email_used = encrypt(
                    message=site_email_used, key=new_key.encode()
                )

                site_password_used = decrypt(
                    encrypted=entry.site_password_used.encode(),
                    key=last_key.encode(),
                )
                entry.site_password_used = encrypt(
                    message=site_password_used, key=new_key.encode()
                )
                entry.save()

            return Response(
                {'message': 'Your Master Password was successfully edited.'}
            )

        except InvalidToken:
            return Response(
                {'message': 'The last master password you typed is wrong'},
                status=status.HTTP_400_BAD_REQUEST,
            )

    return Response({'message': 'fail'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def generate_password(request):
    password = generate_secure_password()
    return Response({'password': password})


@api_view(['POST', 'GET'])
def user_email_change(request):
    if request.method == 'GET':
        return Response({'email': request.user.email})
    user = request.user
    User = get_user_model()
    if (
        User.objects.exclude(pk=user.pk)
        .filter(email=request.data['email'])
        .exists()
    ):
        return Response(
            {'message': 'This email is already vinculated to another user'},
            status=status.HTTP_400_BAD_REQUEST,
        )
    user.email = request.data['email']
    user.save()
    return Response({'email': request.user.email})


@api_view(['POST'])
def check_password(request):
    password = request.data['password']
    authenticated = request.user.check_password(password)
    return Response({'authenticated': authenticated})
