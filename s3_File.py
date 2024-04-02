import boto3
import logging
import os
import json

logger = logging.getLogger(__name__)

AWS_ACCESS_KEY_ID = "AKIATWAVB74RRUPRMTHX"
AWS_SECRET_ACCESS_KEY = "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"

def __create_folder(folder_path):
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)

def remove_file(file_path):
    if os.path.isfile(file_path):
        os.remove(file_path)

# Download s3 file based on bucketname and key.
def download_s3_file(key, folder_extension):
    
    
    file_path = None
    
    folder_path = "downloaded_files"
    folder_path = folder_path + "_" + folder_extension
    __create_folder(folder_path)

    try:
        with open('s3bucket_config.json') as f:
            s3bucket_config = json.loads(f.read())
        bucketname = s3bucket_config["bucketname"]

        s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY) 
        s3_client.download_file(bucketname, key, folder_path + "/" + key.split("/")[-1])
        file_path = folder_path + "/" + key.split("/")[-1]
    
    except Exception as ex:
        #Log Exception
        logger.error("Error occurred when connecting to s3 bucket. Error : " + str(ex))
    
    finally:
        return file_path
    

