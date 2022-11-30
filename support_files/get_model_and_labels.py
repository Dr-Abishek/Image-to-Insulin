import os
from azure.storage.blob import BlobServiceClient

def get_blob(blobname='last.pt'):
  blob_service_client = BlobServiceClient(account_url= "https://abishekimage2insulin.blob.core.windows.net",
                                          credential="7aZbmTQutOM7HrpUi7Fjxb6jhQpHQsD+8PTLtRoTYk6zLmn6iA7T7feOHxLwulkfYwFTY1hxLfl++ASt09srdw==")
  return (blob_service_client)



def download_blob(blob_name_list):
    blob_service_client = get_blob()
    container_client = blob_service_client.get_container_client(container= "food-image-dataset")
    blob_list = container_client.list_blobs()
    
    for blob in blob_list:
        if blob.name in blob_name_list :
            local_path = ""
            local_file_name = blob.name
            container_name= "food-image-dataset"
            download_file_path = os.path.join(local_path, str.replace(local_file_name ,'.txt', 'DOWNLOAD.txt'))
            container_client = blob_service_client.get_container_client(container= container_name) 
            with open(file=download_file_path, mode="wb") as download_file:
             download_file.write(container_client.download_blob(blob.name).readall())
