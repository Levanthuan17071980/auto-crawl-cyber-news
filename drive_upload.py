import json
import os
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

def upload_to_drive(filename):
    service_account_info = json.loads(
        os.environ["GOOGLE_SERVICE_ACCOUNT"]
    )

    creds = Credentials.from_service_account_info(
        service_account_info,
        scopes=["https://www.googleapis.com/auth/drive.file"]
    )

    service = build("drive", "v3", credentials=creds)

    file_metadata = {"name": filename}
    media = MediaFileUpload(
        filename,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    service.files().create(
        body=file_metadata,
        media_body=media,
        fields="id"
    ).execute()

    print("Upload Google Drive thành công")
