from src.common import ui_actions, file_handler, google_drive
from src.app import scheduler


def login_kommo(driver, login_url, home_url, selectors, values):
    ui_actions.carregar_url(driver, login_url)
    ui_actions.processo_de_login(driver, selectors["login"], values)
    ui_actions.aguardar_url(driver, home_url)


def coleta_geral(service, driver, atributos, folder_id, tipo):
    ui_actions.detectar_e_clicar_n_elementos(driver, atributos)
    caminho_arquivo = file_handler.wait_download(tipo)
    caminho_arquivo = file_handler.rename_file(caminho_arquivo, tipo)
    google_drive.upload_report(service, caminho_arquivo, folder_id)
    file_handler.remove_file(caminho_arquivo)


def coleta_kommo(service, driver, selectors, configs):
    dia, dia_semana, hora = scheduler.get_datas()
    if (scheduler.verificacao_data_kommo(dia, dia_semana, hora)):
        url = configs["url"]
        values = configs["credenciais"]
        folder_id = configs["folder_id"]

        login_kommo(driver, url["login_url"], url["home_url"], selectors, values)
        
        selectors = selectors["relatorio"]
        colisao = selectors["colisao"]

        if (scheduler.agendamento_coleta_kommo(dia, dia_semana, hora)):
            coleta_geral(service, driver, colisao["atributos"], folder_id["colisao_folder_id"], tipo="colisao")
