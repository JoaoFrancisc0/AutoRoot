from src.common import sys, os, json, TwoCaptcha, Path


def obter_resources_dir():
    if getattr(sys, 'frozen', False):
        path = Path(sys._MEIPASS) / 'resources' / '2Captcha.json'
        return path
    path = Path(__file__).resolve().parent.parent.parent / 'resources' / '2Captcha.json'
    return path


def ler_dados_api(site_name):
    path = obter_resources_dir()

    with open(path, 'r', encoding='utf-8') as f:
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
