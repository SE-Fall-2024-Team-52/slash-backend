from passlib.context import CryptContext


bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


"""
This module provides utility functions for hashing and verifying passwords using bcrypt.
Functions:
    get_hashed_password(password: str) -> str:
        Hashes a user password using bcrypt and returns the hashed password.
    verify_password(plain_password: str, hashed_password: str) -> bool:
        Verifies a plain password against a hashed password using bcrypt.
"""


def get_hashed_password(password):
    return bcrypt_context.hash(password)


"""
    Verifies a plain password against a hashed password using bcrypt.

    Args:
        plain_password (str): The plain text password to verify.
        hashed_password (str): The hashed password to verify against.

    Returns:
        bool: True if the plain password matches the hashed password, False otherwise.
"""


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)
