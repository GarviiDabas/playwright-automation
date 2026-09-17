from faker import Faker
from config import BASE_URL

fake = Faker()

# ============================================================
# CENTRALIZED EVENT CONSTANTS
# ============================================================

EVENT_ID = 285
EVENT_NAME = "Dilli Diwali Mela"
EVENT_PRICE = 300

EVENT_DATE_SHORT = "Tue, 20 Oct"
EVENT_DATE_LONG = "Tuesday, 20 October"
EVENT_TIME = "10:30 pm"

EVENT_LOCATION = "Pragati Maidan Exhibition Grounds"
EVENT_CITY = "Delhi"

EVENT_URL = f"{BASE_URL}/events/{EVENT_ID}"
EVENTS_URL = f"{BASE_URL}/events"


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

