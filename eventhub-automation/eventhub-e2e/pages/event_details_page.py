import re
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from config import BASE_URL, TEST_EMAIL
from utils.test_data import EVENT_NAME, EVENT_URL
from utils.logger import get_logger

logger = get_logger("EventDetailsPage")

class EventDetailsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.ticket_count_label = page.locator("#ticket-count")
        self.full_name_input = page.get_by_label("Full Name")
        self.email_input = page.get_by_label("Email")
        self.phone_input = page.get_by_label("Phone Number")
        self.confirm_booking_button = page.get_by_role("button", name="Confirm Booking")
        self.view_my_bookings_link = page.get_by_role("link", name="View My Bookings")

    def open_event(self, event_url: str = EVENT_URL, event_name: str = EVENT_NAME):
        logger.info("Opening event page: %s", event_url)
        self.page.goto(event_url)
        expect(self.page.get_by_role("heading", name=event_name)).to_be_visible()

    def fill_booking_form(self, full_name: str, email: str = TEST_EMAIL, phone: str = "9876543210") -> dict:
        booking_data = {
            "full_name": full_name,
            "email": email,
            "phone": phone,
        }
        self.full_name_input.fill(booking_data["full_name"])
        self.email_input.fill(booking_data["email"])
        self.phone_input.fill(booking_data["phone"])
        return booking_data

    def increase_ticket_count(self, times: int = 1):
        logger.info("Increasing ticket count by %d", times)
        ticket_section = self.ticket_count_label.locator("..")
        plus_button = ticket_section.get_by_role("button").nth(1)
        for _ in range(times):
            plus_button.click()

    def confirm_booking(self):
        logger.info("Submitting booking confirmation")
        self.confirm_booking_button.click()
        expect(
            self.page.get_by_role("heading", name=re.compile("Booking Confirmed"))
        ).to_be_visible()

    def get_plus_button(self):
        ticket_section = self.ticket_count_label.locator("..")
        return ticket_section.get_by_role("button").nth(1)

