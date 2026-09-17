import pytest
from playwright.sync_api import Page, expect
from constants import LOGIN_URL

def test_eventhub(page: Page):
    page.goto(LOGIN_URL)
    expect(page.get_by_role("heading", name="The #1 QA Practice Hub")).to_be_visible(timeout=10000)
