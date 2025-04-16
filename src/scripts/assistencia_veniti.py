from src.common import ui_actions

def coleta_atendimentos(driver, selectors, link):
    ui_actions.carregar_url(driver, link)
    ui_actions.detectar_e_clicar_n_elementos(driver, selectors)


def coleta_assistencia_veniti(driver, selectors, links, values):
    # Ebter na página de login
    ui_actions.carregar_url(driver, links[0])
    ui_actions.processo_de_login(driver, selectors["login"], values)
    ui_actions.aguardar_url(driver, links[1])
    coleta_atendimentos(driver, selectors["atendimentos"], links[2])
