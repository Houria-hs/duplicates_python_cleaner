from __future__ import print_function
import os
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import smtplib
from email.message import EmailMessage

SCOPES = ['https://www.googleapis.com/auth/drive']

def list_files_recursive(service, folder_id):
    files = []

    def list_folder(fid):
        query = f"'{fid}' in parents"
        results = service.files().list(
            q=query,
            pageSize=1000,
            fields="files(id, name, mimeType, md5Checksum)"
        ).execute()

        items = results.get('files', [])
        for item in items:
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                list_folder(item['id'])
            else:
                files.append(item)

    list_folder(folder_id)
    return files

def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    folder_id = '1ko86lS8OlSLLzBK71KG7Y2sqnVpCJY83'
    items = list_files_recursive(service, folder_id)

    seen_md5 = {}
    duplicates = []

    protected_extensions = ['.exe', '.bat', '.py']
    protected_names = ['__pycache__', '.git']

    for file in items:
        name = file['name']
        md5 = file.get('md5Checksum')

        if any(name.endswith(ext) for ext in protected_extensions):
            print(f"Skipping protected file (extension): {name}")
            continue
        if any(protected in name for protected in protected_names):
            print(f"Skipping protected file (name): {name}")
            continue

        if not md5:
            print(f"Skipping {name}: no MD5 checksum (can’t safely check duplicate)")
            continue

        if md5 in seen_md5:
            duplicates.append(file)
        else:
            seen_md5[md5] = file['id']

    if duplicates:
        print(f"Found {len(duplicates)} duplicates.")
        confirm = input("Delete duplicates? (yes/no): ")
        if confirm.lower() == "yes":
            deleted_files = []
            for dup in duplicates:
                try:
                    service.files().delete(fileId=dup['id']).execute()
                    print(f"Deleted: {dup['name']} ({dup['id']})")
                    deleted_files.append(dup['name'])
                except Exception as e:
                    print(f"Failed to delete {dup['name']}: {e}")

            if deleted_files:
                msg = EmailMessage()
                msg['Subject'] = 'Duplicate files deleted'
                msg['From'] = 'Python_duplicates_remover'
                msg['To'] = 'houriahasbell@gmail.com'
                msg.set_content(f"The following files were deleted because they were duplicates:\n\n" + "\n".join(deleted_files))

                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    app_password = os.getenv("EMAIL_APP_PASSWORD")
                    if not app_password:
                        raise ValueError("EMAIL_APP_PASSWORD is not set in environment variables.")
                    smtp.login('houriahasbell@gmail.com', app_password)
                    smtp.send_message(msg)
        else:
            print("No files deleted.")
    else:
        print('No duplicates found.')

if __name__ == '__main__':
    main()


