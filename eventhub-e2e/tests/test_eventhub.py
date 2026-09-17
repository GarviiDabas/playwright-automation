import pytest
from playwright.sync_api import Page, expect
from config import BASE_URL

def test_eventhub(page: Page):
    page.goto(f"{BASE_URL}/login")
    expect(page.get_by_role("heading", name="The #1 QA Practice Hub")).to_be_visible(timeout=10000)
