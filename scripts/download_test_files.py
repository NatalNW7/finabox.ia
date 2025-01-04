import os
from base64 import b64decode
from json import loads

from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
TEMP = 'temp'
SERVICE_ACCOUNT_FILE = os.path.join(TEMP, 'service_account.json')


def load_files_info():
    encoded_files_info = os.getenv('FILES_INFO')
    if not encoded_files_info:
        raise ValueError("FILES_INFO' not found.")

    return loads(b64decode(encoded_files_info))


def create_service_account_file():
    if os.path.exists(SERVICE_ACCOUNT_FILE):
        return

    encoded_credentials = os.getenv('GDRIVE_INFO')
    if not encoded_credentials:
        raise ValueError("'GDRIVE_INFO' not found.")

    with open(SERVICE_ACCOUNT_FILE, 'wb') as f:
        f.write(b64decode(encoded_credentials))


def auth_on_gdrive_api():
    create_service_account_file()
    creds = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    return build('drive', 'v3', credentials=creds)


def download_file(service, file_id, destination):
    try:
        request = service.files().get_media(fileId=file_id)
        with open(destination, 'wb') as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f'Download Progress: {int(status.progress() * 100)}%')
        print(f'File saved: {destination}')
    except Exception as e:
        raise Exception(f'An error occurred while downloading file: {e}')


def main():
    os.makedirs(TEMP, exist_ok=True)
    files = load_files_info()
    googledrive_service = auth_on_gdrive_api()

    for file in files:
        file_id = file['file_id']
        destination = os.path.join(TEMP, file['name'])
        if os.path.exists(destination):
            print(f'File already exists: {destination}')
            continue
        download_file(googledrive_service, file_id, destination)


if __name__ == '__main__':
    main()
