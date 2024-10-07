from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import schedule
from datetime import datetime

user_data_dir = "D:/Apps/WhatsApp_User_Data" #Edit as you want

def open_whatsapp():
    options = webdriver.ChromeOptions()
    options.add_argument(f'--user-data-dir={user_data_dir}')
    options.add_argument('--profile-directory=Profile 1') 
    options.add_argument("--log-level=1")
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--no-sandbox')
    print("Ayarlar Yapıldı...")

    driver = webdriver.Chrome(options=options)
    driver.get("https://web.whatsapp.com")
    print("Entering Whatsapp Web...")
    return driver

def close_whatsapp(driver):
    driver.quit()

def send_message(group_name, message):
    try:
        driver = open_whatsapp() 
        WebDriverWait(driver, 40).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )
        
        search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
        search_box.click()
        search_box.clear()
        search_box.send_keys(group_name)
        time.sleep(3)
        print("Searching Grup/User...")
        # Grubu seç
        group = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f'//span[@title="{group_name}"]'))
        )
        group.click()
        time.sleep(2)
        
        message_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
        )
        message_box.click()
        message_box.send_keys(message)
        time.sleep(1)
        print("Sending Message...")

        send_button = driver.find_element(By.XPATH, '//button[@data-tab="11"]')
        send_button.click()
        time.sleep(2)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        close_whatsapp(driver)

user_name = "Test" # Username/Number
message_content = "Test [https://example.com]"  # Message

if __name__ == "__main__":
    send_message(user_name, message_content)
