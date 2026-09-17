import os

# ============================================================
# BASE & ROUTE URL CONSTANTS
# ============================================================

BASE_URL = os.getenv("BASE_URL", "https://eventhub.rahulshettyacademy.com")

LOGIN_URL = f"{BASE_URL}/login"
REGISTRATION_URL = f"{BASE_URL}/register"
EVENTS_URL = f"{BASE_URL}/events"
BOOKINGS_URL = f"{BASE_URL}/bookings"


# ============================================================
# EVENT TEST DATA CONSTANTS
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
