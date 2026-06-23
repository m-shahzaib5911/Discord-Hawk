# crypto_utils.py
import os
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def encrypt_data(plaintext: str, key: bytes) -> str:
    """
    Encrypt plaintext with AES-256-GCM using the supplied key.
    Returns base64-encoded (nonce + ciphertext).
    """
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, plaintext.encode('utf-8'), None)
    return base64.b64encode(nonce + ciphertext).decode('utf-8')


def decrypt_data(payload: str, key: bytes) -> str:
    """
    Decrypt a base64-encoded (nonce + ciphertext) string using the supplied key.
    Returns original plaintext.
    """
    aesgcm = AESGCM(key)
    raw = base64.b64decode(payload)
    nonce, ciphertext = raw[:12], raw[12:]
    return aesgcm.decrypt(nonce, ciphertext, None).decode('utf-8')