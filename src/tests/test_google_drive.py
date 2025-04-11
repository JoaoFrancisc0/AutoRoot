import pytest
from unittest.mock import MagicMock, patch, mock_open

from src.common import google_drive

@pytest.fixture
def fake_service():
    return MagicMock()


def test_authenticate_success(tmp_path):
    service_account_file = "fake_service.json"
    scopes = ["https://www.googleapis.com/auth/drive"]

    fake_credentials = MagicMock()
    fake_build = MagicMock()

    with patch("src.common.google_drive.service_account.Credentials.from_service_account_file", return_value=fake_credentials), \
         patch("src.common.google_drive.Request"), \
         patch("src.common.google_drive.build", return_value=fake_build):

        service = google_drive.authenticate(tmp_path, service_account_file, scopes)

        assert service == fake_build
        fake_credentials.refresh.assert_called_once()


def test_find_report_found(fake_service):
    fake_file = {"id": "123", "name": "file"}
    fake_service.files().list().execute.return_value = {"files": [fake_file]}

    result = google_drive.find_report(fake_service, "file.xlsx", "folder123")

    assert result == fake_file


def test_find_report_not_found(fake_service):
    fake_service.files().list().execute.return_value = {"files": []}

    result = google_drive.find_report(fake_service, "missing.xlsx", "folder123")

    assert result is None

def test_upload_report_create(fake_service):
    with patch("builtins.open", mock_open(read_data="fake content")) as mocked_file:
        fake_service.files().list().execute.return_value = {"files": []}
        fake_service.files().create().execute.return_value = {"id": "999", "name": "new_file"}

        fake_service.files().create.reset_mock()
        
        google_drive.upload_report(fake_service, "C:\\files\\new_file.xlsx", "folder_id")

        fake_service.files().create.assert_called_once()
        mocked_file.assert_called_once_with("C:\\files\\new_file.xlsx", "rb")


def test_upload_report_update(fake_service):
    with patch("builtins.open", mock_open(read_data="fake content")) as mocked_file:
        fake_service.files().list().execute.return_value = {
            "files": [{"id": "existing_id", "name": "old.xlsx"}]
        }

        google_drive.upload_report(fake_service, "C:\\files\\old.xlsx", "folder_id")

        fake_service.files().update.assert_called_once()
        mocked_file.assert_called_once_with("C:\\files\\old.xlsx", "rb")
