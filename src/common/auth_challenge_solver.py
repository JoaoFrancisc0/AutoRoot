from src.common import sys, os, json, TwoCaptcha, pyotp, Path, time


def obter_resources_dir():
    if getattr(sys, 'frozen', False):
        path = Path(sys._MEIPASS) / 'resources' / '2Captcha.json'
        return path
    path = Path(__file__).resolve().parent.parent.parent / 'resources' / '2Captcha.json'
    return path


def ler_dados_api(site_name, type):
    path = obter_resources_dir()

    with open(path, 'r', encoding='utf-8') as f:
        dados = json.load(f)
        site_key = site_name + "_site_key"
        secret_2FA = site_name + "_secret_2FA"
        if type == "reCAPTCHA":
            return dados['api_key'], dados[site_key]
        elif type == "twoFA":
            return dados[secret_2FA]
    

def reCAPTCHA(url, site_name):
    api_key, site_key = ler_dados_api(site_name, type="reCAPTCHA")

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
    

def twoFA(site_name):
    secret = ler_dados_api(site_name, type="twoFA")
    codigo = ""

    while True:
        totp = pyotp.TOTP(secret)
        code = totp.now()                      # seu código de 6 dígitos
        if codigo != code:
            return code
        time.sleep(1)
