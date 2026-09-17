import getpass
import json
import os
import sys

# Add project root directory to sys.path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utils.encryption import get_or_create_key, encrypt_password

TEST_DATA_DIR = os.path.join(PROJECT_ROOT, "test_data")
os.makedirs(TEST_DATA_DIR, exist_ok=True)

CREDENTIALS_FILE = os.path.join(TEST_DATA_DIR, "credentials.json")
TEMPLATE_FILE = os.path.join(TEST_DATA_DIR, "credentials.template.json")


def create_credentials_json(
    test_email: str = None,
    test_password: str = None,
    existing_email: str = None,
):
    """Encrypt password and save credentials JSON file along with a template file."""
    test_email = (
        test_email
        or os.getenv("TEST_USER_EMAIL")
        or input("Enter test email [default: testuser@gmail.com]: ").strip()
        or "testuser@gmail.com"
    )
    test_password = test_password or os.getenv("TEST_USER_PASSWORD")
    if not test_password:
        test_password = getpass.getpass("Enter test password: ")

    existing_email = (
        existing_email
        or os.getenv("EXISTING_USER_EMAIL")
        or input("Enter existing user email [default: existinguser@gmail.com]: ").strip()
        or "existinguser@gmail.com"
    )

    key = get_or_create_key()
    encrypted_pw = encrypt_password(test_password, key)

    credentials_data = {
        "test_email": test_email,
        "encrypted_password": encrypted_pw,
        "existing_email": existing_email,
    }

    with open(CREDENTIALS_FILE, "w", encoding="utf-8") as f:
        json.dump(credentials_data, f, indent=2)

    template_data = {
        "test_email": "user@example.com",
        "encrypted_password": "<ENCRYPTED_FERNET_PASSWORD_TOKEN>",
        "existing_email": "existing_user@example.com",
    }
    with open(TEMPLATE_FILE, "w", encoding="utf-8") as f:
        json.dump(template_data, f, indent=2)

    print("Secret key generated/validated.")
    print(f"Successfully generated encrypted credentials file: {CREDENTIALS_FILE}")
    print(f"Created template credentials file: {TEMPLATE_FILE}")


if __name__ == "__main__":
    create_credentials_json()

