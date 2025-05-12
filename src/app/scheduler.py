from common import date_utils

def get_datas():
    dia = date_utils.get_day()
    dia_semana = date_utils.get_weekday()
    hora = date_utils.get_current_hour()
    return dia, dia_semana, hora

# ============================================================================================ #
# =========================================  VENITI  ========================================= #
# ============================================================================================ #

def verificacao_data_veniti(dia, dia_semana, hora):
    if (agendamento_coleta_atendimentos(dia, dia_semana, hora) or 
        agendamento_coleta_conjuntura(dia, dia_semana, hora)):
        return True
    return False


def agendamento_coleta_atendimentos(dia, dia_semana, hora):
    # hora 0
    if (hora == 0):
        return True
    return False


def agendamento_coleta_conjuntura(dia, dia_semana, hora):
    # hora 0
    if (hora == 0):
        return True
    return False

# =========================================================================================== #
# ========================================  PABXVIP  ======================================== #
# =========================================================================================== #

def verificacao_data_pabxvip(dia, dia_semana, hora):
    if (agendamento_coleta_tw(dia, dia_semana, hora)):
        return True
    return False


def agendamento_coleta_tw(dia, dia_semana, hora):
    # hora 0
    if (hora == 0):
        return True
    return False

# =========================================================================================== #
# ========================================   ILEVA   ======================================== #
# =========================================================================================== #

def verificacao_data_ileva(dia,dia_semana, hora):
    if (agendamento_coleta_custo(dia, dia_semana, hora) or 
        agendamento_coleta_compra(dia, dia_semana, hora) or 
        agendamento_coleta_envolvido(dia, dia_semana, hora) or 
        agendamento_coleta_pagamento(dia, dia_semana, hora)):
        return True
    return False


def agendamento_coleta_custo(dia, dia_semana, hora):
    # se não for fim de semana e hora 7 ou 13
    if (dia_semana not in ["sábado", "domingo"] and hora in [7, 13]):
        return True
    return False


def agendamento_coleta_compra(dia, dia_semana, hora):
    # se não for fim de semana e hora 7 ou 13
    if (dia_semana not in ["sábado", "domingo"] and hora in [7, 13]):
        return True
    return False


def agendamento_coleta_envolvido(dia, dia_semana, hora):
    # se não for fim de semana e hora 7 ou 13
    if (dia_semana not in ["sábado", "domingo"] and hora in [7, 13]):
        return True
    return False


def agendamento_coleta_pagamento(dia, dia_semana, hora):
    # se não for fim de semana e hora 7 ou 13
    if (dia_semana not in ["sábado", "domingo"] and hora in [7, 13]):
        return True
    return False

# =========================================================================================== #
# ========================================   KOMMO   ======================================== #
# =========================================================================================== #

def verificacao_data_kommo(dia, dia_semana, hora):
    if (True):
        return True
    return False


def agendamento_coleta_kommo(dia, dia_semana, hora):
    if (True):
        return True
    return False

# =========================================================================================== #
# ========================================    SGA    ======================================== #
# =========================================================================================== #

def verificacao_data_sga(dia, dia_semana, hora):
    if (False):
        return True
    return False


def agendamento_boleto_fechamento_mensal(dia, dia_semana, hora):
    if (False):
        return True
    return False


def agendamento_veiculo_evasao_mensal(dia, dia_semana, hora):
    if (True):
        return True
    return False


def agendamento_boleto_fechamento_semanal(dia, dia_semana, hora):
    if (True):
        return True
    return False


def agendamento_veiculo_geral(dia, dia_semana, hora):
    if (True):
        return True
    return False


def agendamento_veiculo_cancelamentos_com_rastreador(dia, dia_semana, hora):
    if (False):
        return True
    return False


def agendamento_contrato(dia, dia_semana, hora):
    if (False):
        return True
    return False
