import pytest
from playwright.sync_api import Page, expect
from config import BASE_URL, TEST_EMAIL, TEST_PASSWORD
from pages.login_page import LoginPage
from utils.logger import get_logger

logger = get_logger("Conftest")

@pytest.fixture
def logged_in_page(page: Page) -> Page:
    logger.info("Setting up logged_in_page fixture for user: %s", TEST_EMAIL)
    login_page = LoginPage(page)
    login_page.navigate()
    login_page.login(TEST_EMAIL, TEST_PASSWORD)
    expect(page).to_have_url(f"{BASE_URL}/")
    return page


def pytest_runtest_setup(item):
    logger.info(">>> STARTING TEST: %s", item.name)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call":
        if report.passed:
            logger.info("<<< PASSED TEST: %s", item.name)
        elif report.failed:
            logger.error("<<< FAILED TEST: %s - %s", item.name, report.longreprtext)
            page = item.funcargs.get("page")
            if page:
                try:
                    screenshot_bytes = page.screenshot(type="png")
                    pytest_html = item.config.pluginmanager.getplugin("html")
                    if pytest_html:
                        extra = getattr(report, "extra", [])
                        extra.append(pytest_html.extras.image(screenshot_bytes, "Failure Screenshot"))
                        report.extra = extra
                except Exception as e:
                    logger.error("Failed to capture screenshot for HTML report: %s", e)
        elif report.skipped:
            logger.warning("<<< SKIPPED TEST: %s", item.name)


