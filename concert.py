from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time

chrome_options = Options()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--disable-notifications")
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

driver.get("https://www.theconcert.com/")

try:
    wait = WebDriverWait(driver, 10)
    btn_buy_now = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "div.banner img._btn"))
    )
    element = wait.until(
        EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[7]/div/span/div/div[5]/div/div/div/div[3]/span"))
    )
    
    btn_buy_now.click()
    element.click()
    print("คลิกสำเร็จ!")
except Exception as e:
    print(f"เกิดข้อผิดพลาด: {e}")
finally:
    for i in range(200):
        time.sleep(1)
        print("Second", i)
    driver.quit()
