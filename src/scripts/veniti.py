from src.common import ui_actions


def login_veniti(driver, login_url, home_url, selectors, values):
    ui_actions.carregar_url(driver, login_url)
    ui_actions.processo_de_login(driver, selectors["login"], values)
    ui_actions.confirmar_login(driver, selectors["confirmacao"])
    ui_actions.aguardar_url(driver, home_url)


def coleta_atendimentos(service, driver, selectors, url, folder_id, tipo):
    ui_actions.carregar_url(driver, url)
    ui_actions.detectar_e_clicar_n_elementos(driver, selectors["busca"])
    ui_actions.preencher_periodo_mensal_atual(driver, selectors["periodo"])
    ui_actions.detectar_e_clicar_n_elementos(driver, selectors["atributos"])


def coleta_veniti(service, driver, selectors, configs):
    url = configs["url"]
    values = configs["credenciais"]
    folder_id = configs["folder_id"]    
    login_veniti(driver, url["login_url"], url["home_url"], selectors, values)
    coleta_atendimentos(service, driver, selectors, url["atendimento_url"], folder_id, tipo="atendimentos")
