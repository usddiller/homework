from typing import Literal

import rsa
from django.conf import settings


def read_keys_from_file(file: Literal["private", "public"]) -> str:
    path: str = settings.KEYS_PATH
    if file == "private":
        path += "/private.txt"
    elif file == "public":
        path += "/public.txt"
    with open(file=path, mode="r") as f:
        content = f.read()
    return content


def encrypt_message(text: str) -> str:
    key = read_keys_from_file(file="public")
    public_key: rsa.PublicKey = \
        rsa.PublicKey.load_pkcs1(key.encode("utf-8"))
    message: bytes = text.encode("utf-8")
    encrypted_text = rsa.encrypt(message=message, pub_key=public_key)
    return encrypted_text.hex()


def decrypt_message(encrypted_text: str) -> str:
    key = read_keys_from_file(file="private")
    private_key: rsa.PrivateKey = \
        rsa.PrivateKey.load_pkcs1(key.encode("utf-8"))
    message: bytes = bytes.fromhex(encrypted_text)
    decrypted: bytes = rsa.decrypt(message, private_key)
    return decrypted.decode("utf-8")
