from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import schedule
from datetime import datetime

user_data_dir = "D:/Apps/WhatsApp_User_Data"

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
    print("WhatsApp Web'e giriş Yapılıyor...")
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
        print("Grup Aranıyor...")
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
        print("Ders Bildirimi Gönderiliyor...")

        send_button = driver.find_element(By.XPATH, '//button[@data-tab="11"]')
        send_button.click()
        time.sleep(2)

    except Exception as e:
        print(f"Hata oluştu: {e}")
    finally:
        close_whatsapp(driver)

schedule_list = [
    {"day": "Monday", "time": "16:00", "group": "Ders Bildirimi", "message": "Ders Başlıyor! Grafik-Animasyon. Katılmayı Unutmayın! [https://debsis.firat.edu.tr/course/view.php?id=192620] "},
    {"day": "Monday", "time": "19:00", "group": "Ders Bildirimi", "message": "Ders Başlıyor! Ofis Yazılımları. Katılmayı Unutmayın! [https://debsis.firat.edu.tr/course/view.php?id=192632] "},
    {"day": "Tuesday", "time": "15:00", "group": "Ders Bildirimi", "message": "Ders Başlıyor! İngilizce. Katılmayı Unutmayın! [https://debsis.firat.edu.tr/course/view.php?id=206591] "},
    {"day": "Tuesday", "time": "17:00", "group": "Ders Bildirimi", "message": "Ders Başlıyor! Türk Dili. Katılmayı Unutmayın! [https://debsis.firat.edu.tr/course/view.php?id=205829] "},
    {"day": "Tuesday", "time": "19:00", "group": "Ders Bildirimi", "message": "Ders Başlıyor! Web Tasarım. Katılmayı Unutmayın! [https://debsis.firat.edu.tr/course/view.php?id=192614] "},
    {"day": "Wednesday", "time": "17:00", "group": "Ders Bildirimi", "message": "Ders Başlıyor! Atatürk İnkılapları. Katılmayı Unutmayın! [https://debsis.firat.edu.tr/course/view.php?id=191906] "},
    {"day": "Wednesday", "time": "19:00", "group": "Ders Bildirimi", "message": "Ders Başlıyor! Programlamanın Temelleri. Katılmayı Unutmayın! [https://debsis.firat.edu.tr/course/view.php?id=192608] "},
    {"day": "Thursday", "time": "15:00", "group": "Ders Bildirimi", "message": "Ders Başlıyor! Yazılım Kurulumu. Katılmayı Unutmayın! [https://debsis.firat.edu.tr/course/view.php?id=192626] "},
    {"day": "Thursday", "time": "18:00", "group": "Ders Bildirimi", "message": "Ders Başlıyor! Matematik. Katılmayı Unutmayın! [https://debsis.firat.edu.tr/course/view.php?id=199724] "},
]

for lesson in schedule_list:
    if lesson["day"] == "Monday":
        schedule.every().monday.at(lesson["time"]).do(send_message, lesson["group"], lesson["message"])
    elif lesson["day"] == "Tuesday":
        schedule.every().tuesday.at(lesson["time"]).do(send_message, lesson["group"], lesson["message"])
    elif lesson["day"] == "Wednesday":
        schedule.every().wednesday.at(lesson["time"]).do(send_message, lesson["group"], lesson["message"])
    elif lesson["day"] == "Thursday":
        schedule.every().thursday.at(lesson["time"]).do(send_message, lesson["group"], lesson["message"])


while True:
    schedule.run_pending()
    now = datetime.now().strftime("%H:%M")
    print(f"Saat: {now} | İşlem bekleniyor...")
    time.sleep(60)
