from src.common import driver_manager, config_loader, google_drive, logger
from src.scripts import alfacb, sga, veniti, ileva, pabxvip, kommo
import logging

def carregar_configuracoes(base_dir):
    return {
        "alfacb_configs": config_loader.load_json("alfacb", base_dir, 'configs'),
        "pabxvip_configs": config_loader.load_json("pabxvip", base_dir, 'configs'),
        "veniti_configs": config_loader.load_json("veniti", base_dir, 'configs'),
        "sga_configs": config_loader.load_json("sga", base_dir, 'configs'),
        "ileva_configs": config_loader.load_json("ileva", base_dir, 'configs'),
        "kommo_configs": config_loader.load_json("kommo", base_dir, 'configs'),

        "alfacb_selectors": config_loader.load_json("alfacb", base_dir, 'selectors'),
        "pabxvip_selectors": config_loader.load_json("pabxvip", base_dir, 'selectors'),
        "veniti_selectors": config_loader.load_json("veniti", base_dir, 'selectors'),
        "sga_selectors": config_loader.load_json("sga", base_dir, 'selectors'),
        "ileva_selectors": config_loader.load_json("ileva", base_dir, 'selectors'),
        "kommo_selectors": config_loader.load_json("kommo", base_dir, 'selectors'),

        "log": config_loader.load_json("log", base_dir, '')
    }


def inicializar_driver():
    options = driver_manager.configure_driver_options()
    return driver_manager.start_driver(options)


def autenticar_google_drive(base_dir):
    return google_drive.authenticate(base_dir)


def automacao_alfacb(service, driver, selectors, configs):
    alfacb.coleta_alfacb(service, driver, selectors, configs)


def automacao_veniti(service, driver, selectors, configs):
    veniti.coleta_veniti(service, driver, selectors, configs)


def automacao_pabxvip(service, driver, selectors, configs):
    pabxvip.coleta_pabxvip(service, driver, selectors, configs)


def automacao_sga(service, driver, selectors, configs):
    sga.coleta_sga(service, driver, selectors, configs)


def automacao_ileva(service, driver, selectors, configs):
    ileva.coleta_ileva(service, driver, selectors, configs)


def automacao_kommo(service, driver, selectors, configs):
    kommo.coleta_kommo(service, driver, selectors, configs)


def main(base_dir):
    try:
        log_path = logger.log_config(base_dir)

        logging.info("Automação iniciada.")

        service = autenticar_google_drive(base_dir)
        driver = inicializar_driver()
        
        configs = carregar_configuracoes(base_dir)
        
        automacao_alfacb(service, driver, configs["alfacb_selectors"], configs["alfacb_configs"])

        automacao_veniti(service, driver, configs["veniti_selectors"], configs["veniti_configs"])

        automacao_pabxvip(service, driver, configs["pabxvip_selectors"], configs["pabxvip_configs"])

        automacao_sga(service, driver, configs["sga_selectors"], configs["sga_configs"])

        automacao_ileva(service, driver, configs["ileva_selectors"], configs["ileva_configs"])

        automacao_kommo(service, driver, configs["kommo_selectors"], configs["kommo_configs"])

        logging.info("Automação finalizada.")

    except Exception as e:
        logging.exception (f"Error in main: {e}")

    finally:
        google_drive.upload_log(service, log_path, configs["log"]["log_folder_id"])

if __name__ == "__main__":
    import os
    base_dir = os.getcwd()
    main(base_dir)
