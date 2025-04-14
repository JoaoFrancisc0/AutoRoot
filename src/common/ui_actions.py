from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

def carregar_url(driver, url, timeout=10):
    try:
        driver.get(url)
        WebDriverWait(driver, timeout).until(lambda d: d.title != "")
    except Exception as e:
        print(f"Error loading URL: {e}")
        raise
        
def detectar_elemento(driver, by, value, timeout=10):
    try:
        elemento = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
        return elemento
    except Exception as e:
        print(f"Error detecting element: {e}")
        raise

def clicar_elemento(driver, by, value, timeout=10):
    try:
        elemento = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))
        elemento.click()
    except Exception as e:
        print(f"Error clicking element: {e}")
        raise

def preencher_elemento(elemento, value):
    try:
        elemento.send_keys(value)
    except Exception as e:
        print(f"Error filling element: {e}")
        raise