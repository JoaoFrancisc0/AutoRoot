from src.common import webdriver, Service, ChromeDriverManager

# Configura o Chrome Driver options
def configure_driver_options():
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36")
    # Disable messages and logs
    options.add_argument("--disable-gpu")
    options.add_argument('--log-level=3')
    
    options.add_experimental_option("prefs", {
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "safebrowsing.disable_download_protection": True
    })
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    return options

# Inicia o Chrome WebDriver com as opções configuradas
def start_driver(options):
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
