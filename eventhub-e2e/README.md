# EventHub End-to-End Test Automation Framework

An end-to-end web test automation framework built using **Python**, **Playwright**, and **Pytest**, implementing the **Page Object Model (POM)** design pattern with **encrypted credential management**.

---

## 📌 Features

- **Page Object Model (POM)**: Decoupled UI page elements and actions from test scripts for modularity and maintainability.
- **Encrypted Credentials**: Password encryption using Python's `cryptography` library (`Fernet` AES-128 HMAC symmetric encryption). Sensitive credentials are stored encrypted in JSON and decrypted dynamically at runtime.
- **Dynamic Test Data**: Automated generation of fake user details and unique email addresses via `Faker`.
- **Comprehensive Coverage**: Functional tests covering user registration, login/logout security, event search & metadata, ticket booking, and complete end-to-end user journeys.
- **Pytest Reporting**: Standardized test runner configuration with verbose output and test filtering capabilities.

---

## 📁 Framework Directory Structure

```
eventhub-end-to-end-testing/
├── secret.key                        # Secret Fernet key for decrypting passwords (git-ignored)
├── config.py                         # Centralized config loader & password decryptor
├── conftest.py                       # Global Pytest fixtures (e.g. authenticated page)
├── pytest.ini                        # Pytest settings and CLI defaults
├── requirements.txt                  # Python package dependencies
├── README.md                         # Project documentation
├── pages/                            # Page Object Model classes
│   ├── __init__.py
│   ├── base_page.py                  # Parent class with common Playwright actions
│   ├── login_page.py                 # Login page locators & actions
│   ├── registration_page.py          # User registration page locators & actions
│   ├── home_page.py                  # Home page locators
│   ├── events_page.py                # Event listing and search page
│   ├── event_details_page.py         # Detailed event information page
│   ├── booking_page.py               # Ticket booking form page
│   └── bookings_page.py              # User "My Bookings" page
├── scripts/                          # CLI helper utilities
│   ├── __init__.py
│   └── encrypt_credentials.py        # CLI script to generate secret key & encrypted credentials
├── test_data/                        # Centralized test data & configuration files
│   ├── credentials.json              # Encrypted user credentials (git-ignored)
│   ├── credentials.template.json     # Sample credentials template for version control
│   └── users.json                    # Static test data (e.g. invalid user suites)
├── tests/                            # Pytest test execution suites
│   ├── test_registration.py          # Registration validation tests
│   ├── test_login.py                 # Login authentication tests
│   ├── test_logout.py                # Logout and session security tests
│   ├── test_events.py                # Event search & filter tests
│   ├── test_booking.py               # Ticket reservation tests
│   └── test_full_user_journey.py     # End-to-End full flow test
└── utils/                            # Shared utilities
    ├── __init__.py
    ├── encryption.py                 # Encryption/decryption core module
    └── test_data.py                  # Dynamic test data generators
```

---

## 🛠️ Prerequisites & Setup

### 1. Requirements
- **Python**: `3.8` or higher
- **pip**: Latest version

### 2. Installation
Clone the repository and navigate into the project directory:
```bash
cd eventhub-end-to-end-testing
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

For security, user credentials are encrypted using standard Fernet symmetric encryption and stored in `test_data/credentials.json`.

### Generate Encrypted Credentials
Run the setup script to generate a `secret.key` and populate `test_data/credentials.json`:
```bash
python scripts/encrypt_credentials.py
```

This will automatically create:
1. `secret.key`: Secret key file used to decrypt passwords (never commit this file).
2. `test_data/credentials.json`: Stores `test_email`, `encrypted_password`, and `existing_email`.

> ⚠️ **Security Note**: Both `secret.key` and `test_data/credentials.json` are listed in `.gitignore` to prevent secret leakage into version control.

---

## 🚀 Running Tests

### 1. Run All Tests
Execute the entire test suite in headless mode:
```bash
pytest
```

### 2. Run in Headed Mode
To view browser interactions visually:
```bash
pytest --headed
```

### 3. Run Specific Test Module
Run tests for a single module (e.g., login tests):
```bash
pytest tests/test_login.py
```

### 4. Run a Specific Test Function
```bash
pytest tests/test_booking.py -k "test_book_one_ticket"
```

### 5. Generate HTML Execution Report
```bash
pytest --html=report.html --self-contained-html
```

---

## 📄 License
This repository is maintained for internal automation testing.
