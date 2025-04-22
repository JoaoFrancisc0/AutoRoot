from src.common import ui_actions, file_handler, google_drive


def login_sga(driver, login_url, home_url, selectors, values):
    ui_actions.carregar_url(driver, login_url)
    ui_actions.confirmar_login(driver, selectors["confirmacao"])
    ui_actions.processo_de_login_com_reCAPTCHA(driver, selectors["login"], values)
    ui_actions.aguardar_url(driver, home_url)


def coleta_mensal(service, driver, selectors, url, folder_id, tipo):
    folder_id = folder_id["boleto_fechamento_folder_id"]
    ui_actions.carregar_url(driver, url)
    ui_actions.preencher_periodo_mensal_passado(driver, selectors["periodo"])
    ui_actions.detectar_e_clicar_n_elementos(driver, selectors["atributos"])
    caminho_arquivo = file_handler.wait_download(tipo)
    caminho_arquivo = file_handler.convert_file(caminho_arquivo)
    caminho_arquivo = file_handler.rename_file_previous_month(caminho_arquivo, tipo)
    google_drive.upload_report(service, caminho_arquivo, folder_id)
    file_handler.remove_file(caminho_arquivo)


def coleta_sga(service, driver, selectors, configs):
    url = configs["url"]
    values = configs["credenciais"]
    folder_id = configs["folder_id"]
    login_sga(driver, url["login_url"], url["home_url"], selectors, values)
    coleta_mensal(service, driver, selectors, url["boleto_url"], folder_id, tipo="boleto_fechamento")
