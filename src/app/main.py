from common import driver_manager, config_loader, google_drive
from scripts import assistencia_veniti, assistencia_tw, evento_ileva, evento_kommo

# ==================== FUNÇÕES AUXILIARES ====================
def carregar_configuracoes(base_dir):
    return {
        "assistencia_tw_env": config_loader.load_env("assistencia_tw", base_dir),
        "assistencia_veniti_env": config_loader.load_env("assistencia_veniti", base_dir),
        "evento_ileva_env": config_loader.load_env("evento_ileva", base_dir),
        "evento_kommo_env": config_loader.load_env("evento_kommo", base_dir),
        "assistencia_veniti_selectors": config_loader.load_json("assistencia_veniti", base_dir),
    }

def inicializar_driver():
    options = driver_manager.configure_driver_options()
    return driver_manager.start_driver(options)

def autenticar_google_drive(base_dir):
    return google_drive.authenticate(base_dir)

# ==================== FUNÇÕES DE AUTOMAÇÃO ====================
def automacao_assistencia_tw():
    print("Automação TW ainda não implementada.")

def automacao_assistencia_veniti(driver, urlLogin, selectors, values):
    assistencia_veniti.coleta_assistencia_veniti(driver, urlLogin, selectors, values)

def automacao_evento_ileva():
    print("Automação evento iLeva ainda não implementada.")

def automacao_evento_kommo():
    print("Automação evento Kommo ainda não implementada.")

# ==================== FUNÇÃO PRINCIPAL ====================
def main(base_dir):
    service = autenticar_google_drive(base_dir)
    driver = inicializar_driver()
    
    configs = carregar_configuracoes(base_dir)
    
    automacao_assistencia_tw()
    automacao_assistencia_veniti(
        driver,
        configs["assistencia_veniti_env"]["LOGIN_URL"],
        configs["assistencia_veniti_selectors"]["login"],
        [
            configs["assistencia_veniti_env"]["USERNAME"],
            configs["assistencia_veniti_env"]["PASSWORD"],
            configs["assistencia_veniti_env"]["ID_EXTRA"]
        ]
    )
    automacao_evento_ileva()
    automacao_evento_kommo()
    print("Automação finalizada.")

# ==================== EXECUÇÃO ====================
if __name__ == "__main__":
    import os
    base_dir = os.getcwd()
    main(base_dir)
