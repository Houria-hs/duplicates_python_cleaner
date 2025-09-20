# Music Duplicate Cleaner
---
A simple Python tool that scans a Google Drive folder, finds duplicate music files by comparing their md5Checksum, and deletes the duplicates safely.
Optionally, it sends an email notification with the deleted file list.
---

🚀 Features
🔍 Recursively scans a Google Drive folder and subfolders.
🗂️ Detects duplicate files by comparing MD5 checksums.
✅ Skips protected files (.exe, .bat, .py) and system folders (__pycache__, .git).
🗑️ Deletes duplicates only with user confirmation.
📧 Sends an email with a summary of deleted files.
📝 Logs all actions in scan_log.txt.
---

⚙️ How It Works
Authenticates with Google Drive using OAuth.
Recursively lists all files inside the specified folder.
Checks files’ MD5 checksums to find duplicates.
If duplicates are found:
Asks you to confirm deletion.
Deletes only the duplicates (keeps one original).
Sends you an email report.
Creates a detailed log file for every run.
---

📌 Requirements
Python 3.x
Google Drive API enabled in your Google Cloud project.
credentials.json file from Google Cloud OAuth consent screen.
token.json will be created on first run.
Google App Password (if using Gmail to send email).
---

🛠️ Setup
1️⃣ Clone the repository:
git clone https://github.com/yourusername/music-duplicate-cleaner.git
cd music-duplicate-cleaner
---

2️⃣ Create a virtual environment and activate it:
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate
---

3️⃣ Install dependencies:
pip install -r requirements.txt
---

4️⃣ Add your credentials.json to the project root.
Make sure the Google Drive API is enabled in your Google Cloud project.
---

5️⃣ Create .env file:
EMAIL_APP_PASSWORD=your_app_password_here
FOLDER_ID=your_drive_folder_id_here
---

▶️ Usage
Run the script:
python check_duplicates.py
Open the provided Google auth URL and log in.
Confirm the files you want to delete when asked.
Check scan_log.txt for a detailed report.

⚠️ Important
Always run a test first.
Check the log before confirming deletion.
Deleted files go to Google Drive trash — they can be restored from there if needed.
Keep your credentials and app password safe.
 
