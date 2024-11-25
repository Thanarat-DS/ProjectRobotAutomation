from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from selenium_stealth import stealth
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import time
import random

# "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\selenium_profile"

price = '฿4,500'

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

driver.get("https://www.theconcert.com/")
time.sleep(1)
window_size = driver.get_window_size()

#สุ่มค่าเพื่อไม่ให้คลิกซ้ำที่เดิม
middle_y_factor = random.uniform(1.5, 3)
near_right_x_offset = random.randint(30, 80)

middle_y = window_size['height'] // middle_y_factor
near_right_x = window_size['width'] - near_right_x_offset

action = ActionChains(driver)
action.move_by_offset(near_right_x, middle_y).click().perform()
time.sleep(0.5)

try:
    wait = WebDriverWait(driver, 10)

    # element = WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'เข้าสู่ระบบ')]")) or
    #     EC.presence_of_element_located((By.XPATH, "//button[contains(@class, 'login-btn')]")) or 
    #     EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'login')]"))
    # )
    
    # element.click()
    driver.get("https://www.theconcert.com/concert/3584")

    driver.execute_script("window.scrollBy(0, 80);")

    ticket_button = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="_main-body"]/div/div[1]/div[1]/div[2]/div[2]/div[2]/div/div[2]/div[2]/button')))
    ticket_button.click()

    price_button = wait.until(EC.element_to_be_clickable((By.XPATH, f"//a[@class='btn'][contains(text(), '{price}')]")))
    price_button.click()

    zone_items = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.zone-item")))
    for zone_item in zone_items:
        try:
            # Check if sold out text exists
            sold_out = zone_item.find_elements(By.CLASS_NAME, "sold-out-text")
            if not sold_out:  # If no sold out text found
                zone_item.click()
                break
        except Exception as e:
            continue

    # หาทุก tspan tag ที่มีในหน้าเว็บ
    try:
        tspan_elements = wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, "tspan")))
        if tspan_elements:
            # คลิกที่ tspan tag แรกที่เจอ
            tspan_elements[0].click()
        else:
            print("ไม่พบ tspan tag ในหน้าเว็บ")
    except Exception as e:
        print(f"เกิดข้อผิดพลาดเลือกที่นั่ง: {e}")

    time.sleep(1.5)
    target_x = int(window_size['width'] * 0.15)  # 15% ของความกว้างหน้าจอ
    target_y = int(window_size['height'] * 0.95)  # 95% ของความสูงหน้าจอ
    
    actions = ActionChains(driver)
    actions.move_by_offset(target_x, target_y).click().perform()

    print("คลิกปุ่มซื้อบัตรสำเร็จ")

except Exception as e:
    print(f"เกิดข้อผิดพลาด: {e}")
finally:
    for i in range(200):
        time.sleep(1)
    driver.quit()
