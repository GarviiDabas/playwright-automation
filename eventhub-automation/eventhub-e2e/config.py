import json
import os
from utils.encryption import decrypt_password

from constants import BASE_URL

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
CREDENTIALS_FILE = os.path.join(PROJECT_ROOT, "test_data", "credentials.json")
if not os.path.exists(CREDENTIALS_FILE):
    # Fallback to root credentials.json if present
    CREDENTIALS_FILE = os.path.join(PROJECT_ROOT, "credentials.json")

if not os.path.exists(CREDENTIALS_FILE):
    raise RuntimeError(
        "Credentials file not found at 'test_data/credentials.json'. "
        "Please run 'python scripts/encrypt_credentials.py' to generate credentials."
    )


with open(CREDENTIALS_FILE, "r", encoding="utf-8") as f:
    _credentials = json.load(f)

TEST_EMAIL = _credentials.get("test_email")
_encrypted_password = _credentials.get("encrypted_password")
EXISTING_EMAIL = _credentials.get("existing_email")

if not TEST_EMAIL:
    raise RuntimeError("'test_email' is missing or empty in credentials.json")

if not _encrypted_password:
    raise RuntimeError("'encrypted_password' is missing or empty in credentials.json")

try:
    TEST_PASSWORD = decrypt_password(_encrypted_password)
except Exception as e:
    raise RuntimeError(f"Failed to decrypt password from credentials.json: {e}")

