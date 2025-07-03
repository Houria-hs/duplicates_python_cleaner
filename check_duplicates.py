
from __future__ import print_function
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build 
import smtplib
from email.message import EmailMessage
import os

SCOPES = ['https://www.googleapis.com/auth/drive']

def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=1000, fields="nextPageToken, files(id, name, md5Checksum)").execute()
    items = results.get('files', [])
    # if not items:
    #     print('No files found.')
    # else:
    #     print('Files:')
    #     for item in items:
    #         print(f"{item['name']} ({item['id']})")
    
    seen = {}
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
        key = (name , md5)
        if key in seen:
            duplicates.append(file)
        else:
            seen[key] = file['id']
    if duplicates:
        confirm = input("Delete duplicates? (yes/no): ")
        if confirm.lower() == "yes":
            deleted_files = []
            for dup in duplicates:
                file_id = dup['id']
                try:
                    service.files().delete(fileId=file_id).execute()
                    print(f"Deleted: {dup['name']} ({file_id})")
                    deleted_files.append(dup['name'])  
                except Exception as e:
                    print(f"Failed to delete {dup['name']}: {e}")
            
            if deleted_files:
                #create the email
                msg = EmailMessage()
                msg['Subject'] = 'Duplicate files deleted'
                msg['From'] = 'Python_duplicates_remover'
                msg['To'] = 'houriahasbell@gmail.com'
                msg.set_content(f"The following files were deleted because they were duplicates:\n\n" + "\n".join(deleted_files))
    
                # Send via Gmail SMTP
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                    smtp.login('houriahasbell@gmail.com', os.getenv("EMAIL_APP_PASSWORD"))
                    smtp.send_message(msg)
        else:
            print("No files deleted.")
    else:
        print('no duplicate founds')
if __name__ == '__main__':
    main()

