#!/usr/bin/python3
import datetime
import os
import platform
import sys

from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By

if __name__ == "__main__":
    PATH = "/".join(os.path.realpath(__file__).split("/")[0:-2])
    sys.path.insert(1, PATH)
from error import error
from logger import logger

if platform.machine().strip() == "x86_64":
    DEFAULT_DRIVER_PATH = os.path.abspath("../tools/chromedriver-linux64/chromedriver")
    DEFAULT_BROWSER_PATH = os.path.abspath(
        "../tools/chromedriver-linux64/chrome-linux64/chrome"
    )
else:
    DEFAULT_DRIVER_PATH = os.path.abspath("../tools/chromedriver/chromedriver")
    DEFAULT_BROWSER_PATH = None


class Scraper:
    def __init__(
        self,
        url=None,
        file_path=DEFAULT_DRIVER_PATH,
        file_path_browser=DEFAULT_BROWSER_PATH,
    ):
        self.url = url
        self.driver = None
        self.options = None
        self.chrome_service = None
        self.display = None
        self.file_path = file_path
        self.file_path_browser = file_path_browser
        if platform.machine().strip() != "x86_64":
            self.display = Display(visible=0, size=(800, 600))
            self.display.start()

    def start_chrome_driver(self, file_path, browser_path):
        try:
            if os.path.exists(file_path):
                self.chrome_service = webdriver.ChromeService(executable_path=file_path)
                self.options = webdriver.ChromeOptions()
                if platform.machine().strip() == "x86_64":
                    self.options.binary_location = browser_path
                # op.add_argument("--headless")
                self.options.add_argument("--no-sandbox")
                self.options.add_argument("start-maximized")
                self.options.add_argument("disable-infobars")
                self.options.add_argument("--disable-extensions")
                self.options.add_argument("--disable-popup-blocking")
                self.options.add_argument("--disable-notifications")
                self.driver = webdriver.Chrome(
                    service=self.chrome_service,
                    options=self.options,
                )
                self.driver.implicitly_wait(10)
        except Exception as e:
            logger.logger.error(e)
            raise error.ScrapingError(
                "Driver Error!", error.ErrorCode.DRIVER_ERROR.value
            )

    def close(self):
        self.driver.close()

    def get_data(self):
        result = {}
        try:
            self.start_chrome_driver(self.file_path, self.file_path_browser)
            if self.url is not None and self.driver is not None:
                self.driver.get(self.url)
                elements = self.driver.find_elements(By.XPATH, "//div")
                datetime_obj = ""
                for e in elements:
                    if "Last updated" in e.text:
                        date = (
                            e.text.strip()[e.text.strip().index("Last updated") :]
                            .split("\n")[0]
                            .replace(",", "")
                            .split(" ")
                        )
                        date_string = (
                            f"{date[4]} {date[3]} {date[5]} {date[6]}:00 {date[7]}"
                        )
                        datetime_obj = datetime.datetime.strptime(
                            date_string, "%B %d %Y %I:%M:%S %p"
                        )
                    if "Gym Capacity" in e.text:
                        if datetime_obj:
                            result["timestamp"] = str(datetime_obj)
                        else:
                            result["timestamp"] = str(datetime.datetime.now())
                        result["data"] = {}
                        temp = e.text.split("\n")
                        index = temp.index("Gym Capacity")
                        for i in range(index + 2, len(temp), 2):
                            result["data"][i] = {}
                            result["data"][i]["name"] = temp[i]
                            replacements = ["ActiveSG", "@", "Gym", "CC", "Square"]
                            gym_area = temp[i]
                            for replacement in replacements:
                                gym_area = gym_area.replace(replacement, "")
                            gym_area = gym_area.strip()
                            result["data"][i]["area"] = gym_area
                            result["data"][i]["capacity"] = temp[i + 1]
                        break
                self.driver.quit()

        except Exception as e:
            self.driver.close()
            self.start_chrome_driver(self.file_path, self.file_path_browser)
            logger.logger.error(e)
        finally:
            return result


Scrapping = Scraper


if __name__ == "__main__":
    sc = Scraper("https://activesg.gov.sg/gym-capacity")
    sc.get_data()
