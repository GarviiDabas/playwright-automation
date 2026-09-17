from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger("HomePage")

class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.nav_events_link = page.get_by_test_id("nav-events")
        self.nav_bookings_link = page.get_by_test_id("nav-bookings")
        self.logout_button = page.get_by_role("button", name="Logout")

    def navigate(self):
        self.navigate_to("/")
        return self


    def logout(self):
        if self.logout_button.is_visible():
            logger.info("Logging out current user session")
            self.logout_button.click()

    def go_to_events(self):
        self.nav_events_link.click()

    def go_to_my_bookings(self):
        self.nav_bookings_link.click()

