import mimetypes
import os
import tempfile
import zipfile
from google.cloud import storage


def get_media_type(name):
    file_extension = name.split('.')[-1]
    media_type, _ = mimetypes.guess_type(f"file.{file_extension}")
    return media_type

def download_folder_from_firebase(bucket, folder_path):

    blobs = bucket.list_blobs(prefix=folder_path)

    # Download files
    download_folder = tempfile.mkdtemp()
    os.makedirs(download_folder, exist_ok=True)
    for blob in blobs:
        local_file_path = os.path.join(download_folder, blob.name)
        try:
            blob.download_to_filename(local_file_path)
        except Exception as e:
            print(f'Error downloading file {blob.name}: {e}')
        if blob.name.endswith('/'):
            os.makedirs(local_file_path, exist_ok=True)

    # Zip downloaded files
    zip_file_path = os.path.join(download_folder, 'downloaded_files.zip')
    with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
        for root, dirs, files in os.walk(download_folder):
            for file in files:
                file_path = os.path.join(root, file)
                zip_file.write(file_path, os.path.relpath(file_path, download_folder))
    return zip_file_path


def download_folder_from_firebase1(bucket, folder_path: str) -> str:
    temp_dir = tempfile.mkdtemp()

    # Download the entire folder and its contents
    blob_iterator = bucket.list_blobs(prefix=folder_path)
    for blob in blob_iterator:
        # Skip downloading .DS_Store files
        if blob.name.endswith('.DS_Store'):
            continue

        # Construct the local file path to download the blob to
        local_file_path = os.path.join(temp_dir, os.path.relpath(blob.name, folder_path))

        # Print the file path for debugging purposes
        print("Downloading:", local_file_path)

        # If the blob is a directory, create the corresponding directory locally
        if blob.name.endswith('/'):
            os.makedirs(local_file_path, exist_ok=True)
        else:
            # Download the blob to the local file path
            blob.download_to_filename(local_file_path)

    # Create a ZIP archive of the downloaded folder
    zip_file_path = os.path.join(tempfile.gettempdir(), 'folder.zip')
    with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        for folder_name, _, file_names in os.walk(temp_dir):
            for file_name in file_names:
                # Add each file to the ZIP archive
                file_path = os.path.join(folder_name, file_name)
                zip_file.write(file_path, os.path.relpath(file_path, temp_dir))

    # Clean up the temporary directory shutil.rmtree(temp_dir)

    return zip_file_path


def download_folder_from_firebase2(bucket, folder_path):
    try:
        # Get a reference to the bucket

        # List all files in the folder
        blob_iterator = bucket.list_blobs(prefix=folder_path)

        # Create a temporary directory to store downloaded files
        temp_dir = tempfile.mkdtemp()

        # Download each file and add it to the ZIP archive
        with zipfile.ZipFile(os.path.join(temp_dir, 'folder.zip'), 'w') as zip_file:
            for blob in blob_iterator:
                # Construct the local file path
                print(blob.name)
                local_file_path = os.path.join(temp_dir, os.path.basename(blob.name))

                # Download the file to the temporary directory
                blob.download_to_filename(local_file_path)

                # Add the downloaded file to the ZIP archive
                zip_file.write(local_file_path, os.path.basename(blob.name))

        # Return the path to the ZIP archive
        print("" + os.path.join(temp_dir, 'folder.zip'))
        return os.path.join(temp_dir, 'folder.zip')
    except Exception as e:
        print("Error:", e)
        return None
