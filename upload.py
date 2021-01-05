# SETUP INSTRUCTIONS:
# Ensure Python 3.7+ is installed.
# Follow the steps here to install and activate the virtual env using venv:
# https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/
# Then run `pip install -r requirements.txt`
# Uses either command line arguments or variables defined in config.yml file for configuration.

import os, re
import yaml
import argparse
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

# define optional command line arguments using argparse
parser = argparse.ArgumentParser(description='UPLOAD.PY //// Upload generated video clips to Azure blob storage.')
parser.add_argument('--source_directory', nargs='?', help='the full path to the directory containing the videos to upload.')
parser.add_argument('--azure_connection_string', nargs='?', help='your Azure storage connection string.')
parser.add_argument('--video_file_extension', nargs='?', help='the file extension of the files to be uploaded.')
parser.add_argument('--azure_container_name', nargs='?', help='the Azure container name.')
parser.add_argument('--unique_clip_id', nargs='?', help='the unique id to search for in each video clip name.')
args = parser.parse_args()

# get YAML config.yml file settings, accessed using cfg[key][subkey]
file = open('config.yml', 'r')
cfg = yaml.load(file, Loader= yaml.FullLoader)

# set up variables (command line overrides config.yml)
azure_connection_string = args.azure_connection_string or cfg['upload']['azure']['connection_string']
azure_container_name = args.azure_container_name or cfg['upload']['azure']['container_name']
source_directory = args.source_directory or cfg['upload']['source_directory']
video_file_extension = args.video_file_extension or cfg['shared']['video_file_extension']
unique_clip_id = args.unique_clip_id or cfg['upload']['unique_clip_id']

try:
    # connect to Azure container
    blob_service_client = BlobServiceClient.from_connection_string(azure_connection_string)
    num_uploaded_files = 0

    # scan root directory for files with correct extension
    for root, subdirs, files in os.walk(source_directory):
        for filename in files:
            # check file for correct file type
            if re.match(rf"^.*{unique_clip_id}.*\.{video_file_extension}", filename, re.IGNORECASE):
                print(f'Uploading file {filename} to Azure storage.')
                # get full file path
                full_path = os.path.join(root, filename)
                # upload video file to container specified in configuration file
                blob_client = blob_service_client.get_blob_client(container=azure_container_name, blob=filename)
                with open(full_path, 'rb') as data:
                    blob_client.upload_blob(data, overwrite=True)
                num_uploaded_files += 1

            print(f'Uploaded file {filename} successfully.')
    if num_uploaded_files == 0:
        raise Exception(f'No files with id: {unique_clip_id} found to upload. Render must have failed.')
    else:
        print('Uploaded all files successfully.')

except Exception as ex:
    print('Error uploading video file:')
    print(ex)
    raise Exception(f'Error uploading media: {ex}')
