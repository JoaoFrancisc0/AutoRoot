import pytest

from src.common.html_parser import add_quotes_to_columns

SAMPLE_HTML = '''
<html>
  <body>
    <table border="1">
      <tr><td>123</td><td>abc</td></tr>
      <tr><td>456</td><td>"xyz"</td></tr>
    </table>
  </body>
</html>
'''

EXPECTED_HTML_FRAGMENT = '"123"'  # Espera-se que 123 vire "123" no output

def test_add_quotes_to_columns_utf8(tmp_path):
    fake_path = tmp_path / "test.xls"
    fake_output_path = tmp_path / "test_c.xls"

    # Cria um arquivo temporário com o conteúdo HTML
    fake_path.write_text(SAMPLE_HTML, encoding="utf-8")

    result_path = add_quotes_to_columns(str(fake_path), [0])  # Aplica em coluna 0

    # Verifica se o novo arquivo foi criado
    assert result_path == str(fake_output_path)
    assert fake_output_path.exists()

    # Verifica se o conteúdo foi modificado corretamente
    output_html = fake_output_path.read_text(encoding="utf-16")
    assert EXPECTED_HTML_FRAGMENT in output_html


def test_add_quotes_to_columns_utf16(tmp_path):
    fake_path = tmp_path / "test.xls"
    fake_output_path = tmp_path / "test_c.xls"

    # Escreve o arquivo com encoding utf-16 (forçando o fallback)
    fake_path.write_text(SAMPLE_HTML, encoding="utf-16")

    result_path = add_quotes_to_columns(str(fake_path), [0])

    assert result_path == str(fake_output_path)
    assert fake_output_path.exists()
    output_html = fake_output_path.read_text(encoding="utf-16")
    assert EXPECTED_HTML_FRAGMENT in output_html


def test_table_not_found(tmp_path):
    html_no_table = "<html><body><p>No table here</p></body></html>"
    fake_path = tmp_path / "notable.xls"
    fake_path.write_text(html_no_table, encoding="utf-8")

    with pytest.raises(ValueError, match="No table found in the HTML."):
        add_quotes_to_columns(str(fake_path), [0])
