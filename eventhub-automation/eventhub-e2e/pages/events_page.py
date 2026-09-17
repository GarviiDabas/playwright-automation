import re
from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from constants import EVENTS_URL

class EventsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.heading = page.get_by_role("heading", name="Upcoming Events")
        self.search_input = page.get_by_placeholder("Search events, venues…")

    def navigate(self):
        self.page.goto(EVENTS_URL)
        return self

    def verify_events_page_loaded(self):
        expect(self.heading).to_be_visible()

    def get_event_cards(self):
        return self.page.locator('[data-testid="event-card"]')

    def get_event_by_name(self, event_name: str):
        return self.get_event_cards().filter(has_text=event_name)

    def search_event(self, search_text: str):
        self.search_input.fill(search_text)
        self.search_input.press("Enter")
        self.page.wait_for_load_state("domcontentloaded")
        return self.search_input

    def select_event(self, event_name: str):
        event_card = self.get_event_by_name(event_name)
        expect(event_card).to_be_visible()
        book_btn = event_card.get_by_test_id("book-now-btn")
        try:
            book_btn.click()
            expect(self.page).to_have_url(re.compile(r".*/events/\d+$"), timeout=3000)
        except AssertionError:
            book_btn.click()
            expect(self.page).to_have_url(re.compile(r".*/events/\d+$"))


