from src.common import ui_actions, file_handler, google_drive
from app import scheduler

def login_ileva(driver, login_url, home_url, selectors, values):
    ui_actions.carregar_url(driver, login_url)
    ui_actions.processo_de_login(driver, selectors["login"], values)
    ui_actions.aguardar_url(driver, home_url)
    

def coleta(service, driver, atributos, url, folder_id, tipo):
    try:
        atributos = atributos["atributos"]
        ui_actions.carregar_url(driver, url)
        ui_actions.detectar_e_clicar_n_elementos(driver, atributos)
        caminho_arquivo = file_handler.wait_download(tipo)
        caminho_arquivo = file_handler.convert_file_html(caminho_arquivo)
        caminho_arquivo = file_handler.rename_file(caminho_arquivo, tipo)
        google_drive.upload_report(service, caminho_arquivo, folder_id)
        file_handler.remove_file(caminho_arquivo)
    except Exception as e:
        print(f"Erro ao coletar mensal {tipo}: {e}")


def coleta_ileva(service, driver, selectors, configs):
    dia, dia_semana, hora = scheduler.get_datas()
    if (scheduler.verificacao_data_ileva(dia, dia_semana, hora)):
        url = configs["url"]
        values = configs["credenciais"]
        folder_id = configs["folder_id"]

        login_ileva(driver, url["login_url"], url["home_url"], selectors, values)

        selectors = selectors["relatorio"]
        if (scheduler.agendamento_coleta_custo(dia, dia_semana, hora)):
            coleta(service, driver, selectors["custo"], url["custo_url"], folder_id["custo_folder_id"], tipo="custo")
        if (scheduler.agendamento_coleta_compra(dia, dia_semana, hora)):
            coleta(service, driver, selectors["compra"], url["compra_url"], folder_id["compra_folder_id"], tipo="compra")
        if (scheduler.agendamento_coleta_envolvido(dia, dia_semana, hora)):
            coleta(service, driver, selectors["envolvido"], url["envolvido_url"], folder_id["envolvido_folder_id"], tipo="envolvido")
        if (scheduler.agendamento_coleta_pagamento(dia, dia_semana, hora)):
            coleta(service, driver, selectors["pagamento"], url["pagamento_url"], folder_id["pagamento_folder_id"], tipo="pagamento")