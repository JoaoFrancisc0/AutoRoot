from src.common import ui_actions

def coleta_assistencia_veniti(driver, urlLogin, selectors, values):
    # Ebter na página de login
    ui_actions.carregar_url(driver, urlLogin)
    ui_actions.processo_de_login(driver, selectors, values)
