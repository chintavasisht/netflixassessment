from utils.auth import authenticate
from utils.config import source_folder_id, destination_folder_id
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def list_files_in_folder(service, folder_id):
    try:
        query = f"'{folder_id}' in parents"
        results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
        return results.get('files', [])
    except Exception as e:
        logging.error(f"Error listing files in folder '{folder_id}': {e}")

def copy_file(service, file_id, file_name, destination_folder_id):
    query = f"'{destination_folder_id}' in parents and name='{file_name}' and trashed = false"
    results = service.files().list(q=query, fields="files(id, name)").execute()
    files = results.get('files', [])

    if files:
        logging.info(f"File '{file_name}' already exists with ID: {files[0]['id']}")
    else:
        try:
            file_metadata = {
                'parents': [destination_folder_id],
                'name': [file_name]
            }
            copied_file = service.files().copy(fileId=file_id, body=file_metadata).execute()
            logging.info(f"Copied file ID: {copied_file.get('id')}")
        except Exception as e:
            print(f"Failed to copy file: {e}")

def create_folder(service, name, parent_folder_id):
    try:
        query = f"'{parent_folder_id}' in parents and mimeType='application/vnd.google-apps.folder' and name='{name}' and trashed = false"
        results = service.files().list(q=query, fields="files(id, name)").execute()
        folders = results.get('files', [])

        if folders:
            logging.info(f"Folder '{name}' already exists with ID: {folders[0]['id']}")
            return folders[0]['id']
        else:
            folder_metadata = {
                'name': name,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [parent_folder_id]
            }
            folder = service.files().create(body=folder_metadata, fields='id').execute()
            print(f"Created new folder '{name}' with ID: {folder.get('id')}")
            return folder.get('id')
    except Exception as e:
        logging.error(f"Failed to create folder '{name}': {e}")
        return None

def copy_folder_contents(service, source_folder_id, destination_folder_id):
    try:
        items = list_files_in_folder(service, source_folder_id)
        for item in items:
            if item['mimeType'] == 'application/vnd.google-apps.folder':
                new_folder_id = create_folder(service, item['name'], destination_folder_id)
                copy_folder_contents(service, item['id'], new_folder_id)
            else:
                copy_file(service, item['id'], item['name'], destination_folder_id)
    except Exception as e:
        logging.error(f"Error copying folder contents from '{source_folder_id}' to '{destination_folder_id}': {e}")

def main():
    try:
        service = authenticate()
        copy_folder_contents(service, source_folder_id, destination_folder_id)
    except Exception as e:
        logging.error(f"Failed to complete the copy operation: {e}")

if __name__ == '__main__':
    main()
