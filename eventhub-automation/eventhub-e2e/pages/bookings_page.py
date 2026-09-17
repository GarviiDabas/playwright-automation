import re
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from constants import BOOKINGS_URL

class BookingsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)

    def navigate(self):
        self.page.goto(BOOKINGS_URL)
        return self

    def verify_bookings_page_loaded(self):
        expect(self.page).to_have_url(re.compile(r".*/bookings$"))

    def get_event_booking(self, event_name: str):
        return self.page.get_by_test_id("booking-card").filter(has_text=event_name).first

    def view_booking_details(self, event_name: str):
        booking = self.get_event_booking(event_name)
        expect(booking).to_be_visible()
        booking.get_by_role("button", name="View Details").click()
        expect(self.page).to_have_url(re.compile(r".*/bookings/\d+$"))
