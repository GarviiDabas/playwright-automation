import os
from cryptography.fernet import Fernet

DEFAULT_KEY_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "secret.key")


def generate_key(key_file: str = DEFAULT_KEY_FILE) -> bytes:
    """Generate a new Fernet key and save it to key_file."""
    key = Fernet.generate_key()
    with open(key_file, "wb") as f:
        f.write(key)
    return key


def get_or_create_key(key_file: str = DEFAULT_KEY_FILE) -> bytes:
    """Retrieve encryption key from ENCRYPTION_KEY env var or secret.key file (generating if missing)."""
    env_key = os.getenv("ENCRYPTION_KEY")
    if env_key:
        return env_key.encode("utf-8")

    if os.path.exists(key_file):
        with open(key_file, "rb") as f:
            key = f.read().strip()
            if key:
                return key

    return generate_key(key_file)


def encrypt_password(plain_password: str, key: bytes = None) -> str:
    """Encrypt a plain-text password using Fernet symmetric encryption."""
    if key is None:
        key = get_or_create_key()
    fernet = Fernet(key)
    return fernet.encrypt(plain_password.encode("utf-8")).decode("utf-8")


def decrypt_password(encrypted_password: str, key: bytes = None) -> str:
    """Decrypt a Fernet encrypted password token back to plain text."""
    if key is None:
        key = get_or_create_key()
    fernet = Fernet(key)
    return fernet.decrypt(encrypted_password.encode("utf-8")).decode("utf-8")
