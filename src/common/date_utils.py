from common import locale, datetime, timedelta, unidecode


# Seta o local para português do Brasil
def set_locale():
    try:
        locale.setlocale(locale.LC_TIME, 'pt_BR.utf8')
    except locale.Error:
        pass


# Retorna a data do mês anterior
def get_previous_month_date():
    today = datetime.now()
    first_day_of_current_month = today.replace(day=1)
    last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
    return last_day_of_previous_month


# Retorna a data formatada de acordo com o formato especificado
def get_formatted_date(fmt):
    set_locale()
    return datetime.now().strftime(fmt)


def get_formatted_previous_date(fmt):
    set_locale()
    date = get_previous_month_date()
    return date.strftime(fmt)


# Retorna o nome do mês atual
def get_month_name():
    return unidecode(get_formatted_date("%B"))


def get_previous_month_name():
    return unidecode(get_formatted_previous_date("%B"))


# Retorna o numero do mês atual como uma string
def get_month_number():
    return get_formatted_date("%m")


def get_previous_month_number():
    return get_formatted_previous_date("%m")


# Retorna o ano atual como uma string
def get_year():
    return get_formatted_date("%Y")


def get_previous_year():
    return get_formatted_previous_date("%Y")
