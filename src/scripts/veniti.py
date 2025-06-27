from src.common import ui_actions, file_handler, google_drive, date_utils, table_handler
from src.app import scheduler

def login_veniti(driver, login_url, home_url, selectors, values):
    ui_actions.carregar_url(driver, login_url)
    ui_actions.processo_de_login(driver, selectors["login"], values)
    ui_actions.confirmar_login(driver, selectors["confirmacao"])
    ui_actions.aguardar_url(driver, home_url)


def coleta_atendimentos(service, driver, selectors, url, folder_id, tipo):
    try:
        ui_actions.carregar_url(driver, url)
        ui_actions.detectar_e_clicar_n_elementos(driver, selectors["busca"])
        if date_utils.get_day() == 1:
            ui_actions.preencher_periodo_mensal_passado(driver, selectors["periodo"])
        else:
            ui_actions.preencher_periodo_mensal_atual(driver, selectors["periodo"])
        ui_actions.detectar_e_clicar_n_elementos(driver, selectors["atributos"])
        ui_actions.detectar_e_aguardar_valor_em_elemento(driver, selectors["download"]["status"], "EXPORTADO E BAIXADO")
        ui_actions.detectar_e_clicar_elemento(driver, selectors["download"]["download"])
        caminho_arquivo = file_handler.wait_download(tipo)
        if date_utils.get_day() == 1:
            caminho_arquivo = file_handler.rename_file_previous_month(caminho_arquivo, tipo)
        else:
            caminho_arquivo = file_handler.rename_file_atual_month(caminho_arquivo, tipo)
        google_drive.upload_report(service, caminho_arquivo, folder_id)
        file_handler.remove_file(caminho_arquivo)

    except Exception as e:
        print(f"Erro ao coletar {tipo}: {e}\n")


def coleta_conjuntura(service, driver, selectors, url, folder_id, tipo):
    try:
        ui_actions.carregar_url(driver, url)
        ui_actions.detectar_e_clicar_elemento(driver, selectors["busca"])
        if date_utils.get_day() == 1:
            ui_actions.preencher_periodo_mensal_passado(driver, selectors["periodo"])
        else:
            ui_actions.preencher_periodo_mensal_atual(driver, selectors["periodo"])
        ui_actions.detectar_e_clicar_n_elementos(driver, selectors["atributos"])
        caminho_arquivo = file_handler.wait_download(tipo)
        if date_utils.get_day() == 1:
            caminho_arquivo = file_handler.rename_file_previous_month(caminho_arquivo, tipo)
            month_filter = f"/{date_utils.get_two_months_ago_month_number()}/"
            table_handler.remove_lines_outside_month_filter(caminho_arquivo, 3, month_filter)
        else:
            caminho_arquivo = file_handler.rename_file_atual_month(caminho_arquivo, tipo)
            month_filter = f"/{date_utils.get_previous_month_number()}/"
            table_handler.remove_lines_outside_month_filter(caminho_arquivo, 3, month_filter)
        google_drive.upload_report(service, caminho_arquivo, folder_id)
        file_handler.remove_file(caminho_arquivo)
    except Exception as e:
        print(f"Erro ao coletar {tipo}: {e}\n")


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
