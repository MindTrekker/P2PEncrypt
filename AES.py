from Crypto.Cipher import AES
from ECDH import *
key = generate_shared_key()
key = bytes.fromhex(key)
data = 'some message to send'.encode()
cipher = AES.new(key, AES.MODE_OCB)
ciphertext, tag = cipher.encrypt_and_digest(data)
assert len(cipher.nonce) == 15
nonce = cipher.nonce
tag = tag
data = ciphertext
decipher = AES.new(key, AES.MODE_OCB, nonce=nonce)
print(decipher.decrypt_and_verify(data, tag))
