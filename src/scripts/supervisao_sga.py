from src.common import ui_actions
import time
def coleta_boleto_fechamento(driver, selectors, link):
    ui_actions.carregar_url(driver, link)


def coleta_supervisao_sga(driver, selectors, links, values):
    ui_actions.carregar_url(driver, links[0])
    ui_actions.confirmar_login(driver, selectors["confirmacao"])
    ui_actions.processo_de_login(driver, selectors["login"], values)
    ui_actions.aguardar_url(driver, links[1])
