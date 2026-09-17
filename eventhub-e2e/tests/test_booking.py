import re
import pytest
from playwright.sync_api import Page, expect
from config import BASE_URL, TEST_EMAIL
from pages.event_details_page import EventDetailsPage
from pages.booking_page import BookingPage
from pages.bookings_page import BookingsPage
from utils.test_data import EVENT_NAME, EVENT_PRICE, EVENT_URL, generate_booking_info

def test_book_available_event(logged_in_page: Page):
    page = logged_in_page
    event_details = EventDetailsPage(page)
    event_details.open_event(EVENT_URL, EVENT_NAME)
    booking_data = generate_booking_info(TEST_EMAIL)
    event_details.fill_booking_form(booking_data["full_name"], booking_data["email"], booking_data["phone"])
    assert booking_data["email"] == TEST_EMAIL
    event_details.confirm_booking()

def test_verify_booking_confirmation(logged_in_page: Page):
    page = logged_in_page
    event_details = EventDetailsPage(page)
    booking_page = BookingPage(page)
    event_details.open_event(EVENT_URL, EVENT_NAME)
    booking_data = generate_booking_info(TEST_EMAIL)
    event_details.fill_booking_form(booking_data["full_name"], booking_data["email"], booking_data["phone"])
    event_details.confirm_booking()
    booking_page.verify_confirmation_details()

def test_verify_booking_in_my_bookings(logged_in_page: Page):
    page = logged_in_page
    event_details = EventDetailsPage(page)
    bookings_page = BookingsPage(page)
    event_details.open_event(EVENT_URL, EVENT_NAME)
    booking_data = generate_booking_info(TEST_EMAIL)
    event_details.fill_booking_form(booking_data["full_name"], booking_data["email"], booking_data["phone"])
    event_details.confirm_booking()
    event_details.view_my_bookings_link.click()
    bookings_page.verify_bookings_page_loaded()
    booking = bookings_page.get_event_booking(EVENT_NAME)
    expect(booking).to_be_visible()
    expect(booking.get_by_text("confirmed")).to_be_visible()

def test_book_one_ticket(logged_in_page: Page):
    page = logged_in_page
    event_details = EventDetailsPage(page)
    event_details.open_event(EVENT_URL, EVENT_NAME)
    expect(event_details.ticket_count_label).to_have_text("1")
    booking_data = generate_booking_info(TEST_EMAIL)
    event_details.fill_booking_form(booking_data["full_name"], booking_data["email"], booking_data["phone"])
    event_details.confirm_booking()

def test_book_multiple_tickets(logged_in_page: Page):
    page = logged_in_page
    event_details = EventDetailsPage(page)
    event_details.open_event(EVENT_URL, EVENT_NAME)
    event_details.increase_ticket_count(1)
    expect(event_details.ticket_count_label).to_have_text("2")
    booking_data = generate_booking_info(TEST_EMAIL)
    event_details.fill_booking_form(booking_data["full_name"], booking_data["email"], booking_data["phone"])
    event_details.confirm_booking()

def test_book_maximum_allowed_tickets(logged_in_page: Page):
    page = logged_in_page
    event_details = EventDetailsPage(page)
    event_details.open_event(EVENT_URL, EVENT_NAME)
    event_details.increase_ticket_count(9)
    expect(event_details.ticket_count_label).to_have_text("10")
    booking_data = generate_booking_info(TEST_EMAIL)
    event_details.fill_booking_form(booking_data["full_name"], booking_data["email"], booking_data["phone"])
    event_details.confirm_booking()

def test_ticket_quantity_cannot_exceed_ten(logged_in_page: Page):
    page = logged_in_page
    event_details = EventDetailsPage(page)
    event_details.open_event(EVENT_URL, EVENT_NAME)
    event_details.increase_ticket_count(9)
    expect(event_details.ticket_count_label).to_have_text("10")
    plus_button = event_details.get_plus_button()
    expect(plus_button).to_be_disabled()

def test_event_has_available_seats(logged_in_page: Page):
    page = logged_in_page
    event_details = EventDetailsPage(page)
    event_details.open_event(EVENT_URL, EVENT_NAME)
    expect(page.get_by_text("Available", exact=True)).to_be_visible()
    expect(page.get_by_text(re.compile(r"\d+\s*/\s*\d+\s*seats"))).to_be_visible()

def test_unauthenticated_user_is_redirected_to_login(page: Page):
    page.goto(EVENT_URL)
    expect(page).to_have_url(f"{BASE_URL}/login")
    expect(page.get_by_role("heading", name="Sign in to EventHub")).to_be_visible()

def test_booking_form_after_reload(logged_in_page: Page):
    page = logged_in_page
    event_details = EventDetailsPage(page)
    event_details.open_event(EVENT_URL, EVENT_NAME)
    expect(event_details.ticket_count_label).to_have_text("1")
    booking_data = generate_booking_info(TEST_EMAIL)
    event_details.fill_booking_form(booking_data["full_name"], booking_data["email"], booking_data["phone"])
    page.reload()
    expect(page.get_by_role("heading", name=EVENT_NAME)).to_be_visible()
    expect(event_details.ticket_count_label).to_have_text("1")

def test_browser_back_from_booking_page(logged_in_page: Page):
    page = logged_in_page
    event_details = EventDetailsPage(page)
    page.goto(f"{BASE_URL}/events")
    expect(page.get_by_role("heading", name="Upcoming Events")).to_be_visible()
    event_details.open_event(EVENT_URL, EVENT_NAME)
    page.go_back()
    expect(page).to_have_url(re.compile(r".*/events$"))
    expect(page.get_by_role("heading", name="Upcoming Events")).to_be_visible()

def test_leave_booking_without_confirmation(logged_in_page: Page):
    page = logged_in_page
    event_details = EventDetailsPage(page)
    event_details.open_event(EVENT_URL, EVENT_NAME)
    booking_data = generate_booking_info(TEST_EMAIL)
    event_details.fill_booking_form(booking_data["full_name"], booking_data["email"], booking_data["phone"])
    page.get_by_test_id("nav-events").click()
    expect(page).to_have_url(f"{BASE_URL}/events")

def test_booking_persists_after_confirmation(logged_in_page: Page):
    page = logged_in_page
    event_details = EventDetailsPage(page)
    bookings_page = BookingsPage(page)
    event_details.open_event(EVENT_URL, EVENT_NAME)
    booking_data = generate_booking_info(TEST_EMAIL)
    event_details.fill_booking_form(booking_data["full_name"], booking_data["email"], booking_data["phone"])
    event_details.confirm_booking()
    event_details.view_my_bookings_link.click()
    booking = bookings_page.get_event_booking(EVENT_NAME)
    expect(booking).to_be_visible()
    expect(booking.get_by_text("confirmed")).to_be_visible()

def test_open_booking_details_from_my_bookings(logged_in_page: Page):
    page = logged_in_page
    event_details = EventDetailsPage(page)
    bookings_page = BookingsPage(page)
    event_details.open_event(EVENT_URL, EVENT_NAME)
    booking_data = generate_booking_info(TEST_EMAIL)
    event_details.fill_booking_form(booking_data["full_name"], booking_data["email"], booking_data["phone"])
    event_details.confirm_booking()
    event_details.view_my_bookings_link.click()
    bookings_page.view_booking_details(EVENT_NAME)

def test_verify_booking_details(logged_in_page: Page):
    page = logged_in_page
    event_details = EventDetailsPage(page)
    booking_page = BookingPage(page)
    bookings_page = BookingsPage(page)
    event_details.open_event(EVENT_URL, EVENT_NAME)
    booking_data = generate_booking_info(TEST_EMAIL)
    event_details.fill_booking_form(booking_data["full_name"], booking_data["email"], booking_data["phone"])
    event_details.confirm_booking()
    booking_page.verify_confirmation_details()
    event_details.view_my_bookings_link.click()
    booking = bookings_page.get_event_booking(EVENT_NAME)
    expect(booking).to_be_visible()
    expect(booking.get_by_text("confirmed")).to_be_visible()
    expect(booking.get_by_text("1 ticket")).to_be_visible()
    expect(booking.get_by_text(f"${EVENT_PRICE}")).to_be_visible()

