import pytest
from playwright.sync_api import Page, expect
from config import BASE_URL
from pages.home_page import HomePage

LOGIN_URL = f"{BASE_URL}/login"
PROTECTED_URL = f"{BASE_URL}/bookings"

def test_logout_redirects_to_login(logged_in_page: Page):
    page = logged_in_page
    home_page = HomePage(page)
    home_page.logout()
    expect(page).to_have_url(LOGIN_URL)
    expect(page.get_by_role("heading", name="Sign in to EventHub")).to_be_visible()

def test_logout_successfully(logged_in_page: Page):
    page = logged_in_page
    home_page = HomePage(page)
    expect(home_page.logout_button).to_be_visible()
    home_page.logout()
    expect(page).to_have_url(LOGIN_URL)

def test_logout_terminates_session(logged_in_page: Page):
    page = logged_in_page
    home_page = HomePage(page)
    home_page.logout()
    expect(page).to_have_url(LOGIN_URL)
    page.goto(PROTECTED_URL)
    expect(page).to_have_url(LOGIN_URL)
    expect(page.get_by_role("heading", name="Sign in to EventHub")).to_be_visible()

def test_protected_page_inaccessible_after_logout(logged_in_page: Page):
    page = logged_in_page
    home_page = HomePage(page)
    home_page.logout()
    page.goto(PROTECTED_URL)
    expect(page).to_have_url(LOGIN_URL)

def test_browser_back_does_not_restore_session(logged_in_page: Page):
    page = logged_in_page
    home_page = HomePage(page)
    home_page.logout()
    page.go_back()
    expect(page).to_have_url(LOGIN_URL)

def test_refresh_after_logout_keeps_user_logged_out(logged_in_page: Page):
    page = logged_in_page
    home_page = HomePage(page)
    home_page.logout()
    expect(page).to_have_url(LOGIN_URL)
    page.reload()
    expect(page).to_have_url(LOGIN_URL)
    expect(page.get_by_role("heading", name="Sign in to EventHub")).to_be_visible()

