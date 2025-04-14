import pytest
import json
from src.common import config_loader

def test_load_env_success(tmp_path):
    env_dir = tmp_path / "resources" / "envs"
    env_dir.mkdir(parents=True)
    env_file = env_dir / "test.env"
    env_file.write_text("KEY1=value1\nKEY2=value2", encoding="utf-8")

    result = config_loader.load_env("test", tmp_path)

    assert result["KEY1"] == "value1"
    assert result["KEY2"] == "value2"


def test_load_env_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError) as excinfo:
        config_loader.load_env("missing", tmp_path)
    assert "Arquivo .env 'missing'" in str(excinfo.value)


def test_load_json_success(tmp_path):
    json_dir = tmp_path / "resources" / "selectors"
    json_dir.mkdir(parents=True)
    json_file = json_dir / "sample.json"
    data = {"field1": "value1", "field2": 2}
    json_file.write_text(json.dumps(data, indent=2), encoding="utf-8")

    result = config_loader.load_json("sample", tmp_path)

    assert result == data


def test_load_json_file_not_found(tmp_path):
    with pytest.raises(FileNotFoundError) as excinfo:
        config_loader.load_json("missing", tmp_path)
    assert "Arquivo JSON 'missing'" in str(excinfo.value)
