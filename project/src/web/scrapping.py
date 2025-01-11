from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from selenium.webdriver.common.by import By
import os,platform
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


if platform.machine().strip() == 'x86_64':
    file_path = os.path.abspath('../tools/chromedriver-linux64/chromedriver')
    file_path_browser = os.path.abspath('../tools/chromedriver-linux64/chrome-linux64/chrome')
else:
    file_path = os.path.abspath('../tools/chromedriver/chromedriver')

class Scrapping():

    def __init__( self, url=None):
        self.url = url
        if os.path.exists(file_path):
            if platform.machine().strip() != 'x86_64':
                display = Display(visible=0, size=(800, 600))
                display.start()
            cService = webdriver.ChromeService(executable_path=file_path)
            op = webdriver.ChromeOptions()
            if platform.machine().strip() == 'x86_64':
                op.binary_location = file_path_browser
            # op.add_argument("--headless")
            op.add_argument("--no-sandbox")
            op.add_argument("start-maximized")
            op.add_argument("disable-infobars")
            op.add_argument("--disable-extensions")
            op.add_argument("--disable-popup-blocking")
            op.add_argument("--disable-notifications")
            self.driver = webdriver.Chrome(service = cService,options=op)
            self.driver.implicitly_wait(10)

    def close ( self ):
        self.driver.close()
    
    def getData( self ):
        if self.url is not None:
            self.driver.get(self.url)
            elements = self.driver.find_elements(By.XPATH, '//div')
            d = {}
            datetime_obj = ''
            for e in elements:
                if 'Last updated' in e.text:
                    date = e.text.strip()[e.text.strip().index('Last updated'):].split('\n')[0].replace(',', '').split(' ')
                    date_string = f"{date[4]} {date[3]} {date[5]} {date[6]}:00 {date[7]}"
                    datetime_obj = datetime.datetime.strptime(date_string, '%B %d %Y %I:%M:%S %p')
                if "Gym Capacity" in e.text:
                    if datetime_obj:
                        d['timestamp'] = str(datetime_obj)
                    else:
                        d['timestamp'] =  str(datetime.datetime.now())
                    d['data'] = {}
                    temp = e.text.split('\n')
                    index = temp.index("Gym Capacity")
                    for i in range(index+2,len(temp),2):
                        d['data'][temp[i]] = temp[i+1]
                    break
            return d


if __name__ == "__main__":
    sc = Scrapping('https://activesg.gov.sg/gym-capacity')
    sc.getData()

