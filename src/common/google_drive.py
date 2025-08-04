from src.common import build, MediaFileUpload, Request, service_account, logging, os

# Authenticates with the Google Drive API
def authenticate(base_dir, service_account_file='credenciais.json', scopes='https://www.googleapis.com/auth/drive'):
    try:
        if isinstance(scopes, str):
            scopes = [scopes]
        cred_path = base_dir / "resources" / service_account_file
        creds = service_account.Credentials.from_service_account_file(cred_path, scopes=scopes)
        creds.refresh(Request())
        return build("drive", "v3", credentials=creds)
    except Exception as e:
        raise Exception (f"Error authenticating with the Google Drive API: {e}")


# Searches for a report file in a specified Google Drive folder
def find_report(service, file_name, folder_id):
    try:
        query = f"name = '{file_name}' and '{folder_id}' in parents and trashed = false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get("files", [])
        return files[0] if files else None
    except Exception as e:
        raise Exception (f"Error searching file in Google Drive: {e}")


# Uploads or updates a report file to Google Drive, converting to Google Sheets format
def upload_report(service, file_path, parent_folder_id):
    try:
        file_name = file_path.split("\\")[-1]
        existing_file = find_report(service, file_name, parent_folder_id)
        media = MediaFileUpload(file_path, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        if existing_file:
            file_id = existing_file["id"]
            service.files().update(fileId=file_id, media_body=media).execute()
            # print(f"File updated: {file_name} (ID: {file_id})")
            logging.info(f"File updated: {file_name}\n")
        else:
            file_metadata = {
                "name": file_name,
                "parents": [parent_folder_id],
                # "mimeType": "application/vnd.google-apps.spreadsheet" Para google Sheets
                "mimeType": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet" # Para Excel
            }
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields="id, name"
            ).execute()
            # print(f"File uploaded: {file.get('name')} (ID: {file.get('id')})")
            logging.info(f"File uploaded: {file.get('name')}\n")

    except Exception as e:
        raise Exception (f"Error uploading to Google Drive: {e}")


def upload_log(service, log_file_path, log_folder_id):
    try:
        file_name = os.path.basename(log_file_path)

        media = MediaFileUpload(log_file_path, mimetype="text/plain")

        file_metadata = {
            "name": file_name,
            "parents": [log_folder_id],
            "mimeType": "text/plain"
        }
        file = service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id, name"
        ).execute()
        print(f"Log enviado ao Google Drive: {file.get('name')}")

    except Exception as e:
        print(f"Error uploading log: {e}")


def upload_images(service, image_paths, folder_id):
    for image_path in image_paths:
        try:
            file_name = os.path.basename(image_path)

            media = MediaFileUpload(image_path, mimetype="image/png")

            file_metadata = {
                "name": file_name,
                "parents": [folder_id],
                "mimeType": "image/png"
            }

            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields="id, name"
            ).execute()

            print(f"Imagem enviada ao Google Drive: {file.get('name')}")

        except Exception as e:
            print(f"Erro ao enviar imagem {image_path}: {e}")
