from src.common import auth_challenge_solver, WebDriverWait, EC, time, date_utils

def carregar_url(driver, url, timeout=10):
    driver.get(url)
    WebDriverWait(driver, timeout).until(lambda d: d.current_url == url)


def aguardar_url(driver, url, timeout=10):
    WebDriverWait(driver, timeout).until(lambda d: d.current_url == url)


def preencher_elemento(elemento, value):
    elemento.send_keys(value)


def preencher_periodo_mensal_atual(driver, selectors):
    numMes = date_utils.get_month_number()
    numAno = date_utils.get_year()
    numUltimoDia = date_utils.get_last_day_of_the_month(int(numAno), int(numMes))
        
    dataInicio = f"01/{numMes}/{numAno}"
    dataFinal = f"{numUltimoDia}/{numMes}/{numAno}"
    detectar_e_preencher_campo_data(driver, selectors["inicio"], dataInicio)
    detectar_e_preencher_campo_data(driver, selectors["final"], dataFinal)


def preencher_periodo_mensal_passado(driver, selectors):
    numMes = date_utils.get_previous_month_number()
    numAno = date_utils.get_previous_year()
    numUltimoDia = date_utils.get_last_day_of_the_month(int(numAno), int(numMes))
        
    dataInicio = f"01/{numMes}/{numAno}"
    dataFinal = f"{numUltimoDia}/{numMes}/{numAno}"
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
    iso_date = date_utils.get_iso_date(data)
    tipo_data = elemento.get_attribute("type")
    if tipo_data == "date":
        driver.execute_script(
            "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'));",
            elemento, iso_date
            )
    elif tipo_data == "text":
        driver.execute_script(
            "arguments[0].value = arguments[1]; arguments[0].dispatchEvent(new Event('change'));",
            elemento, data
            )
    

def detectar_e_aguardar_valor_em_elemento(driver, selectors, valorEsperado, timeout=120):
    inicio = time.time()
    by = selectors['by']
    value = selectors['value']
    while time.time() - inicio < timeout:
        elemento = detectar_elemento(driver, by, value)
        if elemento.text.strip() == valorEsperado:
            return
        time.sleep(5)
    raise TimeoutError(f"Erro timeout ao aguardar {valorEsperado}.")


def clicar_elemento(elemento):
    try:
        elemento.click()
        time.sleep(1)
    except Exception:
        raise


def detectar_elemento(driver, by, value, timeout=10):
    try:
        elemento = WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))
        return elemento
    except Exception:
        raise


def detectar_e_preencher_elemento(driver, selector, valor_preenchimento):
    by = selector["by"]
    value = selector["value"]
    elemento = detectar_elemento(driver, by, value)
    preencher_elemento(elemento, valor_preenchimento)


def detectar_e_clicar_elemento(driver, *args):
    try:
        if len(args) == 1:
            selector = args[0]
            by = selector["by"]
            value = selector["value"]
        if len(args) == 2:
            by = args[0]
            value = args[1]
        elemento = detectar_elemento(driver, by, value)
        clicar_elemento(elemento)
    except Exception as e:
        raise Exception(f"Error clicking element: {value}")


def detectar_e_clicar_n_elementos(driver, selectors):
    items = list(selectors.items())
    for i, (campo, info) in enumerate(items):
        by = info['by']
        value = info['value']
        detectar_e_clicar_elemento(driver, by, value)


def on_click_event(driver, selector):
    try:
        selector = selector["abrir_filtro_por_produtos_do_veiculo"]
        by = selector['by']
        value = selector['value']
        elemento = detectar_elemento(driver, by, value)
        driver.execute_script("arguments[0].click();", elemento)
        time.sleep(1)  # Aguarda o clique ser processado
    except Exception as e:
        raise Exception(f"Error on clicking element event: {value}")


def processo_de_login(driver, selectors, valuesLogin):
    items = list(selectors.items())
    for i, (campo, info) in enumerate(items):
        by = info['by']
        value = info['value']
        elemento = detectar_elemento(driver, by, value)

        if campo in valuesLogin:
            preencher_elemento(elemento, valuesLogin[campo])
        else:
            clicar_elemento(elemento)


def processo_de_login_com_reCAPTCHA(driver, selectors, valuesLogin, login_url, site_name):
    items = list(selectors.items())
    for i, (campo, info) in enumerate(items):
        by = info['by']
        value = info['value']
        elemento = detectar_elemento(driver, by, value)

        if campo in valuesLogin:
            preencher_elemento(elemento, valuesLogin[campo])
        else:
            resolver_captcha(driver, login_url, site_name)
            # time.sleep(30)


def confirmar_login(driver, selectors):
    try:
        by = selectors['by']
        value = selectors['value']
        detectar_e_clicar_elemento(driver, by, value)
    except Exception:
        pass


def resolver_captcha(driver, login_url, site_name):
    token = auth_challenge_solver.reCAPTCHA(login_url, site_name)
    driver.execute_script(f'document.getElementById("g-recaptcha-response").innerHTML = "{token}";')
    print("Captcha resolvido com sucesso!\n")


def resolver_2FA(driver, selector_botao, selecotr_2FA, site_name):
    codigo = auth_challenge_solver.twoFA(site_name)
    detectar_e_preencher_elemento(driver, selecotr_2FA, codigo)
    detectar_e_clicar_elemento(driver, selector_botao)
    