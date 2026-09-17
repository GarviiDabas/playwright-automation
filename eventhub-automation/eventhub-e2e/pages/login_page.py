from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from config import BASE_URL
from utils.logger import get_logger

logger = get_logger("LoginPage")

class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = page.get_by_placeholder("you@email.com")
        self.password_input = page.get_by_placeholder("••••••")
        self.sign_in_button = page.get_by_role("button", name="Sign In")
        self.heading = page.get_by_role("heading", name="Sign in to EventHub")

    def navigate(self):
        logger.info("Navigating to login page")
        self.page.goto(f"{BASE_URL}/login")
        return self

    def login(self, email: str, password: str):
        logger.info("Attempting login for user: %s", email)
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.sign_in_button.click()

    def verify_login_page_loaded(self):
        expect(self.heading).to_be_visible()

