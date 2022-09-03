"""
Exploratory tests for the cryptography package.
"""


from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa


def test_retrieve_rsa_parameters():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    p, q = private_key.private_numbers().p, private_key.private_numbers().q
    n = private_key.public_key().public_numbers().n

    # sufficiently large (we would have to hope they are prime)
    assert p > 10e6
    assert q > 10e6

    # n is really the product
    assert p * q == n


def test_symmetric_encryption():
    message = "A really secret message. Not for prying eyes."
    message_bytes = message.encode('utf8')

    key = Fernet.generate_key()
    assert key is not None

    scheme = Fernet(key)

    cypher = scheme.encrypt(message_bytes)
    assert cypher != message_bytes
    assert cypher != message

    decrypted = scheme.decrypt(cypher)
    assert decrypted == message_bytes
