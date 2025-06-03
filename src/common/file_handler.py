from src.common import os, pd, time, date_utils


def get_download_folder():
    """Retorna o caminho da pasta de downloads do usuário."""
    return os.path.join(os.path.expanduser("~"), "Downloads")


def is_recent_file(caminho_arquivo, segundos=10):
    """Verifica se o arquivo foi modificado nos últimos X segundos."""
    agora = time.time()
    return agora - os.path.getmtime(caminho_arquivo) <= segundos


def find_recent_file(extensoes=(".xlsx", ".xls"), segundos=10):
    """Procura arquivos existentes que foram modificados recentemente."""
    caminho_download = get_download_folder()
    for arquivo in os.listdir(caminho_download):
        if arquivo.endswith(extensoes):
            caminho_arquivo = os.path.join(caminho_download, arquivo)
            if is_recent_file(caminho_arquivo, segundos):
                return caminho_arquivo
    return None


def find_new_file(arquivos_antes, extensoes=(".xlsx", ".xls")):
    """Procura novos arquivos baixados com extensões específicas."""
    caminho_download = get_download_folder()
    arquivos_agora = set(os.listdir(caminho_download))
    novos_arquivos = arquivos_agora - arquivos_antes
    for arquivo in novos_arquivos:
        if arquivo.endswith(extensoes):
            return os.path.join(caminho_download, arquivo)
    return None


def wait_download(tipo, extensoes=(".xlsx", ".xls"), timeout=90, recente_em_segundos=10):
    """Aguarda o download de um novo arquivo .xlsx ou .xls, priorizando arquivos recentes."""
    try:
        caminho_download = get_download_folder()
        tempo_inicial = time.time()

        # Primeiro, tenta encontrar um arquivo já existente e recente
        arquivo_recente = find_recent_file(extensoes, recente_em_segundos)
        if arquivo_recente:
            return arquivo_recente

        # Se não encontrar, começa a observar novos arquivos
        arquivos_antes = set(os.listdir(caminho_download))

        while True:
            novo_arquivo = find_new_file(arquivos_antes, extensoes)
            if novo_arquivo:
                return novo_arquivo

            # Timeout para não travar pra sempre
            if time.time() - tempo_inicial > timeout:
                raise TimeoutError(f"Timeout esperando download do tipo {tipo}")

            time.sleep(1)

    except Exception as e:
        raise


# Remover o arquivo residual
def remove_file(file_path):
    try:
        os.remove(file_path)
        time.sleep(2)
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        raise
    except PermissionError:
        print(f"Permission denied to remove the file: {file_path}")
        raise
    except Exception as e:
        print(f"Unexpected error while removing the file: {e}")
        raise


# Converte o arquivo .xls (formato tabela HTML) para o formato .xlsx
def convert_file_html(file_path):
    try:
        new_file_path = file_path + "x"  # just adds an 'x' to make .xlsx

        # Read all tables from the HTML-formatted file
        dfs = pd.read_html(file_path)

        # Write them into a new Excel file
        with pd.ExcelWriter(new_file_path, engine="openpyxl") as writer:
            for i, df in enumerate(dfs):
                df.to_excel(writer, sheet_name=f"Sheet{i+1}", index=False)

        # print(f"Conversion completed: {new_file_path}")
        remove_file(file_path)
        return new_file_path
    except Exception as e:
        print(f"Error converting file: {e}")
        raise


# Renomeia o arquivo
def rename_file(file_path, file_type):
    try:
        directory = os.path.dirname(file_path)
        new_name = f"{file_type}.xlsx"
        new_path = os.path.join(directory, new_name)
        os.rename(file_path, new_path)
        return new_path
    except Exception as e:
        print(f"Error renaming file: {e}")
        raise


def rename_file_atual_month(caminho_arquivo, tipo):
    """Renomeia o arquivo para um nome mais amigável."""
    try:
        namMes = date_utils.get_month_name()
        numAno = date_utils.get_year()
        pasta, _ = os.path.split(caminho_arquivo)
        novo_nome = f"{tipo}_{namMes}_{numAno}.xlsx"
        caminho_novo = os.path.join(pasta, novo_nome)
        os.rename(caminho_arquivo, caminho_novo)
        return caminho_novo
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho_arquivo}")
        raise
    except PermissionError:
        print(f"Permissão negada para renomear o arquivo: {caminho_arquivo}")
        raise
    except Exception as e:
        print(f"Erro inesperado ao renomear o arquivo: {e}")
        raise


def rename_file_previous_month(caminho_arquivo, tipo):
    """Renomeia o arquivo para um nome mais amigável."""
    try:
        namMes = date_utils.get_previous_month_name()
        numAno = date_utils.get_previous_year()
        pasta, _ = os.path.split(caminho_arquivo)
        novo_nome = f"{tipo}_{namMes}_{numAno}.xlsx"
        caminho_novo = os.path.join(pasta, novo_nome)
        os.rename(caminho_arquivo, caminho_novo)
        return caminho_novo
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {caminho_arquivo}")
        raise
    except PermissionError:
        print(f"Permissão negada para renomear o arquivo: {caminho_arquivo}")
        raise
    except Exception as e:
        print(f"Erro inesperado ao renomear o arquivo: {e}")
        raise
