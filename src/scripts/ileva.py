from src.common import ui_actions, file_handler, google_drive, html_parser
from src.app import scheduler

def login_ileva(driver, login_url, home_url, selectors, values):
    ui_actions.carregar_url(driver, login_url)
    ui_actions.processo_de_login(driver, selectors["login"], values)
    ui_actions.aguardar_url(driver, home_url)
    

def coleta(service, driver, atributos, url, folder_id, tipo, colunas_sensiveis):
    atributos = atributos["atributos"]
    ui_actions.carregar_url(driver, url)
    ui_actions.detectar_e_clicar_n_elementos(driver, atributos)
    caminho_arquivo = file_handler.wait_download(tipo)
    caminho_arquivo_antigo = caminho_arquivo
    caminho_arquivo = html_parser.add_quotes_to_columns(caminho_arquivo, colunas_sensiveis)
    file_handler.remove_file(caminho_arquivo_antigo)
    caminho_arquivo = file_handler.convert_file_html(caminho_arquivo)
    caminho_arquivo = file_handler.rename_file(caminho_arquivo, tipo)
    google_drive.upload_report(service, caminho_arquivo, folder_id)
    file_handler.remove_file(caminho_arquivo)


def coleta_ileva(service, driver, selectors, configs):
    dia, dia_semana, hora = scheduler.get_datas()
    if (scheduler.verificacao_data_ileva(dia, dia_semana, hora)):
        url = configs["url"]
        values = configs["credenciais"]
        folder_id = configs["folder_id"]

        login_ileva(driver, url["login_url"], url["home_url"], selectors, values)

        selectors = selectors["relatorio"]
        if (scheduler.agendamento_coleta_custo(dia, dia_semana, hora)):
            coleta(service, driver, selectors["custo"], url["custo_url"], folder_id["root_folder_id"], tipo="custo", colunas_sensiveis=[5,6,7,8,9,10,11,12,13,14])
        if (scheduler.agendamento_coleta_compra(dia, dia_semana, hora)):
            coleta(service, driver, selectors["compra"], url["compra_url"], folder_id["root_folder_id"], tipo="compra", colunas_sensiveis=[])
        if (scheduler.agendamento_coleta_envolvido(dia, dia_semana, hora)):
            coleta(service, driver, selectors["envolvido"], url["envolvido_url"], folder_id["root_folder_id"], tipo="envolvido", colunas_sensiveis=[])
        if (scheduler.agendamento_coleta_pagamento(dia, dia_semana, hora)):
            coleta(service, driver, selectors["pagamento"], url["pagamento_url"], folder_id["root_folder_id"], tipo="pagamento", colunas_sensiveis=[])
            