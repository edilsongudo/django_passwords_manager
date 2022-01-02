import base64
import os
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.fernet import Fernet
import secrets


def generate_key(password_provided):
    password = password_provided.encode()
    # os.urandom(32)
    salt = b'\xf8\x10P\xc3\xe0\xaa\x08\x8cF\x81\xb6\xdf\x1fw6RA\rn%\xbf\xd6~\x9a\xbetA\xf0yMYj'
    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1
    )

    key = base64.urlsafe_b64encode(kdf.derive(password))
    return key.decode()


def encrypt(message, key):
    f = Fernet(key)
    encrypted = f.encrypt(message.encode())
    return encrypted.decode()


def decrypt(encrypted, key):
    f = Fernet(key)
    decrypted = f.decrypt(encrypted)
    return decrypted.decode()
