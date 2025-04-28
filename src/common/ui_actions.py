from common import WebDriverWait, EC, time, date_utils


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


def preencher_periodo_mensal_atual(driver, selectors):
    numMes = date_utils.get_month_number()
    numAno = date_utils.get_year()
        
    dataInicio = f"01/{numMes}/{numAno}"
    dataFinal = f"31/{numMes}/{numAno}"
    detectar_e_preencher_campo_data(driver, selectors["inicio"], dataInicio)
    detectar_e_preencher_campo_data(driver, selectors["final"], dataFinal)


def preencher_periodo_mensal_passado(driver, selectors):
    numMes = date_utils.get_previous_month_number()
    numAno = date_utils.get_previous_year()
        
    dataInicio = f"01/{numMes}/{numAno}"
    dataFinal = f"31/{numMes}/{numAno}"
    detectar_e_preencher_campo_data(driver, selectors["inicio"], dataInicio)
    detectar_e_preencher_campo_data(driver, selectors["final"], dataFinal)    


def preencher_periodo_semanal(driver, selectors):
    numDia = date_utils.get_day()
    numMes = date_utils.get_month_number()
    numAno = date_utils.get_year()

    dataInicio = date_utils.get_last_friday()
    dataFinal = f"{numDia}/{numMes}/{numAno}"
    detectar_e_preencher_campo_data(driver, selectors["inicio"], dataInicio)
    detectar_e_preencher_campo_data(driver, selectors["final"], dataFinal)    


def detectar_e_preencher_campo_data(driver, selectors, data):
    by = selectors['by']
    value = selectors['value']
    elemento = detectar_elemento(driver, by, value)
    driver.execute_script(
        "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'));",
        elemento, data
        )
    

def detectar_e_aguardar_valor_em_elemento(driver, selectors, valorEsperado, timeout=60):
    try:
        inicio = time.time()
        by = selectors['by']
        value = selectors['value']
        while time.time() - inicio < timeout:
            elemento = detectar_elemento(driver, by, value)
            if elemento.text.strip() == valorEsperado:
                return
            time.sleep(5)
    except Exception as e:
        print(f"Error detecting element: {e}")
        raise


def clicar_elemento(elemento):
    try:
        elemento.click()
        time.sleep(1)
    except Exception as e:
        print(f"Error clicking element: {e}")
        raise


def detectar_elemento(driver, by, value, timeout=10):
    try:
        elemento = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
        return elemento
    except Exception as e:
        print(f"Error detecting element: {e}")
        raise


def detectar_e_clicar_elemento(driver, by, value):
    try:
        print(by, value)
        elemento = detectar_elemento(driver, by, value)
        clicar_elemento(elemento)
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
            detectar_e_clicar_elemento(driver, by, value)
    except Exception as e:
        print(f"Error detecting or cliking an element: {e}")
        raise


def processo_de_login(driver, selectors, valuesLogin):
    try:
        items = list(selectors.items())
        for i, (campo, info) in enumerate(items):
            by = info['by']
            value = info['value']
            elemento = detectar_elemento(driver, by, value)

            if campo in valuesLogin:
                preencher_elemento(elemento, valuesLogin[campo])
            else:
                clicar_elemento(elemento)
    except Exception as e:
        print(f"Error in loging: {e}")
        raise


def processo_de_login_com_reCAPTCHA(driver, selectors, valuesLogin):
    try:
        items = list(selectors.items())
        for i, (campo, info) in enumerate(items):
            by = info['by']
            value = info['value']
            elemento = detectar_elemento(driver, by, value)

            if campo in valuesLogin:
                preencher_elemento(elemento, valuesLogin[campo])
            else:
                resolver_reCAPTCHA()
                clicar_elemento(elemento)
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


def resolver_reCAPTCHA():
    time.sleep(30)
