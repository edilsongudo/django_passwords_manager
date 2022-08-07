import base64
import os
import secrets
import string

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt


def generate_key(password_provided, salt):
    password = password_provided.encode()
    kdf = Scrypt(salt=salt, length=32, n=2 ** 14, r=8, p=1)

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


CHARS = string.ascii_letters + string.digits + string.punctuation


def generate_secure_password(length=20, chars=CHARS):
    password = ''.join(secrets.choice(chars) for i in range(length))
    return password
