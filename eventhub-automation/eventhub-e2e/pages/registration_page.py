from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from constants import REGISTRATION_URL
from config import TEST_PASSWORD
from utils.test_data import generate_unique_email
from utils.logger import get_logger

logger = get_logger("RegistrationPage")

class RegistrationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = page.get_by_test_id("register-email")
        self.password_input = page.get_by_test_id("register-password")
        self.confirm_password_input = page.get_by_placeholder("Repeat your password")
        self.register_button = page.get_by_role("button", name="Create Account")
        self.heading = page.get_by_role("heading", name="Create an Account")

    def navigate(self):
        logger.info("Navigating to registration page")
        self.page.goto(REGISTRATION_URL)
        return self

    def fill_registration_form(
        self,
        email: str = None,
        password: str = TEST_PASSWORD,
        confirm_password: str = TEST_PASSWORD,
    ) -> str:
        email = email or generate_unique_email()
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.confirm_password_input.fill(confirm_password)
        return email

    def submit(self):
        self.register_button.click()

    def register(
        self,
        email: str = None,
        password: str = TEST_PASSWORD,
        confirm_password: str = TEST_PASSWORD,
    ) -> str:
        used_email = self.fill_registration_form(email, password, confirm_password)
        logger.info("Submitting registration for email: %s", used_email)
        self.submit()
        return used_email

