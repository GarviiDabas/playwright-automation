import pytest
from playwright.sync_api import Page, expect
from constants import BASE_URL
from config import TEST_EMAIL, TEST_PASSWORD
from pages.login_page import LoginPage

def test_login_valid_credentials(page: Page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(TEST_EMAIL, TEST_PASSWORD)
    expect(page).to_have_url(f"{BASE_URL}/")

def test_login_invalid_password(page: Page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(TEST_EMAIL, "WrongPassword123")
    expect(page).not_to_have_url(f"{BASE_URL}/")

def test_login_invalid_email_format(page: Page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("invalid-email-format", TEST_PASSWORD)
    expect(page.locator(".mt-1.text-xs.text-red-600")).to_be_visible()

def test_login_invalid_email(page: Page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("wrongemail@gmail.com", "WrongPassword123")
    expect(page.locator('div[aria-live="polite"]')).to_be_visible()

def test_login_empty_email(page: Page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("", TEST_PASSWORD)
    expect(page.locator(".mt-1.text-xs.text-red-600")).to_be_visible()

def test_login_empty_password(page: Page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(TEST_EMAIL, "")
    expect(page.locator(".mt-1.text-xs.text-red-600")).to_be_visible()

def test_login_email_with_spaces(page: Page):
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login("invalid email@gmail.com", TEST_PASSWORD)
    expect(page.locator(".mt-1.text-xs.text-red-600")).to_be_visible()
