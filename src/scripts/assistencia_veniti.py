from src.common import ui_actions, date_utils

def coleta_atendimentos(driver, selectors, link):
    ui_actions.carregar_url(driver, link)
    ui_actions.detectar_e_clicar_n_elementos(driver, selectors["atendimentos_1"])
    numMes = date_utils.get_month_number()
    numAno = date_utils.get_year()
    dataInicio = f"01/{numMes}/{numAno}"
    dataFinal = f"31/{numMes}/{numAno}"
    ui_actions.detectar_e_preencher_campo_data(driver, selectors["periodo"]["inicio"], dataInicio)
    ui_actions.detectar_e_preencher_campo_data(driver, selectors["periodo"]["final"], dataFinal)


def coleta_assistencia_veniti(driver, selectors, links, values):
    # Ebter na página de login
    ui_actions.carregar_url(driver, links[0])
    ui_actions.processo_de_login(driver, selectors["login"], values)
    ui_actions.confirmar_login(driver, selectors["confirmacao"])
    ui_actions.aguardar_url(driver, links[1])
    coleta_atendimentos(driver, selectors, links[2])
