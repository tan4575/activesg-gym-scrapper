import datetime
from unittest.mock import MagicMock

import pytest
from error import error
from web.scrapping import Scraper


class FakeElement:
    def __init__(self, text):
        self.text = text


class FakeDriver:
    def __init__(self, elements=None):
        self.elements = elements or []
        self.closed = False
        self.quit_called = False
        self.visited_url = None

    def get(self, url):
        self.visited_url = url

    def find_elements(self, by, value):
        return self.elements

    def implicitly_wait(self, seconds):
        self.wait_seconds = seconds

    def close(self):
        self.closed = True

    def quit(self):
        self.quit_called = True


def test_get_data_parses_gym_capacity(monkeypatch):
    text = (
        "Last updated, on 24 June 2026 1:05 PM\n"
        "Gym Capacity\n"
        "header\n"
        "ActiveSG Bishan Gym\n"
        "45%\n"
        "ActiveSG Toa Payoh Gym\n"
        "Closed"
    )
    driver = FakeDriver([FakeElement(text)])
    scraper = Scraper("https://example.test")
    scraper.start_chrome_driver = MagicMock(
        side_effect=lambda *args: setattr(scraper, "driver", driver)
    )

    result = scraper.get_data()

    scraper.start_chrome_driver.assert_called_once_with(
        scraper.file_path,
        scraper.file_path_browser,
    )
    assert driver.visited_url == "https://example.test"
    assert driver.quit_called is True
    assert result["timestamp"] == str(
        datetime.datetime.strptime("June 24 2026 1:05:00 PM", "%B %d %Y %I:%M:%S %p")
    )
    assert result["data"][3] == {
        "name": "ActiveSG Bishan Gym",
        "area": "Bishan",
        "capacity": "45%",
    }
    assert result["data"][5]["capacity"] == "Closed"


def test_start_chrome_driver_raises_scraping_error_for_driver_failure(monkeypatch):
    scraper = Scraper()
    monkeypatch.setattr("web.scrapping.os.path.exists", lambda path: True)

    def raise_driver_error(*args, **kwargs):
        raise RuntimeError("driver failed")

    monkeypatch.setattr("web.scrapping.webdriver.Chrome", raise_driver_error)

    with pytest.raises(error.ScrapingError):
        scraper.start_chrome_driver("driver", "browser")


def test_close_closes_driver():
    driver = FakeDriver()
    scraper = Scraper()
    scraper.driver = driver

    scraper.close()

    assert driver.closed is True
