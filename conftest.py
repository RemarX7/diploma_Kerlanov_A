import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from api.schedule_api import ScheduleAPI


@pytest.fixture
def driver():
    """Фикстура для WebDriver."""
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()


@pytest.fixture
def api():
    """Фикстура для API клиента."""
    return ScheduleAPI()


def pytest_configure(config):
    config.addinivalue_line("markers", "api: API тесты")
    config.addinivalue_line("markers", "ui: UI тесты")
