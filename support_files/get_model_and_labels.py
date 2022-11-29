from azure.storage.blob import BlobServiceClient
import streamlit as st
from github import Github

def get_blob(blob_name):
  blob = BlobClient(account_url="https://abishekimage2insulin.blob.core.windows.net",
                    container_name="food-image-dataset",
                    blob_name=blob_name,
                    credential="7aZbmTQutOM7HrpUi7Fjxb6jhQpHQsD+8PTLtRoTYk6zLmn6iA7T7feOHxLwulkfYwFTY1hxLfl++ASt09srdw==")
  #blob_service = BlobServiceClient(account_name='abishekimage2insulin', account_key='7aZbmTQutOM7HrpUi7Fjxb6jhQpHQsD+8PTLtRoTYk6zLmn6iA7T7feOHxLwulkfYwFTY1hxLfl++ASt09srdw==')
  return(blob)

def blob_to_git():
    g = Github("Dr-Abishek", "Abi@github1")
    GITHUB_REPO = "https://github.com/Dr-Abishek/Image-to-Insulin"
    repo = g.get_user().get_repo(GITHUB_REPO)
    all_files = []
    contents = repo.get_contents("")
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            contents.extend(repo.get_contents(file_content.path))
        else:
            file = file_content
            all_files.append(str(file).replace('ContentFile(path="','').replace('")',''))

    #with open('/tmp/file.txt', 'r') as file:
        #content = file.read()
    blob_container = 'food-image-dataset'
    try:
        last = get_blob('last.pt')
        labels = get_blob('custom.yaml')
        st.success(type(blob))
        st.success("Success getting Blob service")
    except:
        st.warning("Unable to download blob")
        
    # Upload to github
    git_prefix = ''
    git_file = git_prefix + 'last.pt'
    if git_file in all_files:
        contents = repo.get_contents(git_file)
        repo.update_file(contents.path, "committing files", last, contents.sha, branch="master")
        st.success(git_file + ' UPDATED')
    else:
        repo.create_file(git_file, "committing files", last, branch="master")
        st.success(git_file + ' CREATED')
