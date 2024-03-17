from ecies.utils import generate_eth_key
from ecies import encrypt, decrypt
import binascii

privKey = generate_eth_key()
privKeyHex = privKey.to_hex()
pubKeyHex = privKey.public_key.to_hex()

def lib_ECEIS_encrypt(message):
    encrypted = encrypt(pubKeyHex, message)
    ciphertext = binascii.hexlify(encrypted)
    return ciphertext

def lib_ECEIS_decrypt(ciphertext):
    decrypted = decrypt(privKeyHex, ciphertext)
    return decrypted