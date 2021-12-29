import hashlib
from .utils import *


def check_if_master_password_is_correct(request, masterPassGiven):
    """
        CHECKS if the first 3 chars of the hashed version of the master password
        GIVEN is equal to the first 3 chars of the hashed version of
        the ORIGINAL master password

        -> If that happens it is very likely the correct master password
        so we return true
    """
    key = generate_key(masterPassGiven)
    crypt = hashlib.sha256()
    crypt.update(key.encode())
    key = crypt.hexdigest()
    print(key)
    print(request.user.masterpassword.master)
    if key[0:3] == request.user.masterpassword.master:
        return "true"
    return "false"
