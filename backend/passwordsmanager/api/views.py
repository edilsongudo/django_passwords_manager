import json

from cryptography.fernet import InvalidToken
from rest_framework.decorators import api_view
from rest_framework.response import Response

from passmanager.forms import *
from passmanager.models import *
from passmanager.utils import *


@api_view(['POST'])
def getEntries(request):
    data = json.loads(request.body.decode('utf-8'))
    masterpassword = data['masterpassword']
    key = generate_key(masterpassword, request.user.masterpassword.salt)

    response = []
    entries = Entry.objects.filter(author=request.user).exclude(
        is_generated_for_initial_master_pw_check=True
    )

    for entry in entries:
        try:
            entry_email = decrypt(
                encrypted=entry.site_email_used.encode(), key=key.encode()
            )

            entry_password = decrypt(
                encrypted=entry.site_password_used.encode(),
                key=key.encode(),
            )

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
    data = json.loads(request.body.decode('utf-8'))
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

        return Response(response)
    return Response({'status': 'fail', 'errors': form.errors})


@api_view(['POST'])
def deleteEntry(request):
    data = json.loads(request.body.decode('utf-8'))
    pk = data['id']
    entry = Entry.objects.get(pk=pk)
    if entry.author == request.user:
        entry.delete()
        return Response({'response': 'ok'})
    return Response({'response': 'fail'})


@api_view(['GET'])
def has_user_defined_a_master_password(request):
    return Response(
        {
            'has_user_defined_a_master_password': request.user.masterpassword.has_defined_a_master_password
        }
    )
