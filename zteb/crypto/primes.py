"""
Functionality for randomly picking large prime numbers.
"""


from typing import Tuple
from cryptography.hazmat.primitives.asymmetric import rsa


def get_large_primes_tuple() -> Tuple[int, int]:
    """
    Returns
    -------
    A tuple of two large prime numbers.
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    return (
        private_key.private_numbers().p,
        private_key.private_numbers().q,
    )
