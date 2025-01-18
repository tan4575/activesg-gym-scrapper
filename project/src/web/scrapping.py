from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from pyvirtualdisplay import Display
from selenium.webdriver.common.by import By
import os,platform,sys
import datetime
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

if __name__ == "__main__":
    PATH = "/".join(os.path.realpath(__file__).split("/")[0:-2])
    sys.path.insert(1,PATH)
from logger import logger
from error import error

if platform.machine().strip() == 'x86_64':
    file_path = os.path.abspath('../tools/chromedriver-linux64/chromedriver')
    file_path_browser = os.path.abspath('../tools/chromedriver-linux64/chrome-linux64/chrome')
else:
    file_path = os.path.abspath('../tools/chromedriver/chromedriver')

class Scrapping():

    def __init__( self, url=None):
        self.url = url
        self.driver = None
        try:
            if os.path.exists(file_path):
                if platform.machine().strip() != 'x86_64':
                    display = Display(visible=0, size=(800, 600))
                    display.start()
                self.cService = webdriver.ChromeService(executable_path=file_path)
                self.op = webdriver.ChromeOptions()
                if platform.machine().strip() == 'x86_64':
                    self.op.binary_location = file_path_browser
                # op.add_argument("--headless")
                self.op.add_argument("--no-sandbox")
                self.op.add_argument("start-maximized")
                self.op.add_argument("disable-infobars")
                self.op.add_argument("--disable-extensions")
                self.op.add_argument("--disable-popup-blocking")
                self.op.add_argument("--disable-notifications")
                self.driver = webdriver.Chrome(service = self.cService,options=self.op)
                self.driver.implicitly_wait(10)
        except Exception as e:
            logger.logger.error(e)
            raise error.ScrappingException("Driver Error!", error.ERROR_CODE.DRIVER_ERROR.value)


    def close ( self ):
        self.driver.close()
    
    def getData( self ):
        d = {}
        try:
            if self.url is not None and self.driver is not None:
                self.driver.get(self.url)
                elements = self.driver.find_elements(By.XPATH, '//div')
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
                            d['data'][i] = {}
                            d['data'][i]['name'] = temp[i]
                            replace = ['ActiveSG','@','Gym','CC', 'Square']
                            GYMarea = temp[i]
                            for r in replace:
                                GYMarea = GYMarea.replace(r, '')
                            GYMarea = GYMarea.strip()
                            d['data'][i]['area'] = GYMarea
                            d['data'][i]['capacity'] = temp[i+1]
                        break
        except Exception as e:
            self.driver.close()
            self.driver = webdriver.Chrome(service = self.cService,options=self.op)
            self.driver.implicitly_wait(10)
            logger.logger.error(e)
        finally:
            return d


if __name__ == "__main__":
    sc = Scrapping('https://activesg.gov.sg/gym-capacity')
    sc.getData()

