from src.common import ui_actions
import time


def coleta_atendimentos(driver, selectors, link):
    ui_actions.carregar_url(driver, link)
    ui_actions.detectar_e_clicar_n_elementos(driver, selectors["busca"])
    ui_actions.preencher_periodo_mensal(driver, selectors["periodo"])
    ui_actions.detectar_e_clicar_n_elementos(driver, selectors["atributos"])


def coleta_assistencia_veniti(driver, selectors, links, values):
    # Ebter na página de login
    ui_actions.carregar_url(driver, links[0])
    ui_actions.processo_de_login(driver, selectors["login"], values)
    ui_actions.confirmar_login(driver, selectors["confirmacao"])
    ui_actions.aguardar_url(driver, links[1])
    coleta_atendimentos(driver, selectors, links[2])
