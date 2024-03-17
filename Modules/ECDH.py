from coincurve import PrivateKey
import hashlib

key1 = PrivateKey(b'123456789')
key2 = PrivateKey(b'101112131')
#print(key1.public_key.format(False).hex())

def generate_shared_key():
    shared_public_key = key2.public_key.multiply(bytes.fromhex(key1.to_hex()))
    h = hashlib.sha256()
    h.update(shared_public_key.format())
    return h.hexdigest()
#print(generate_shared_key())