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
    browser.add_cookie({"name": "MUSIC_U", "value": "00319F750779D3C9CF047BFB4C8BFCA0F389E58A56B0F687EFADCCC85C539FE94210F30F8BEAA2419ACF51A1088FE183A1F0BA473608EFC604251F65A9A210383A5A82D817425926A2F5D784DCB1F131903623D52EB9A1EAB5D8A9F7E5E3A35043C5EEDD77C97DB1449C0F202CF7860694A8058A170A722E87BCDD96FC9FF89E8CB235D27B0F119BA7EBD568ACDFFF797265A183019CBA90C7A2EF7E44CD68219B544D2A613F3209444AAC174634B4E8C43BB7B26A33CB8BD8809E50F67C7E10D1C1A25F2C380B4D50A51A4877E4BCB88FCE0BA5D7D248518BF89270D4455B53D7BB2CE5ACDC05C70683E99DEC7B627E573F616E8ED167F864D25DADC7AEDA42563E33ACFBDC40904C1FBD6CB235905DC55E66612AE0D73C1F0EFC72629C40B64825A062C907D9ADF39BB7FA8F3470C242B42A41E391DA297875EB7990F36C83396805F7952667433E7055F0866A3B7557"})
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
