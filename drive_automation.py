import os
from googleapiclient.http import MediaIoBaseDownload
from google_service import Create_Service # Assuming 'google_service.py' is in the same directory

def main():
    service = drive_service()

    main_folder_id = input('Insert your folder ID: ')

    download_path = "D:\mauri\Downloads" # Carpeta donde se guardarán todos los archivos descargados
    if not os.path.exists(download_path):
        os.makedirs(download_path)

    download_recursive(service, main_folder_id, download_path)

    print("Download Complete.")

def download_recursive(service, folder_id, download_path):
    response = service.files().list(q=f"'{folder_id}' in parents",
                                    fields='files(id,name,mimeType)').execute()

    files = response.get('files', [])

    for file in files:
        file_id = file['id']
        file_name = file['name']
        file_type = file['mimeType']

        file_path = os.path.join(download_path, file_name)

        if file_type == 'application/vnd.google-apps.folder':
            # Si es una carpeta, descarga recursivamente su contenido
            subfolder_path = os.path.join(download_path, file_name)
            if not os.path.exists(subfolder_path):
                os.makedirs(subfolder_path)
            download_recursive(service, file_id, subfolder_path)
        else:
            # Si es un archivo, descárgalo
            if not os.path.exists(file_path):
                request = service.files().get_media(fileId=file_id)
                with open(file_path, 'wb') as fh:
                    downloader = MediaIoBaseDownload(fh, request)
                    done = False
                    while not done:
                        status, done = downloader.next_chunk()
                        print(f"Downloading {file_name}... {int(status.progress() * 100)}% completed.")
            else:
                print(f"The file {file_name} already exists, skipping download")


def drive_service():
    client_secret_file = 'client_secret_GoogleCloudDemo.json'
    api_name = 'drive'
    api_version = 'v3'
    scopes = ['https://www.googleapis.com/auth/drive']

    service = Create_Service(client_secret_file, api_name, api_version, scopes)

    return service 

if __name__ == "__main__":
    main()

