from faker import Faker
from constants import (
    BASE_URL,
    EVENT_ID,
    EVENT_NAME,
    EVENT_PRICE,
    EVENT_DATE_SHORT,
    EVENT_DATE_LONG,
    EVENT_TIME,
    EVENT_LOCATION,
    EVENT_CITY,
    EVENT_URL,
    EVENTS_URL,
)

fake = Faker()


# ============================================================
# DYNAMIC TEST DATA HELPERS
# ============================================================

def generate_unique_email() -> str:
    """Generate a dynamic unique email address for registration tests."""
    return fake.unique.email()


def generate_booking_info(email: str) -> dict:
    """Generate dynamic booking form data."""
    return {
        "full_name": fake.name(),
        "email": email,
        "phone": fake.numerify("##########"),
    }

