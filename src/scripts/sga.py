from src.common import ui_actions, file_handler, google_drive
from src.app import scheduler


def login_sga(driver, login_url, home_url, selectors, values):
    ui_actions.carregar_url(driver, login_url)
    ui_actions.confirmar_login(driver, selectors["confirmacao"])
    ui_actions.processo_de_login_com_reCAPTCHA(driver, selectors["login"], values, login_url, site_name="sga")
    ui_actions.resolver_2FA(driver, selectors["login"]["botao"], selectors["2FA"], site_name="sga")
    ui_actions.aguardar_url(driver, home_url)


def coleta_mensal(service, driver, atributos, periodo, url, folder_id, tipo, fechamento):
    ui_actions.carregar_url(driver, url)
    if (fechamento):
        ui_actions.preencher_periodo_mensal_passado(driver, periodo)
    else:
        ui_actions.preencher_periodo_mensal_atual(driver, periodo)
    ui_actions.detectar_e_clicar_n_elementos(driver, atributos)
    caminho_arquivo = file_handler.wait_download(tipo)
    caminho_arquivo = file_handler.convert_file_html(caminho_arquivo)
    if (fechamento):
        caminho_arquivo = file_handler.rename_file_previous_month(caminho_arquivo, tipo)
    else:
        caminho_arquivo = file_handler.rename_file_atual_month(caminho_arquivo, tipo)
    google_drive.upload_report(service, caminho_arquivo, folder_id)
    file_handler.remove_file(caminho_arquivo)


def coleta_semanal(service, driver, atributos, periodo, url, folder_id, tipo):
    ui_actions.carregar_url(driver, url)
    ui_actions.preencher_periodo_semanal(driver, periodo)
    ui_actions.detectar_e_clicar_n_elementos(driver, atributos)
    caminho_arquivo = file_handler.wait_download(tipo)
    caminho_arquivo = file_handler.convert_file_html(caminho_arquivo)
    caminho_arquivo = file_handler.rename_file(caminho_arquivo, tipo)
    google_drive.upload_report(service, caminho_arquivo, folder_id)
    file_handler.remove_file(caminho_arquivo)


def coleta_geral(service, driver, atributos, url, folder_id, tipo):
    ui_actions.carregar_url(driver, url)
    ui_actions.detectar_e_clicar_n_elementos(driver, atributos)
    caminho_arquivo = file_handler.wait_download(tipo)
    caminho_arquivo = file_handler.convert_file_html(caminho_arquivo)
    caminho_arquivo = file_handler.rename_file(caminho_arquivo, tipo)
    google_drive.upload_report(service, caminho_arquivo, folder_id)
    file_handler.remove_file(caminho_arquivo)


def coleta_sga(service, driver, selectors, configs):
    dia, dia_semana, hora = scheduler.get_datas()
    if (scheduler.verificacao_data_sga(dia, dia_semana, hora)):
        url = configs["url"]
        values = configs["credenciais"]
        folder_id = configs["folder_id"]

        login_sga(driver, url["login_url"], url["home_url"], selectors, values)
        
        selectors = selectors["setor"]
        supervisao = selectors["supervisao"]
        rastreamento = selectors["rastreamento"]
        evento = selectors["evento"]

        if (scheduler.agendamento_boleto_fechamento_mensal(dia, dia_semana, hora)):
            coleta_mensal(service, driver, supervisao["atributos_boleto_fechamento"], supervisao["periodo_boleto_fechamento"], url["boleto_url"], folder_id["boleto_fechamento_folder_id"], tipo="boleto_fechamento", fechamento=True)
        
        if (scheduler.agendamento_boleto_fechamento_semanal(dia, dia_semana, hora)):
            coleta_semanal(service, driver, supervisao["atributos_boleto_fechamento"], supervisao["periodo_boleto_fechamento"], url["boleto_url"], folder_id["root_folder_id"], tipo="boleto_fechamento_semanal")
        
        if (scheduler.agendamento_veiculo_evasao_mensal(dia, dia_semana, hora)):
            coleta_mensal(service, driver, supervisao["atributos_veiculo_evasao"], supervisao["periodo_veiculo_evasao"], url["veiculo_url"], folder_id["veiculo_evasao_folder_id"], tipo="veiculo_evasao", fechamento=True)

        if (scheduler.agendamento_veiculo_ativo_mensal(dia, dia_semana, hora)):
            coleta_mensal(service, driver, supervisao["atributos_veiculo_ativo"], supervisao["periodo_veiculo_ativo"], url["veiculo_url"], folder_id["veiculo_ativo_folder_id"], tipo="veiculo_ativo", fechamento=True)
        
        if (scheduler.agendamento_veiculo_ativo_semanal(dia, dia_semana, hora)):
            coleta_semanal(service, driver, supervisao["atributos_veiculo_ativo"], supervisao["periodo_veiculo_ativo"], url["veiculo_url"], folder_id["root_folder_id"], tipo="veiculo_ativo_semanal")

        if (scheduler.agendamento_veiculo_cancelamentos_com_rastreador(dia, dia_semana, hora)):
            coleta_mensal(service, driver, rastreamento["atributos_veiculos_cancelamentos_com_rastreador"], rastreamento["periodo_veiculos_cancelamentos_com_rastreador"], url["veiculo_url"], folder_id["veiculo_cancelamento_com_rastreador_folder_id"], tipo="veiculo_cancelamento_com_rastreador", fechamento=False)
        
        if (scheduler.agendamento_contrato(dia, dia_semana, hora)):
            coleta_geral(service, driver, evento["atributos_contrato"], url["veiculo_url"], folder_id["root_folder_id"], tipo="contrato")
