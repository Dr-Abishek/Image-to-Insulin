from azure.storage.blob import BlobServiceClient
import streamlit as st

def get_blob():
  #blob = BlobClient(account_url="https://abishekimage2insulin.blob.core.windows.net",
                   #container_name="food-image-dataset",
                  # blob_name=blob_name,
                    #credential="7aZbmTQutOM7HrpUi7Fjxb6jhQpHQsD+8PTLtRoTYk6zLmn6iA7T7feOHxLwulkfYwFTY1hxLfl++ASt09srdw==")
  blob_service = BlobServiceClient(account_name='abishekimage2insulin', account_key='7aZbmTQutOM7HrpUi7Fjxb6jhQpHQsD+8PTLtRoTYk6zLmn6iA7T7feOHxLwulkfYwFTY1hxLfl++ASt09srdw==')
  return(blob_service)
