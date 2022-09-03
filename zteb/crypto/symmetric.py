"""
Provides an abstraction over the symmetric encryption scheme primitives.
"""

from cryptography.fernet import Fernet


def generate_key():
    return Fernet.generate_key()


class SymmetricEncryptionScheme:
    """
    An easy to use symmetric encryption scheme.
    """

    def __init__(self, key):
        self._key = key
        self._encryption_scheme = Fernet(self._key)

    def encrypt(self, message: str, encoding: str = 'utf8') -> bytes:
        message_bytes = message.encode(encoding)
        return self._encryption_scheme.encrypt(message_bytes)

    def decrypt(self, cypher: bytes, encoding: str = 'utf8') -> str:
        message_bytes = self._encryption_scheme.decrypt(cypher)
        return message_bytes.decode(encoding)
