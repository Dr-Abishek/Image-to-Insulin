import os
from azure.storage.blob import BlobServiceClient

def get_blob():
  blob_service_client = BlobServiceClient(account_url= "https://abishekimage2insulin.blob.core.windows.net",
                                          credential="7aZbmTQutOM7HrpUi7Fjxb6jhQpHQsD+8PTLtRoTYk6zLmn6iA7T7feOHxLwulkfYwFTY1hxLfl++ASt09srdw=="
                                         )
  return (blob_service_client)



def download_blob_from_azure(blob_name_list):
    blob_service_client = BlobServiceClient(account_url= "https://abishekimage2insulin.blob.core.windows.net",
                                          credential="7aZbmTQutOM7HrpUi7Fjxb6jhQpHQsD+8PTLtRoTYk6zLmn6iA7T7feOHxLwulkfYwFTY1hxLfl++ASt09srdw=="
                                         )
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
            
def upload_blob_to_azure(blob,type_of_blob,user_id):
    blob_service_client = BlobServiceClient(account_url= "https://abishekimage2insulin.blob.core.windows.net",
                                            credential="7aZbmTQutOM7HrpUi7Fjxb6jhQpHQsD+8PTLtRoTYk6zLmn6iA7T7feOHxLwulkfYwFTY1hxLfl++ASt09srdw=="
                                           )
    container_name= "food-image-dataset"
    blob_name = ""
    if type_of_blob == "img":
      blob_name = "temp_img_"+str(user_id)+".jpg"
    else:
      blob_name = "temp_txt_"+str(user_id)+".txt"
    blob_client = blob_service_client.get_blob_client(container=container_name, blob = blob_name)
    #with open(file=blob, mode="rb") as data:
    blob_client.upload_blob(blob, ,overwrite=True)
