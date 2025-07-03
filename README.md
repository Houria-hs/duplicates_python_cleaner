# Music Duplicate Cleaner

This is a simple Python tool to automatically find and remove duplicate files from a Google Drive account.

## What it does

✅ Connects to Google Drive using OAuth 2.0  
✅ Lists all files
✅ Detects duplicates by name + md5 checksum  
✅ Deletes only duplicates (keeps the original)  
✅ (Planned) Sends an email warning when duplicates are deleted

## How to run

1. Install dependencies
2.  Add your `credentials.json` (Google API credentials).
3. Run
   
 **NOTE:** Never push `credentials.json` or `token.json` to GitHub! They are secrets.
