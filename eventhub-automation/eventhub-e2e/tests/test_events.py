import pytest
from playwright.sync_api import Page, expect
from config import BASE_URL
from pages.events_page import EventsPage
from pages.event_details_page import EventDetailsPage
from utils.test_data import (
    EVENT_ID,
    EVENT_NAME,
    EVENT_PRICE,
    EVENT_DATE_SHORT,
    EVENT_DATE_LONG,
    EVENT_TIME,
    EVENT_LOCATION,
    EVENT_CITY,
    EVENT_URL,
    EVENTS_URL,
)

def test_events_are_displayed(logged_in_page: Page):
    page = logged_in_page
    events_page = EventsPage(page)
    events_page.navigate()
    cards = events_page.get_event_cards()
    expect(cards.first).to_be_visible()
    assert cards.count() > 0

def test_event_cards_contain_required_information(logged_in_page: Page):
    page = logged_in_page
    events_page = EventsPage(page)
    events_page.navigate()
    cards = events_page.get_event_cards()
    expect(cards.first).to_be_visible()
    first_event = cards.first

    expect(first_event.locator("h3")).to_be_visible()
    expect(first_event.get_by_text(EVENT_DATE_SHORT, exact=True)).to_be_visible()
    expect(first_event.get_by_text(f"{EVENT_LOCATION}, {EVENT_CITY}", exact=True)).to_be_visible()
    expect(first_event.get_by_text(f"${EVENT_PRICE}", exact=True)).to_be_visible()
    expect(first_event.get_by_text("seats available", exact=False)).to_be_visible()
    expect(first_event.get_by_test_id("book-now-btn")).to_be_visible()

def test_select_event_from_list(logged_in_page: Page):
    page = logged_in_page
    events_page = EventsPage(page)
    events_page.navigate()
    event_card = events_page.get_event_by_name("World Tech Summit")
    expect(event_card).to_be_visible()
    event_card.get_by_role("link").first.click()
    expect(page).to_have_url(f"{BASE_URL}/events/283")

def test_search_existing_event(logged_in_page: Page):
    page = logged_in_page
    events_page = EventsPage(page)
    events_page.navigate()
    events_page.search_event(EVENT_NAME)
    expect(events_page.get_event_by_name(EVENT_NAME)).to_be_visible()

def test_search_non_existing_event(logged_in_page: Page):
    page = logged_in_page
    events_page = EventsPage(page)
    events_page.navigate()
    events_page.search_event("Non Existing Event XYZ")
    expect(events_page.get_event_cards()).to_have_count(0)

def test_search_empty_value(logged_in_page: Page):
    page = logged_in_page
    events_page = EventsPage(page)
    events_page.navigate()
    events_page.search_event("")
    expect(events_page.get_event_cards().first).to_be_visible()

def test_search_partial_event_name(logged_in_page: Page):
    page = logged_in_page
    events_page = EventsPage(page)
    events_page.navigate()
    events_page.search_event("Dilli")
    expect(events_page.get_event_by_name(EVENT_NAME)).to_be_visible()

def test_search_different_capitalization(logged_in_page: Page):
    page = logged_in_page
    events_page = EventsPage(page)
    events_page.navigate()
    events_page.search_event(EVENT_NAME.lower())
    expect(events_page.get_event_by_name(EVENT_NAME)).to_be_visible()

def test_search_with_leading_trailing_spaces(logged_in_page: Page):
    page = logged_in_page
    events_page = EventsPage(page)
    events_page.navigate()
    events_page.search_event(f"  {EVENT_NAME}  ")
    expect(events_page.get_event_by_name(EVENT_NAME)).to_be_visible()

def test_search_special_characters(logged_in_page: Page):
    page = logged_in_page
    events_page = EventsPage(page)
    events_page.navigate()
    events_page.search_event("@#$%^&*")
    expect(events_page.get_event_cards()).to_have_count(0)

def test_search_very_long_text(logged_in_page: Page):
    page = logged_in_page
    events_page = EventsPage(page)
    events_page.navigate()
    search = events_page.search_event(f"{EVENT_NAME} " * 100)
    expect(search).to_be_visible()
    expect(events_page.get_event_cards()).to_have_count(0)

def test_event_details_page_opens(logged_in_page: Page):
    page = logged_in_page
    details_page = EventDetailsPage(page)
    details_page.open_event(EVENT_URL, EVENT_NAME)
    expect(page).to_have_url(EVENT_URL)

def test_event_name_is_displayed(logged_in_page: Page):
    page = logged_in_page
    details_page = EventDetailsPage(page)
    details_page.open_event(EVENT_URL, EVENT_NAME)

def test_event_date_time_is_displayed(logged_in_page: Page):
    page = logged_in_page
    details_page = EventDetailsPage(page)
    details_page.open_event(EVENT_URL, EVENT_NAME)
    expect(page.get_by_text(EVENT_DATE_LONG, exact=True)).to_be_visible()
    expect(page.get_by_text(EVENT_TIME, exact=True)).to_be_visible()

def test_event_location_is_displayed(logged_in_page: Page):
    page = logged_in_page
    details_page = EventDetailsPage(page)
    details_page.open_event(EVENT_URL, EVENT_NAME)
    expect(page.get_by_text(EVENT_LOCATION, exact=True)).to_be_visible()
    expect(page.get_by_text(EVENT_CITY, exact=True)).to_be_visible()

def test_event_description_is_displayed(logged_in_page: Page):
    page = logged_in_page
    details_page = EventDetailsPage(page)
    details_page.open_event(EVENT_URL, EVENT_NAME)
    expect(page.get_by_role("heading", name="About this event")).to_be_visible()

def test_event_availability_is_displayed(logged_in_page: Page):
    page = logged_in_page
    details_page = EventDetailsPage(page)
    details_page.open_event(EVENT_URL, EVENT_NAME)
    expect(page.get_by_text("seats", exact=False)).to_be_visible()
