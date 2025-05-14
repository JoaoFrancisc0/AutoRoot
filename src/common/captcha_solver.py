from src.common import sys, os, json, TwoCaptcha


def ler_dados_api(site_name):
    # Pega o diretório onde o script ou .exe está sendo executado
    if getattr(sys, 'frozen', False):
        # Estamos no .exe (PyInstaller define isso)
        base_path = sys._MEIPASS if hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable)
    else:
        # Executando como script .py
        base_path = os.path.dirname(os.path.abspath(__file__))

    # Sobe até a raiz do projeto e acessa a pasta 'resources'
    projeto_root = os.path.abspath(os.path.join(base_path, '..', '..'))  # de /common/ para raiz
    caminho_arquivo = os.path.join(projeto_root, 'resources', '2Captcha.json')

    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        dados = json.load(f)
        site_key = site_name + "_site_key"

        return dados['api_key'], dados[site_key]
    

def reCAPTCHA(url, site_name):
    api_key, site_key = ler_dados_api(site_name)

    sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

    api_key = os.getenv('APIKEY_2CAPTCHA', api_key)

    solver = TwoCaptcha(api_key)

    try:
        result = solver.recaptcha(
            sitekey=site_key,
            url=url)

    except Exception as e:
        sys.exit(e)

    else:
        return result['code']
