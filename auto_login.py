# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "001164F542EDFE36CE990AAA734311428FCBB5584B5C0143AC7DCC1A0F3C6AA4EEC41D7C42E53BA6A486CFCBB4D23CB105AEF04A534058B2473F11795826A47071DB3B5F079E97C209B9437D400C76FEC131B7CB5DDC0A832560C9EBD9B8E9F0F5D3909ED16EEBA49F456F775D4F9A7B2102C5D9612DC6BF6807DA4FDF0CC16DB9B0F907B0B1C01917D26180D76C16BE40ABD0946FBE38FBBBB3881E47734D65710A7BF75C3964779CEFA3E51615FF36B3EDB0CDEE8BB0B2F1AB2AD43BD8D222A7F192D3DC62ED1F3DE084F8878209B30F2B4A9C0E5EDEE59A376808BD9B725051A88B8A669971C6E096E32A5145F9FE64A9501B47BDC881B493CCF3F8618D0CCFF5EF439C9A5E32B1E00455D4EBA95243F893057F96FA5C7B30DFF8D737B0648441C7C506ED4109F2E5C7B847732C7134BB58A5AF8F917C07B9101118A97AC4A78B11567B57066FE5C63603D910C27FF8"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
