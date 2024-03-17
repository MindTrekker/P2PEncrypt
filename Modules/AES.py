from Crypto.Cipher import AES
from ECDH import *
def encrypt(key, data):

    key = bytes.fromhex(key)
    print('The key in AES: ' + str(key))
    data = str(data).encode()
    cipher = AES.new(key, AES.MODE_OCB)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    assert len(cipher.nonce) == 15
    return ciphertext, tag, cipher.nonce

def decrypt(key, data, tag, nonce):
    
    key = bytes.fromhex(key)
    decipher = AES.new(key, AES.MODE_OCB, nonce=nonce)
    message = decipher.decrypt_and_verify(data, tag)
    return message
