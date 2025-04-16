from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def carregar_url(driver, url, timeout=10):
    try:
        driver.get(url)
        WebDriverWait(driver, timeout).until(lambda d: d.current_url == url)
    except Exception as e:
        print(f"Error loading URL: {e}")
        raise

def aguardar_url(driver, url, timeout=10):
    try:
        WebDriverWait(driver, timeout).until(lambda d: d.current_url == url)
    except Exception as e:
        print(f"Error to load URL: {e}")
        raise


def preencher_elemento(elemento, value):
    try:
        elemento.send_keys(value)
    except Exception as e:
        print(f"Error filling element: {e}")
        raise
        

def detectar_elemento(driver, by, value, timeout=10):
    try:
        elemento = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
        return elemento
    except Exception as e:
        print(f"Error detecting element: {e}")
        raise


def clicar_elemento(elemento):
    try:
        elemento.click()
    except Exception as e:
        print(f"Error clicking element: {e}")
        raise


def detectar_e_clicar_elemento(driver, by, value, timeout=10):
    try:
        elemento = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))
        elemento.click()
    except Exception as e:
        print(f"Error clicking element: {e}")
        raise


def detectar_e_clicar_n_elementos(driver, selectors):
    try:
        items = list(selectors.items())
        for i, (campo, info) in enumerate(items):
            by = info['by']
            value = info['value']
            print(by, value)
            time.sleep(10)
            detectar_e_clicar_elemento(driver, by, value)
    except Exception as e:
        print(f"Error in detecting or cliking an element: {e}")
        raise


def processo_de_login(driver, selectors, valuesLogin):
    try:
        items = list(selectors.items())
        for i, (campo, info) in enumerate(items):
            by = info['by']
            value = info['value']
            elemento = detectar_elemento(driver, by, value)

            if i == len(items) - 1:  # último item
                clicar_elemento(elemento)
            else:
                preencher_elemento(elemento, valuesLogin[i])
    except Exception as e:
        print(f"Error in loging: {e}")
        raise


def confirmar_login(driver, selectors):
    try:
        by = selectors['by']
        value = selectors['value']
        detectar_e_clicar_elemento(driver, by, value)
    except:
        # Confirmação não necessária
        pass
