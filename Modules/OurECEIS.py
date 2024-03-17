from Modules.AES import encrypt, decrypt
from Modules.generate_points import *
import hashlib

shared_key_point = shared_key_generator()
value = str(hex(shared_key_point)).encode('utf-8')
key = hashlib.sha256((value))
key = key.hexdigest()

def eceis_encrypt(message):
    ciphertext, tag, nonce = encrypt(key, message)
    return ciphertext, tag, nonce

def eceis_decrypt(key, ciphertext, tag, nonce):
    message = decrypt(key, ciphertext, tag, nonce)
    return message

ct, tag, nonce = eceis_encrypt('some message')
print('Encrypted')
print(ct)
print('decrypted')
msg = eceis_decrypt(key, ct, tag, nonce)
print(msg)