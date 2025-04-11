import locale
from datetime import datetime
from unidecode import unidecode

# Seta o local para português do Brasil
def set_locale():
    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
    except locale.Error:
        pass

# Retorna a data formatada de acordo com o formato especificado
def get_formatted_date(fmt):
    set_locale()
    return datetime.now().strftime(fmt)

# Retorna o nome do mês atual
def get_month_name():
    return unidecode(get_formatted_date("%B"))

# Retorna o numero do mês atual como uma string
def get_month_number():
    return get_formatted_date("%m")

# Retorna o ano atual como uma string
def get_year():
    return get_formatted_date("%Y")
