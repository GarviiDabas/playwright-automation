import re
import pytest
from playwright.sync_api import Page, expect
from config import BASE_URL, TEST_PASSWORD
from pages.registration_page import RegistrationPage
from pages.login_page import LoginPage
from pages.home_page import HomePage
from pages.events_page import EventsPage
from pages.event_details_page import EventDetailsPage
from pages.booking_page import BookingPage
from pages.bookings_page import BookingsPage
from utils.test_data import (
    generate_unique_email,
    generate_booking_info,
    EVENT_NAME,
    EVENT_LOCATION,
    EVENT_PRICE,
)

def test_full_end_to_end_user_journey(page: Page):
    """
    End-to-End User Journey covering all core features:
    Phase 1: Registration Validation & Account Creation
    Phase 2: Authentication, Logout & Protected Route Security
    Phase 3: Event Discovery, Search & Metadata Verification
    Phase 4: Ticket Quantity Selection & Form Submission
    Phase 5: Booking Confirmation Details & 'My Bookings' Verification
    Phase 6: Booking Details View
    Phase 7: Session Termination
    """

    # ----------------------------------------------------
    # PHASE 1: Registration (Validation & Account Creation)
    # ----------------------------------------------------
    registration_page = RegistrationPage(page)
    registration_page.navigate()

    # Step 1a: Negative validation check - password mismatch
    registration_page.register(
        email=generate_unique_email(),
        password=TEST_PASSWORD,
        confirm_password="WrongPassword123!"
    )
    expect(page.get_by_text("match", exact=False)).to_be_visible()

    # Step 1b: Positive check - successful registration
    user_email = generate_unique_email()
    registration_page.register(email=user_email, password=TEST_PASSWORD, confirm_password=TEST_PASSWORD)
    expect(page).to_have_url(f"{BASE_URL}/", timeout=15000)

    # ----------------------------------------------------
    # PHASE 2: Authentication & Security Controls
    # ----------------------------------------------------
    home_page = HomePage(page)

    # Step 2a: Logout newly created account
    home_page.logout()
    expect(page).to_have_url(f"{BASE_URL}/login")

    # Step 2b: Protected URL security verification before login
    page.goto(f"{BASE_URL}/bookings")
    expect(page).to_have_url(f"{BASE_URL}/login")

    # Step 2c: Log back in with registered credentials
    login_page = LoginPage(page)
    login_page.login(user_email, TEST_PASSWORD)
    expect(page).to_have_url(f"{BASE_URL}/", timeout=15000)

    # ----------------------------------------------------
    # PHASE 3: Event Discovery & Search Verification
    # ----------------------------------------------------
    events_page = EventsPage(page)
    events_page.navigate()
    events_page.verify_events_page_loaded()

    # Step 3a: Search existing event
    events_page.search_event(EVENT_NAME)
    event_card = events_page.get_event_by_name(EVENT_NAME)
    expect(event_card).to_be_visible()

    # Step 3b: Verify required event information is present on card
    expect(event_card.get_by_text(EVENT_NAME)).to_be_visible()

    # ----------------------------------------------------
    # PHASE 4: Event Details & Ticket Customization
    # ----------------------------------------------------
    events_page.select_event(EVENT_NAME)
    event_details_page = EventDetailsPage(page)
    expect(page.get_by_role("heading", name=EVENT_NAME)).to_be_visible()

    # Step 4a: Increase ticket count to 2
    event_details_page.increase_ticket_count(1)
    expect(event_details_page.ticket_count_label).to_have_text("2")

    # Step 4b: Fill booking form with user details
    booking_data = generate_booking_info(user_email)
    event_details_page.fill_booking_form(
        full_name=booking_data["full_name"],
        email=booking_data["email"],
        phone=booking_data["phone"]
    )
    event_details_page.confirm_booking()

    # ----------------------------------------------------
    # PHASE 5: Booking Confirmation & 'My Bookings' Verification
    # ----------------------------------------------------
    booking_page = BookingPage(page)
    booking_page.verify_confirmation_details()

    # Navigate to My Bookings
    event_details_page.view_my_bookings_link.click()
    bookings_page = BookingsPage(page)
    bookings_page.verify_bookings_page_loaded()

    user_booking = bookings_page.get_event_booking(EVENT_NAME)
    expect(user_booking).to_be_visible()
    expect(user_booking.get_by_text("confirmed", exact=False)).to_be_visible()
    expect(user_booking.get_by_text("2 tickets", exact=False)).to_be_visible()

    # ----------------------------------------------------
    # PHASE 6: Detailed Booking View Navigation
    # ----------------------------------------------------
    bookings_page.view_booking_details(EVENT_NAME)
    expect(page).to_have_url(re.compile(r".*/bookings/\d+$"))

    # ----------------------------------------------------
    # PHASE 7: Session Termination & Back Button Protection
    # ----------------------------------------------------
    home_page.logout()
    expect(page).to_have_url(f"{BASE_URL}/login")

    # Browser back check after logout
    page.go_back()
    expect(page).to_have_url(f"{BASE_URL}/login")

