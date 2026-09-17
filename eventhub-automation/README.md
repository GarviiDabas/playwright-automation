# EventHub End-to-End Test Automation Framework

An end-to-end web test automation framework built using **Python**, **Playwright**, and **Pytest**, implementing the **Page Object Model (POM)** design pattern with **encrypted credential management** and **centralized constants**.

---

## 📌 Features

- **Page Object Model (POM)**: Decoupled UI page elements and actions from test scripts for modularity and maintainability.
- **Centralized Constants**: Application URLs, page routes, and test data constants centrally organized in `constants.py`.
- **Encrypted Credentials**: Password encryption using Python's `cryptography` library (`Fernet` AES-128 HMAC symmetric encryption). Sensitive credentials are stored encrypted in JSON and decrypted dynamically at runtime.
- **Dynamic Test Data**: Automated generation of fake user details and unique email addresses via `Faker`.
- **Comprehensive Coverage**: Functional tests covering user registration, login/logout security, event search & metadata, ticket booking, and complete end-to-end user journeys.
- **Pytest Reporting**: Standardized test runner configuration with verbose log outputs and HTML report generation.

---

## 📁 Framework Directory Structure

```
eventhub-automation/
└── eventhub-e2e/
    ├── constants.py                  # Centralized application & route constants
    ├── config.py                     # Config loader & password decryptor
    ├── conftest.py                   # Global Pytest fixtures & execution hooks
    ├── pytest.ini                    # Pytest settings and CLI defaults
    ├── requirements.txt              # Python package dependencies
    ├── README.md                     # Project documentation
    ├── pages/                        # Page Object Model classes
    │   ├── base_page.py              # Parent class with common Playwright actions
    │   ├── login_page.py             # Login page locators & actions
    │   ├── registration_page.py      # User registration page locators & actions
    │   ├── home_page.py              # Home page locators & session actions
    │   ├── events_page.py            # Event listing and search page
    │   ├── event_details_page.py     # Detailed event information page
    │   ├── booking_page.py           # Ticket booking form page
    │   └── bookings_page.py          # User "My Bookings" page
    ├── scripts/                      # CLI helper utilities
    │   └── encrypt_credentials.py    # Utility to generate secret key & encrypted credentials
    ├── test_data/                    # Centralized test data
    │   ├── credentials.json          # Encrypted user credentials (git-ignored)
    │   └── credentials.template.json # Sample credentials template for version control
    ├── tests/                        # Pytest test execution suites
    │   ├── test_registration.py      # Registration validation tests
    │   ├── test_login.py             # Login authentication tests
    │   ├── test_logout.py            # Logout and session security tests
    │   ├── test_events.py            # Event search & filter tests
    │   ├── test_booking.py           # Ticket reservation tests
    │   └── test_full_user_journey.py # End-to-End full flow test
    └── utils/                        # Shared utilities
        ├── encryption.py             # Encryption/decryption core module
        ├── logger.py                 # Centralized logging setup
        └── test_data.py              # Dynamic test data generators
```

---

## 🛠️ Prerequisites & Setup

### 1. Requirements
- **Python**: `3.8` or higher
- **pip**: Latest version

### 2. Installation
Navigate into the `eventhub-e2e` project directory:
```bash
cd eventhub-e2e
```

Install the required Python packages:
```bash
pip install -r requirements.txt
```

Install Playwright browser binaries:
```bash
playwright install
```

---

## 🔐 Credential Encryption Setup

For security, user credentials are encrypted using Fernet symmetric encryption and stored in `test_data/credentials.json`.

### Generate Encrypted Credentials
Run the setup script to generate `secret.key` and `test_data/credentials.json`:
```bash
python scripts/encrypt_credentials.py
```

---

## 🚀 Running Tests

### 1. Run All Tests
Execute the entire test suite:
```bash
pytest
```

### 2. Run in Headed Mode
To view browser interactions visually:
```bash
pytest --headed
```

### 3. Run Specific Test Suite
```bash
pytest tests/test_login.py
```

### 4. Generate HTML Execution Report
```bash
pytest --html=reports/report.html --self-contained-html
```
