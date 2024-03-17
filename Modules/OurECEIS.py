from AES import encrypt, decrypt
from generate_points import *
import hashlib

#Call for key exchange
def our_ecdh(privatekey, publickey, a, p):
    shared_key_point_x = calc_shared_point(privatekey, publickey, a, p)
    value = str(hex(shared_key_point_x)).encode('utf-8')
    key = hashlib.sha256((value))
    key = key.hexdigest()

#Encrypts using agreed upon diffie-hellman key, encrypts using AES
def eceis_encrypt(message, key):
    ciphertext, tag, nonce = encrypt(key, message)
    return ciphertext, tag, nonce

#Decrypts using AES, and diffie-hellman key
def eceis_decrypt(key, ciphertext, tag, nonce):
    message = decrypt(key, ciphertext, tag, nonce)
    return message