from src.common import ui_actions, file_handler, google_drive, date_utils
from src.app import scheduler

def login_pabxvip(driver, login_url, home_url, selectors, values):
    ui_actions.carregar_url(driver, login_url)
    ui_actions.processo_de_login(driver, selectors["login"], values)
    ui_actions.aguardar_url(driver, home_url)


def coleta_mensal(service, driver, atributos, periodo, url, folder_id, tipo):
    try:
        ui_actions.carregar_url(driver, url)
        if (date_utils.get_day() == 1):
            ui_actions.preencher_periodo_mensal_passado(driver, periodo)
        else:
            ui_actions.preencher_periodo_mensal_atual(driver, periodo)
        ui_actions.detectar_e_clicar_n_elementos(driver, atributos)
        caminho_arquivo = file_handler.wait_download(tipo)
        if (date_utils.get_day() == 1):
            caminho_arquivo = file_handler.rename_file_previous_month(caminho_arquivo, tipo)
        else:
            caminho_arquivo = file_handler.rename_file_atual_month(caminho_arquivo, tipo)
        
        google_drive.upload_report(service, caminho_arquivo, folder_id)
        file_handler.remove_file(caminho_arquivo)
    except Exception as e:
        print(f"Erro ao coletar {tipo}: {e}\n")


def coleta_pabxvip(service, driver, selectors, configs):
    dia, dia_semana, hora = scheduler.get_datas()
    if (scheduler.verificacao_data_pabxvip(dia, dia_semana, hora)):
        url = configs["url"]
        values = configs["credenciais"]
        folder_id = configs["folder_id"]

        login_pabxvip(driver, url["login_url"], url["home_url"], selectors, values)
        
        selectors = selectors["relatorio"]
        tw = selectors["tw"]

        if (scheduler.agendamento_coleta_tw(dia, dia_semana, hora)):
            coleta_mensal(service, driver, tw["atributos"], tw["periodo"], url["atendimento_url"], folder_id["tw_folder_id"], tipo="tw")
