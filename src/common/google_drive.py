from common import build, MediaFileUpload, Request, service_account


# Authenticates with the Google Drive API
def authenticate(base_dir, service_account_file='credenciais.json', scopes='https://www.googleapis.com/auth/drive'):
    try:
        if isinstance(scopes, str):
            scopes = [scopes]
        cred_path = base_dir / "resources" / service_account_file
        creds = service_account.Credentials.from_service_account_file(cred_path, scopes=scopes)
        # print(creds)
        creds.refresh(Request())
        return build("drive", "v3", credentials=creds)
    except Exception as e:
        print(f"Error authenticating with the Google Drive API: {e}")
        raise


# Searches for a report file in a specified Google Drive folder
def find_report(service, file_name, folder_id):
    try:
        file_name = file_name[:-5] if file_name.endswith(".xlsx") else file_name
        query = f"name = '{file_name}' and '{folder_id}' in parents and trashed = false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        files = results.get("files", [])
        return files[0] if files else None
    except Exception as e:
        print(f"Error searching file in Google Drive: {e}")
        raise


# Uploads or updates a report file to Google Drive, converting to Google Sheets format
def upload_report(service, file_path, parent_folder_id):
    try:
        file_name = file_path.split("\\")[-1]
        existing_file = find_report(service, file_name, parent_folder_id)
        media = MediaFileUpload(file_path, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        if existing_file:
            file_id = existing_file["id"]
            service.files().update(fileId=file_id, media_body=media).execute()
            print(f"File updated: {file_name} (ID: {file_id})")
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
            print(f"File uploaded: {file.get('name')} (ID: {file.get('id')})")
    except Exception as e:
        print(f"Error uploading to Google Drive: {e}")
        raise
