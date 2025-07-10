import os
import platform
import time

from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def chrome_options():
    options = ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")


DRIVER_MAPPING = {
    "Chrome": {
        "service": ChromeService,
        "options": chrome_options,
        "system": {
            "Darwin": {
                "arm64": "chromedriver-mac-arm",
                "x86": ""
            },
            "Linux": {
                "aarch64": "chromedriver-linux",
                "x86_64": "",
            }
        }
    },
}

def get_driver(browser="Chrome"):
    os_name = platform.system()
    arch = platform.machine()
    
    driver_name = DRIVER_MAPPING[browser]['system'][os_name][arch]
    driver_path = os.path.join('drivers', driver_name)
    driver = getattr(webdriver, browser)
    kwargs = {
        "executable_path": driver_path
    }
    if DRIVER_MAPPING[browser].get('options'):
        options = DRIVER_MAPPING[browser]['options']()
        kwargs['options'] = options
    service = DRIVER_MAPPING[browser]['service'](**kwargs)
    
    return driver(service=service)



def main():
    url = "https://www.wegmans.com/"
    coupon_url = "https://www.wegmans.com/shop/coupons"
    
    username = os.environ.get('username')
    password = os.environ.get('password')
    
    driver = get_driver()
    driver.get(url)
    # wait for page to load
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//span[text()='Sign In / Register']"))
    )
    # find and click sign in button
    driver.find_element(By.XPATH, "//span[text()='Sign In / Register']").click()
    # wait for auth page to load
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "signInName"))
    )
    # enter credentials and submit
    driver.find_element(By.ID, "signInName").send_keys(username)
    driver.find_element(By.ID, "password").send_keys(password)
    driver.find_element(By.ID, "next").click()
    # wait for page to load again
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//nav"))
    )
    # navigate to coupon page
    driver.get(coupon_url)
    # wait for page to load
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//label[text()='Clipped']"))
    )
    # get list of buttons and loop to click
    buttons = driver.find_elements(By.CLASS_NAME, "clip-button")
    for button in buttons:
        button.click()
        time.sleep(0.5)
    
    time.sleep(10)



if __name__ == "__main__":
    load_dotenv()
    main()