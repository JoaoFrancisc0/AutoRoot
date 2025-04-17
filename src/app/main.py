from common import driver_manager, config_loader, google_drive
from scripts import assistencia_veniti, supervisao_sga


def carregar_configuracoes(base_dir):
    return {
        "assistencia_tw_env": config_loader.load_env("assistencia_tw", base_dir),
        "assistencia_veniti_env": config_loader.load_env("assistencia_veniti", base_dir),
        "evento_ileva_env": config_loader.load_env("evento_ileva", base_dir),
        "evento_kommo_env": config_loader.load_env("evento_kommo", base_dir),
        "supervisao_sga_env": config_loader.load_env("supervisao_sga", base_dir),
        "assistencia_veniti_selectors": config_loader.load_json("assistencia_veniti", base_dir),
        "supervisao_sga_selectors": config_loader.load_json("supervisao_sga", base_dir)
    }


def inicializar_driver():
    options = driver_manager.configure_driver_options()
    return driver_manager.start_driver(options)


def autenticar_google_drive(base_dir):
    return google_drive.authenticate(base_dir)


def automacao_assistencia_veniti(driver, urlLogin, selectors, values):
    assistencia_veniti.coleta_assistencia_veniti(driver, urlLogin, selectors, values)


def automacao_supervisao_sga(driver, urlLogin, selectors, values):
    supervisao_sga.coleta_supervisao_sga(driver, urlLogin, selectors, values)


def main(base_dir):
    service = autenticar_google_drive(base_dir)
    driver = inicializar_driver()
    
    configs = carregar_configuracoes(base_dir)
    
    # automacao_assistencia_veniti(
    #     driver,
    #     configs["assistencia_veniti_selectors"],
    #     [
    #         configs["assistencia_veniti_env"]["LOGIN_URL"],
    #         configs["assistencia_veniti_env"]["HOME_URL"],
    #         configs["assistencia_veniti_env"]["ATENDIMENTO_URL"],
    #         configs["assistencia_veniti_env"]["CONJUNTURA_URL"],
    #     ],
    #     [
    #         configs["assistencia_veniti_env"]["USERNAME"],
    #         configs["assistencia_veniti_env"]["PASSWORD"],
    #         configs["assistencia_veniti_env"]["ID_EXTRA"]
    #     ]
    # )

    automacao_supervisao_sga(
        driver,
        configs["supervisao_sga_selectors"],
        [
            configs["supervisao_sga_env"]["LOGIN_URL"],
            configs["supervisao_sga_env"]["HOME_URL"],
            configs["supervisao_sga_env"]["VEICULO_URL"],
            configs["supervisao_sga_env"]["BOLETO_URL"],
        ],
        [
            configs["supervisao_sga_env"]["USERNAME"],
            configs["supervisao_sga_env"]["PASSWORD"]
        ]
    )

    print("Automação finalizada.")
    input("Pressione Enter para sair...")


if __name__ == "__main__":
    import os
    base_dir = os.getcwd()
    main(base_dir)
