from utils.auth import authenticate
from utils.config import source_folder_id
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def list_top_level_folders(service, folder_id):
    try:
        query = f"'{folder_id}' in parents and mimeType = 'application/vnd.google-apps.folder'"
        results = service.files().list(q=query, pageSize=1000, fields="files(id, name)").execute()
        return results.get('files', [])
    except Exception as e:
        logging.error(f"Failed to list top level folders: {e}")

def count_children(service, folder_id):
    try:

        total_count = 0
        query = f"'{folder_id}' in parents"
        results = service.files().list(q=query, pageSize=1000, fields="files(id, mimeType)").execute()
        items = results.get('files', [])
        total_count += len(items)

        for item in items:
            if 'mimeType' in item and item['mimeType'] == 'application/vnd.google-apps.folder':
                total_count += count_children(service, item['id'])

        return total_count
    except Exception as e:
        logging.error(f"Error counting nested items: {e}")

def count_nested_folders(service, folder_id):
    try:
        folder_count = 0
        query = f"'{folder_id}' in parents"
        results = service.files().list(q=query, pageSize=1000, fields="files(id, mimeType)").execute()
        items = results.get('files', [])

        for item in items:
            if 'mimeType' in item and item['mimeType'] == 'application/vnd.google-apps.folder':
                folder_count += 1
                folder_count += count_nested_folders(service, item['id'])

        return folder_count
    except Exception as e:
        logging.error(f"Error counting nested folders in {folder_id}: {e}")
        return None

def generate_report(service, folder_id):
    try:
        top_level_folder = list_top_level_folders(service, folder_id)
        report = []

        for folder in top_level_folder:
            count = count_children(service, folder['id'])
            report.append((folder['name'], count))
        return report
    except Exception as e:
        logging.error(f"Failed to generate report: {e}")

def main():
    try:        
        service = authenticate()
        report = generate_report(service, source_folder_id)

        for folder_name, count in report:
            logging.info(f"{folder_name} has {count} objects")

        total_nested_folders = count_nested_folders(service, source_folder_id)
        logging.info(f"Total nested folders in the source folder: {total_nested_folders}")
    except Exception as e:
        logging.error(f"Error generating report: {e}")

if __name__ == '__main__':
    main()