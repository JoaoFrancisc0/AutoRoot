import os
import pytest

from src.common import file_handler

@pytest.fixture
def sample_html_file(tmp_path):
    # Cria um arquivo .xls com conteúdo em formato de tabela HTML
    file = tmp_path / "sample.xls"
    html_table = """
    <table>
        <tr><th>Coluna1</th><th>Coluna2</th></tr>
        <tr><td>Valor1</td><td>Valor2</td></tr>
    </table>
    """
    file.write_text(html_table, encoding="utf-8")
    return file


def test_convert_file_creates_xlsx(sample_html_file):
    converted_path = file_handler.convert_file(str(sample_html_file))
    assert os.path.exists(converted_path)
    assert converted_path.endswith(".xlsx")


def test_rename_file(tmp_path):
    file = tmp_path / "test.xlsx"
    file.write_text("conteúdo")
    
    new_path = file_handler.rename_file(str(file), "report")
    assert os.path.exists(new_path)
    assert "report.xlsx" in str(new_path)


def test_remove_file(tmp_path):
    file = tmp_path / "to_delete.xlsx"
    file.write_text("dados")
    
    assert file.exists()
    file_handler.remove_file(str(file))
    assert not file.exists()
