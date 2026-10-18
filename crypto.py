import hashlib

def hash_password(testo):
    codifica = hashlib.sha256(testo.encode('utf-8')).hexdigest()
    return codifica