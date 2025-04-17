from src.common import ui_actions
import time


def coleta_boleto_fechamento_mensal(driver, selectors, link):
    ui_actions.carregar_url(driver, link)
    ui_actions.preencher_periodo_mensal_passado(driver, selectors["periodo"])
    ui_actions.detectar_e_clicar_n_elementos(driver, selectors["atributos"])


def coleta_supervisao_sga(driver, selectors, links, values):
    ui_actions.carregar_url(driver, links[0])
    ui_actions.confirmar_login(driver, selectors["confirmacao"])
    ui_actions.processo_de_login_com_reCAPTCHA(driver, selectors["login"], values)
    ui_actions.aguardar_url(driver, links[1])
    coleta_boleto_fechamento_mensal(driver, selectors, links[3])
