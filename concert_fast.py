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

price = '฿6,940'
zone_target = ['A2','C3','D1', 'D2']
web_target = "https://www.theconcert.com/concert/3775"

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

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

def open_target_website(url):
    driver.get(url)
    driver.execute_script("window.scrollBy(0, 80);")

def enter_ticket_page(wait):
    try:
        time.sleep(0.1)
        print("Finding Enter Button...")

        ticket_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="_main-body"]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div/div[2]/div[2]/button')))
        ticket_button.click()
        print("enter ticket page")
    except Exception as e:
        print(f"Cannot click ticket button: {e}")

def select_price(wait, price):
    try:
        time.sleep(0.1)
        print("Finding target price...")

        price_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[@class='btn'][contains(text(), '{price}')]")))
        price_button.click()
        print(f"Clicked price: {price}")
    except Exception as e:
        print(f"Cannot click price button: {e}")

def select_zone(wait, zone_target):
    try:
        time.sleep(0.1)
        print("Finding target zone...")
        zone_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.zone-item")))
        for zone_item in zone_items:
            try:
                zone_name = zone_item.find_element(By.CSS_SELECTOR, ".badge.badge-zone").text
                if zone_name in zone_target:
                    wait_zone_item = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.zone-item")))
                    zone_item.click()
                    print(f"Clicked zone: {zone_target}")
                    break
                else:
                    print(zone_name, " != ", zone_target)
            except Exception as e:
                print(f"Cannot click zone: {e}, zone_name={zone_name}")
    except Exception as e:
        print(f"Error: {e}")

def click_all_seats(driver, wait):
    try:
        time.sleep(0.2)
        wait_element = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "text[style*='cursor: pointer']")))
        text_elements = driver.find_elements(By.CSS_SELECTOR, "text[style*='cursor: pointer']")
        for element in text_elements:
            element.click()
            time.sleep(random.uniform(0.3, 0.4))
    except Exception as e:
        print(f"Error or limit reached: {e}")
    finally:
        print("Success")

if __name__ == "__main__":
    wait = WebDriverWait(driver, 10)

    open_target_website(web_target)
    enter_ticket_page(wait)
    select_price(wait, price)
    select_zone(wait, zone_target)
    click_all_seats(driver, wait)

    driver.quit()

    # for _ in range(1000):
    #     text = int(input("Select Task: \n1: open web\n2: enter ticket page\n3: select price\n4: select zone\n5: click all seats\n6: exit\n"))
    #     match text:
    #         case 1:
    #             open_target_website(driver, web_target)
    #         case 2:
    #             enter_ticket_page(driver, wait)
    #         case 3:
    #             select_price(driver, wait, price)
    #         case 4:
    #             select_zone(driver, wait, zone_target)
    #         case 5:
    #             click_all_seats(driver, wait)
    #         case 6:
    #             driver.quit()
    #             break