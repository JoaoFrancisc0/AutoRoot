from common import date_utils, driver_manager, config_loader, google_drive

def automacao_assistencia_tw():
    pass

def automacao_assistencia_veniti():
    pass

def automacao_evento_ileva():
    pass

def automacao_evento_kommo():
    pass

def main(base_dir):
    service = google_drive.authenticate(base_dir)

    options = driver_manager.configure_driver_options()
    driver = driver_manager.start_driver(options)

    assistencia_tw_env = config_loader.load_env("assistencia_tw", base_dir)
    assistencia_veniti_env = config_loader.load_env("assistencia_veniti", base_dir)
    evento_ileva_env = config_loader.load_env("evento_ileva", base_dir)
    evento_kommo_env = config_loader.load_env("evento_kommo", base_dir)
    assistencia_tw_selectors = config_loader.load_json("assistencia_tw", base_dir)
    # assistencia_veniti_selectors = config_loader.load_json("assistencia_veniti", base_dir)
    # evento_ileva_selectors = config_loader.load_json("evento_ileva", base_dir)
    # evento_kommo_selectors = config_loader.load_json("evento_kommo", base_dir)
    automacao_assistencia_tw()
    automacao_assistencia_veniti()
    automacao_evento_ileva()
    automacao_evento_kommo()
    print("Rodou")
