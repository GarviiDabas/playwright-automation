import pytest
from playwright.sync_api import Page, expect
from constants import BASE_URL
from config import TEST_PASSWORD, EXISTING_EMAIL
from pages.registration_page import RegistrationPage
from utils.test_data import generate_unique_email

def test_registration_valid_user(page: Page):
    registration_page = RegistrationPage(page)
    registration_page.navigate()
    unique_email = generate_unique_email()
    registration_page.register(email=unique_email, password=TEST_PASSWORD, confirm_password=TEST_PASSWORD)
    expect(page).not_to_have_url(f"{BASE_URL}/register")

def test_registration_duplicate_email(page: Page):
    registration_page = RegistrationPage(page)
    registration_page.navigate()
    registration_page.register(email=EXISTING_EMAIL, password=TEST_PASSWORD, confirm_password=TEST_PASSWORD)
    expect(page.get_by_text("already registered", exact=False)).to_be_visible()

def test_registration_password_mismatch(page: Page):
    registration_page = RegistrationPage(page)
    registration_page.navigate()
    registration_page.register(email=generate_unique_email(), password=TEST_PASSWORD, confirm_password="DifferentPassword1!")
    expect(page.get_by_text("match", exact=False)).to_be_visible()

def test_register_with_invalid_email(page: Page):
    registration_page = RegistrationPage(page)
    registration_page.navigate()
    registration_page.register(email="invalid-email", password=TEST_PASSWORD, confirm_password=TEST_PASSWORD)
    expect(page).to_have_url(f"{BASE_URL}/register")

def test_register_with_empty_fields(page: Page):
    registration_page = RegistrationPage(page)
    registration_page.navigate()
    registration_page.submit()
    expect(page).to_have_url(f"{BASE_URL}/register")
    expect(registration_page.email_input).to_be_visible()
    expect(registration_page.password_input).to_be_visible()

def test_password_below_minimum_length(page: Page):
    registration_page = RegistrationPage(page)
    registration_page.navigate()
    invalid_password = "Pass1!"
    registration_page.register(email=generate_unique_email(), password=invalid_password, confirm_password=invalid_password)
    expect(page).to_have_url(f"{BASE_URL}/register")

def test_password_with_special_characters(page: Page):
    registration_page = RegistrationPage(page)
    registration_page.navigate()
    password = "Password1!"
    registration_page.register(email=generate_unique_email(), password=password, confirm_password=password)
    expect(page.get_by_text("One special character", exact=False)).to_be_visible()

