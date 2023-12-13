import hashlib

class Encrypt:

    @staticmethod
    def encrypt(password):
        hash_object = hashlib.sha512()
        hash_object.update(password.encode('utf-8'))

        return hash_object.hexdigest()
