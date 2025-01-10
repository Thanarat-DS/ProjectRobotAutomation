from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\selenium_profile"

price = '฿2,500'
zone_target = 'A1'
web_target = "https://www.theconcert.com/concert/3727"

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

## เข้าเว็บ Target & เข้าเลือกที่นั่ง
driver.get(web_target)
driver.execute_script("window.scrollBy(0, 80);")

wait = WebDriverWait(driver, 10)

try:
    ticket_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="_main-body"]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div/div[2]/div[2]/button')))
    ticket_button.click()
except Exception as e:
    print(f"คลิกปุ่มเข้าซื้อไม่ได้: {e}")

## เลือกโซน
try:
    price_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[@class='btn'][contains(text(), '{price}')]")))
    price_button.click()
    print(f"clicked price: {price}")
except Exception as e:
    print(f"คลิกปุ่มราคาไม่ได้: {e}")

## เลือกราคา
try:
    time.sleep(0.2)
    zone_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.zone-item")))
    for zone_item in zone_items:
        try:
            zone_name = zone_item.find_element(By.CSS_SELECTOR, ".badge.badge-zone").text
            if zone_name == zone_target:
                zone_item.click()
                print(f"clicked zone: {zone_target}")
                break
            else:
                print(zone_name, " != ", zone_target)
        except Exception as e:
            print(f"คลิกปุ่มโซนไม่ได้: {e}, zone_name={zone_name}")
except Exception as e:
    print(f"Error: {e}")

## คลิกทุกที่นั่ง
try:
    time.sleep(0.3)
    wait_element = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "text[style*='cursor: pointer']")))
    text_elements = driver.find_elements(By.CSS_SELECTOR, "text[style*='cursor: pointer']")
    for element in text_elements:
        element.click()

        #หน่วงเวลา
        time.sleep(random.uniform(0.11, 0.15))
except Exception as e:
    print(f"error or may be it reach limit message:{e}")
finally:
    print("success")