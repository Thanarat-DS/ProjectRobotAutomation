from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium_stealth import stealth
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

driver.get("https://bot.sannysoft.com/")

wait = WebDriverWait(driver, 10)

for i in range(200):
    time.sleep(1)
    print("Second: ", i)

driver.quit()
