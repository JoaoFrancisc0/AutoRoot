from common import driver_manager, config_loader, google_drive
from scripts import assistencia_veniti, supervisao_sga


def carregar_configuracoes(base_dir):
    return {
        "assistencia_tw_configs": config_loader.load_json("assistencia_tw", base_dir, 'configs'),
        "assistencia_veniti_configs": config_loader.load_json("assistencia_veniti", base_dir, 'configs'),
        "evento_ileva_configs": config_loader.load_json("evento_ileva", base_dir, 'configs'),
        "evento_kommo_configs": config_loader.load_json("evento_kommo", base_dir, 'configs'),
        "supervisao_sga_configs": config_loader.load_json("supervisao_sga", base_dir, 'configs'),
        "assistencia_veniti_selectors": config_loader.load_json("assistencia_veniti", base_dir, 'selectors'),
        "supervisao_sga_selectors": config_loader.load_json("supervisao_sga", base_dir, 'selectors')
    }


def inicializar_driver():
    options = driver_manager.configure_driver_options()
    return driver_manager.start_driver(options)


def autenticar_google_drive(base_dir):
    return google_drive.authenticate(base_dir)


def automacao_assistencia_veniti(service, driver, selectors, configs):
    assistencia_veniti.coleta_assistencia_veniti(service, driver, selectors, configs)


def automacao_supervisao_sga(service, driver, selectors, configs):
    supervisao_sga.coleta_supervisao_sga(service, driver, selectors, configs)


def main(base_dir):
    service = autenticar_google_drive(base_dir)
    driver = inicializar_driver()
    
    configs = carregar_configuracoes(base_dir)
    
    automacao_assistencia_veniti(service, driver,
        configs["assistencia_veniti_selectors"],
        configs["assistencia_veniti_configs"]
    )

    automacao_supervisao_sga(service, driver,
        configs["supervisao_sga_selectors"],
        configs["supervisao_sga_configs"]
    )

    print("Automação finalizada.")
    input("Pressione Enter para sair...")


if __name__ == "__main__":
    import os
    base_dir = os.getcwd()
    main(base_dir)
