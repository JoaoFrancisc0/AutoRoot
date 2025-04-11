from common import date_utils, driver_manager

def automacao_assistencia_tw():
    pass

def automacao_assistencia_veniti():
    pass

def automacao_evento_ileva():
    pass

def automacao_evento_kommo():
    pass

def main(base_dir):
    options = driver_manager.configure_driver_options()
    driver = driver_manager.start_driver(options)

    automacao_assistencia_tw()
    automacao_assistencia_veniti()
    automacao_evento_ileva()
    automacao_evento_kommo()
    print("Rodou")
