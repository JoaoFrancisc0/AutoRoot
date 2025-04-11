import os
import pandas as pd
import time

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
def convert_file(file_path):
    try:
        new_file_path = file_path + "x"  # just adds an 'x' to make .xlsx

        # Read all tables from the HTML-formatted file
        dfs = pd.read_html(file_path)

        # Write them into a new Excel file
        with pd.ExcelWriter(new_file_path, engine="openpyxl") as writer:
            for i, df in enumerate(dfs):
                df.to_excel(writer, sheet_name=f"Sheet{i+1}", index=False)

        print(f"Conversion completed: {new_file_path}")
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
