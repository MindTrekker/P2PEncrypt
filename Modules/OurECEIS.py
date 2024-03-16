from Modules import AES
from Modules import generate_points

shared_key_point = generate_points.generate_points()
key_equal_x_value = shared_key_point[0]

def encrypt(message):
    ciphertext, tag, nonce = AES.encrypt(shared_key_point, message)
    return ciphertext, tag, nonce

def decrypt(key_equal_x_value, ciphertext, tag, nonce):
    message = AES.decrypt(key_equal_x_value, ciphertext, tag, nonce)
    return message

ct, tag, nonce = encrypt('some message')
print(ct)
