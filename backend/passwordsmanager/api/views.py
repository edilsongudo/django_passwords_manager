from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
from passmanager.models import *
from passmanager.utils import *
from cryptography.fernet import InvalidToken

@api_view(['POST'])
def getData(request):
    data = json.loads(request.body.decode('utf-8'))
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

    return Response(
        {'response': response, 'is_masterpass_correct': True}
    )