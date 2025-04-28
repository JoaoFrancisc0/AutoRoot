from src.common import ui_actions, file_handler, google_drive, date_utils
from app import scheduler


def login_veniti(driver, login_url, home_url, selectors, values):
    ui_actions.carregar_url(driver, login_url)
    ui_actions.processo_de_login(driver, selectors["login"], values)
    ui_actions.confirmar_login(driver, selectors["confirmacao"])
    ui_actions.aguardar_url(driver, home_url)


def coleta_atendimentos(service, driver, selectors, url, folder_id, tipo):
    ui_actions.carregar_url(driver, url)
    ui_actions.detectar_e_clicar_n_elementos(driver, selectors["busca"])
    if date_utils.get_day() == 1:
        ui_actions.preencher_periodo_mensal_passado(driver, selectors["periodo"])
    else:
        ui_actions.preencher_periodo_mensal_atual(driver, selectors["periodo"])
    ui_actions.detectar_e_clicar_n_elementos(driver, selectors["atributos"])
    ui_actions.detectar_e_aguardar_valor_em_elemento(driver, selectors["download"]["status"], "EXPORTADO")
    ui_actions.detectar_e_clicar_elemento(driver, selectors["download"]["download"])
    if date_utils.get_day() == 1:
        envio_mensal_passado(service, folder_id, tipo)
    else:
        envio_mensal_atual(service, folder_id, tipo)


def coleta_conjuntura(service, driver, selectors, url, folder_id, tipo):
    ui_actions.carregar_url(driver, url)
    print(url)
    print("teste1")
    ui_actions.detectar_e_clicar_elemento(driver, selectors["busca"])
    print("teste2")
    if date_utils.get_day() == 1:
        ui_actions.preencher_periodo_mensal_passado(driver, selectors["periodo"])
    else:
        ui_actions.preencher_periodo_mensal_atual(driver, selectors["periodo"])
    print("teste3")
    ui_actions.detectar_e_clicar_n_elementos(driver, selectors["atributos"])
    print("teste4")
    if date_utils.get_day() == 1:
        envio_mensal_passado(service, folder_id, tipo)
    else:
        envio_mensal_atual(service, folder_id, tipo)

def envio_mensal_passado(service, folder_id, tipo):
    caminho_arquivo = file_handler.wait_download(tipo)
    caminho_arquivo = file_handler.rename_file_previous_month(caminho_arquivo, tipo)
    google_drive.upload_report(service, caminho_arquivo, folder_id)
    file_handler.remove_file(caminho_arquivo)


def envio_mensal_atual(service, folder_id, tipo):
    caminho_arquivo = file_handler.wait_download(tipo)
    caminho_arquivo = file_handler.rename_file_atual_month(caminho_arquivo, tipo)
    google_drive.upload_report(service, caminho_arquivo, folder_id)
    file_handler.remove_file(caminho_arquivo)



def coleta_veniti(service, driver, selectors, configs):
    dia, dia_semana, hora = scheduler.get_datas()
    if (scheduler.verificacao_data_veniti(dia, dia_semana, hora)):
        url = configs["url"]
        values = configs["credenciais"]
        folder_id = configs["folder_id"]

        login_veniti(driver, url["login_url"], url["home_url"], selectors, values)

        selectors = selectors["relatorio"]
        if (scheduler.agendamento_coleta_atendimentos(dia, dia_semana, hora)):
            coleta_atendimentos(service, driver, selectors["atendimentos"], url["atendimento_url"], folder_id["atendimentos_folder_id"], tipo="atendimentos")
        if (scheduler.agendamento_coleta_conjuntura(dia, dia_semana, hora)):
            coleta_conjuntura(service, driver, selectors["conjuntura"], url["conjuntura_url"], folder_id["conjuntura_folder_id"], tipo="conjuntura")
