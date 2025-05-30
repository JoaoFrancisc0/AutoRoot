from src.common import ui_actions, file_handler, google_drive
from src.app import scheduler

def login_alfacb(driver, login_url, home_url, selectors, values):
    ui_actions.carregar_url(driver, login_url)
    ui_actions.processo_de_login(driver, selectors["login"], values)
    ui_actions.aguardar_url(driver, home_url)

# Verificar o schedule para os 2 de rastreamento (sga e alfacb)
def coleta_mensal(service, driver, atributos, periodo, url, folder_id, tipo):
    ui_actions.carregar_url(driver, url)
    ui_actions.detectar_e_clicar_elemento(driver, atributos["filtro_data"])
    ui_actions.preencher_periodo_mensal_atual(driver, periodo)
    ui_actions.detectar_e_clicar_elemento(driver, atributos["buscar"])
    ui_actions.detectar_e_clicar_elemento(driver, atributos["baixar_relatorio_em_excel"])
    caminho_arquivo = file_handler.wait_download(tipo)
    caminho_arquivo = file_handler.rename_file_atual_month(caminho_arquivo, tipo)
    google_drive.upload_report(service, caminho_arquivo, folder_id)
    file_handler.remove_file(caminho_arquivo)


def coleta_alfacb(service, driver, selectors, configs):
    dia, dia_semana, hora = scheduler.get_datas()
    ultimo_dia = scheduler.get_last_day_of_the_month()
    if (scheduler.verificacao_data_alfacb(dia, dia_semana, hora, ultimo_dia)):
        url = configs["url"]
        values = configs["credenciais"]
        folder_id = configs["folder_id"]

        login_alfacb(driver, url["login_url"], url["home_url"], selectors, values)

        selectors = selectors["relatorio"]["Ordem_de_servico"]
        
        if (scheduler.agendamento_coleta_ordem_de_servico(dia, dia_semana, hora, ultimo_dia)):
            coleta_mensal(service, driver, selectors["atributos"], selectors["periodo"], url["Ordem_de_servico_url"], folder_id["ordem_de_servico_folder_id"], tipo="ordem_de_servico")