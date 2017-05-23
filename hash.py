import hashlib


def hash_password(password):
    m = hashlib.md5()
    m.update(password.encode('utf-8'))
    return m.hexdigest()
