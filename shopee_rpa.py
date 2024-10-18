from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from selenium_stealth import stealth
import os
import time
import random

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\selenium_profile"


def random_sleep():
    time.sleep(random.uniform(2, 5))

load_dotenv()
username_env = os.getenv('SHOPEE_USERNAME')
password_env = os.getenv('SHOPEE_PASSWORD')

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-notifications")
chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36")


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
driver.execute_script("window.navigator.chrome = { runtime: {} };")
driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});")
driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});")

# Selenium Stealth settings
stealth(driver,
      languages=["en-US", "en"],
      vendor="Google Inc.",
      platform="Win32",
      webgl_vendor="Intel Inc.",
      renderer="Intel Iris OpenGL Engine",
      fix_hairline=True,
  )

driver.get("https://bot.sannysoft.com/")
time.sleep(50)
random_sleep()
driver.get("https://shopee.co.th")
print("start shopee")
time.sleep(5)
random_sleep()
driver.get("https://shopee.co.th/user/notifications/order")
print("start menu")

wait = WebDriverWait(driver, 10)

def select_language():
    try:
        thai_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'ไทย')]")))
        thai_button.click()

        print("Success Select Thai Language Button")
        time.sleep(1)
    except Exception as e:
        print(f"Error during language selection: {e}")

def login_shopee():
    try:
        username = wait.until(EC.visibility_of_element_located((By.NAME, "loginKey")))
        password = wait.until(EC.visibility_of_element_located((By.NAME, "password")))

        username.send_keys(username_env)
        password.send_keys(password_env)

        login_submit = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'เข้าสู่ระบบ')]")))
        login_submit.click()
        
        print(f"Success login")
        time.sleep(30)
    except Exception as e:
        print(f"Error during login: {e}")

def search_product(product_name):
    try:
        search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@placeholder='ค้นหาสินค้า']")))
        search_box.send_keys(product_name)
        search_box.send_keys(Keys.RETURN)

        time.sleep(3)
    except Exception as e:
        print(f"Error during search: {e}")

def add_to_cart():
    try:
        first_product = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.shopee-search-item-result__item")))
        first_product.click()

        driver.switch_to.window(driver.window_handles[1])

        add_to_cart_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn--l.btn--primary.btn--rounded")))
        add_to_cart_button.click()

        time.sleep(3)
    except Exception as e:
        print(f"Error during add to cart: {e}")

def checkout():
    try:
        cart_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href='/cart']")))
        cart_button.click()

        checkout_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.btn--l.btn--primary.btn--rounded")))
        checkout_button.click()

        time.sleep(3)
    except Exception as e:
        print(f"Error during checkout: {e}")



# select_language()
# login_shopee()
# search_product("ชื่อสินค้าที่ต้องการค้นหา")
# add_to_cart()
# checkout()

time.sleep(200)
driver.quit()
