from playwright.sync_api import Page, expect
from constants import BASE_URL
from utils.logger import get_logger

logger = get_logger("BasePage")

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to(self, path: str = ""):
        target_url = f"{BASE_URL}{path}" if path.startswith("/") else path
        logger.info("Navigating to URL: %s", target_url)
        self.page.goto(target_url)

    def get_url(self) -> str:
        return self.page.url

    def verify_url(self, expected_url: str):
        expect(self.page).to_have_url(expected_url)

    def verify_url_pattern(self, pattern):
        expect(self.page).to_have_url(pattern)

