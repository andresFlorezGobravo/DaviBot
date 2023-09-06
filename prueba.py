from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time


# Para dejar el navegador abierto
options = Options()
options.add_experimental_option('detach', True)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# Se accede al sitio web
driver.get('https://mila.cobranzasbeta.com.co/')
driver.refresh()

# Se maximiza la ventana
driver.maximize_window()

# Se espera 3 segundos a que se carge el chat
time.sleep(3)
#chats = driver.find_elements("xpath", "//div[contains(@class, 'screen-content')][..//div[contains(@class, 'jsm-user-wrapper bot'][..//div[contains(@class, 'jsm-chat-box-content']")

# Se cambia el driver al iframe del chat
driver.switch_to.frame(frame_reference=driver.find_element("xpath", "//iframe[@id='iframechat']"))

# Se buscan los elementos p dentro del div con id = jsm-user-wrapper bot (Respuestas del bot)
chats = driver.find_elements("xpath", "//div[@class='jsm-user-wrapper bot']//p")

for chat in chats:
    
    print(chat.get_attribute("innerHTML"))


driver.find_element("xpath", "//div[@id='bt_id_0']").click()

driver.find_element("xpath","//input[@id='textInput']").click()

time.sleep(3)
driver.find_element("xpath","//input[@id='textInput']").send_keys('4653493')
time.sleep(3)

driver.find_element("xpath","//input[@id='textInput']").send_keys(Keys.RETURN)

time.sleep(5)

driver.find_element("xpath","//div[@id='bt_id_2']").click()

time.sleep(20)
driver.find_element("xpath","//input[@id='textInput']").send_keys('SI')
time.sleep(1)
driver.find_element("xpath","//input[@id='textInput']").send_keys(Keys.RETURN)
#driver.close()



def num_respuestas_bot(driver):
    return len(driver.find_elements("xpath", "//div[@class='jsm-user-wrapper bot']"))