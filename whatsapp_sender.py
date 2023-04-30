from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time

class InvalidPhoneNumberException(Exception):
    pass

class InvalidDictionary(Exception):
    pass

class WhatsappDaemon():
    def __init__(self,chrome_exe_path,chrome_profile_path,chrome_driver_path):
        self.chrome_exe_path = chrome_exe_path
        self.chrome_profile_path = chrome_profile_path
        self.chrome_driver_path = chrome_driver_path
        self.user_agent = r"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        self.xpath = r"/html/body/div[1]/div/div/div[5]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div[1]/p"
        self.delay_after_enter = 2
    
    def send_message(self, text={}, timeout=60):
        try:
            URL = []
            if not text or type(text) != dict:
                raise InvalidDictionary(f"Invalid dictionary passed {text}")
            else:
                for phone_number, message in text.items():
                    if len(phone_number) != 12:
                        raise InvalidPhoneNumberException(f"Invalid number passed {phone_number}")
                    else:
                        URL.append(f"https://web.whatsapp.com/send?phone={phone_number}&text={message}&app_absent=1")
                    
            chrome_options = Options()
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--remote-debugging-port=9222')
            chrome_options.add_argument('--disable-dev-shm-usage')
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--window-size=1920,1080")
            chrome_options.add_argument("start-maximized")
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument(f"user-data-dir={self.chrome_profile_path}")
            chrome_options.add_argument(f"user-agent={self.user_agent}")
            chrome_options.add_argument('--disable-software-rasterizer')
            chrome_options.binary_location=self.chrome_exe_path
            service = Service(self.chrome_driver_path)
            browser = webdriver.Chrome(service=service,options=chrome_options)

            for url in URL:
                try:
                    browser.get(url)
                except Exception as err:
                    print(err)
                    return None
                try:
                    WebDriverWait(browser, timeout).until(EC.element_to_be_clickable((By.XPATH, self.xpath)))
                except TimeoutException:
                    print("Probably WhatsApp not logged in already in chrome browser. Timed out while waiting for WhatsApp to load, try increasing timeout")
                    return None
                
                try:
                    browser.find_element(By.XPATH, self.xpath).send_keys(Keys.RETURN)
                except NoSuchElementException:
                    print("Unable to find the element for entering the text, please contact the developer")
                    return None
                
                time.sleep(self.delay_after_enter)

            browser.quit()

            return True
        
        except Exception as err:
            print(err)
            return None







