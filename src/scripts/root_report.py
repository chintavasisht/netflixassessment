from utils.auth import authenticate
import logging
from utils.config import source_folder_id

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def report_total_items(service, folder_id):
    try:
        query = f"'{folder_id}' in parents and trashed = false"
        results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
        files = results.get('files', [])
        total_files = len([file for file in files if file['mimeType'] != 'application/vnd.google-apps.folder'])
        total_folders = len([file for file in files if file['mimeType'] == 'application/vnd.google-apps.folder'])
        logging.info(f"Total files: {total_files}, Total folders: {total_folders}")
    except Exception as e:
        logging.error(f"Error reporting total items in folder '{folder_id}': {e}")


def main():
    try:
        service = authenticate()
        report_total_items(service, source_folder_id)
    except Exception as e:
        logging.error(f"Failed to generate root report: {e}")

if __name__ == '__main__':
    main()

