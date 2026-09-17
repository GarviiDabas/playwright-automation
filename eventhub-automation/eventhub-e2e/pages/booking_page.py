import re
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from utils.logger import get_logger

logger = get_logger("BookingPage")

class BookingPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.booking_ref = page.locator(".booking-ref")
        self.tickets_label = page.get_by_text("Tickets", exact=True)
        self.total_label = page.get_by_text("Total", exact=True)
        self.confirmed_heading = page.get_by_role("heading", name=re.compile("Booking Confirmed"))

    def verify_confirmation_details(self):
        expect(self.confirmed_heading).to_be_visible()
        expect(self.booking_ref).to_be_visible()
        expect(self.tickets_label).to_be_visible()
        expect(self.total_label).to_be_visible()
        logger.info("Verified booking confirmation details successfully")

