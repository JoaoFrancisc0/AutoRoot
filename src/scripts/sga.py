from src.common import ui_actions, file_handler, google_drive
from app import scheduler


def login_sga(driver, login_url, home_url, selectors, values):
    ui_actions.carregar_url(driver, login_url)
    ui_actions.confirmar_login(driver, selectors["confirmacao"])
    ui_actions.processo_de_login_com_reCAPTCHA(driver, selectors["login"], values)
    ui_actions.aguardar_url(driver, home_url)


def coleta_mensal(service, driver, selectors, url, folder_id, tipo):
    ui_actions.carregar_url(driver, url)
    ui_actions.preencher_periodo_mensal_passado(driver, selectors["periodo"])
    ui_actions.detectar_e_clicar_n_elementos(driver, selectors["atributos"])
    caminho_arquivo = file_handler.wait_download(tipo)
    caminho_arquivo = file_handler.convert_file(caminho_arquivo)
    caminho_arquivo = file_handler.rename_file_previous_month(caminho_arquivo, tipo)
    google_drive.upload_report(service, caminho_arquivo, folder_id)
    file_handler.remove_file(caminho_arquivo)


def coleta_semanal(service, driver, selectors, url, folder_id, tipo):
    pass


def coleta_sga(service, driver, selectors, configs):
    dia, dia_semana, hora = scheduler.get_datas()
    if (scheduler.verificacao_data_sga(dia, dia_semana, hora)):  
        url = configs["url"]
        values = configs["credenciais"]
        folder_id = configs["folder_id"]
        login_sga(driver, url["login_url"], url["home_url"], selectors, values)

        if (scheduler.agendamento_boleto_fechamento_mensal(dia, dia_semana, hora)):
            coleta_mensal(service, driver, selectors, url["boleto_url"], folder_id["boleto_fechamento_folder_id"], tipo="boleto_fechamento")
        elif (scheduler.agendamento_veiculo_evasao_mensal_e_veiculo_cancelamento_mensal(dia, dia_semana, hora)):
            coleta_mensal(service, driver, selectors, url["veiculo_evasao_url"], folder_id["veiculo_evasao_folder_id"], tipo="veiculo_evasao")
            coleta_mensal(service, driver, selectors, url["veiculo_cancelamento_url"], folder_id["veiculo_cancelamento_folder_id"], tipo="veiculo_cancelamento")
        elif (scheduler.agendamento_boleto_fechamento_semanal_e_veiculo_cancelamento_semanal(dia, dia_semana, hora)):
            coleta_semanal(service, driver, selectors, url["veiculo_cancelamento_semanal_url"], folder_id["veiculo_cancelamento_semanal_folder_id"], tipo="veiculo_cancelamento_semanal")
