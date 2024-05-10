# Create a list of hashmap key values .
import torch
import time
import gc
from io import BytesIO
import requests
import os
from PIL import Image
from github import Github
# Utility Functions to be called from all modules

# Function to return a list of keys of a nested dictionary using it's key value (item or creature)
def keys_list(dict, index):
    keys_list=list(dict.keys())
    return keys_list[index]

# Function to clear model from VRAM to make space for other model
def reclaim_mem():
    
    print(f"Memory before del {torch.cuda.memory_allocated()}")
    torch.cuda.ipc_collect()
    gc.collect()
    torch.cuda.empty_cache()
    time.sleep(0.01)
    print(f"Memory after del {torch.cuda.memory_allocated()}")

#def del_object(object):
 #       del object
  #      gc.collect()

# Create a list of a directory if directory exists
def directory_contents(directory_path):
    if os.path.isdir(directory_path) :
          contents = os.listdir(directory_path)
          return contents
    else : pass

# Delete a list of file 
def delete_files(file_paths):
    if file_paths:
     
        for file_path in file_paths:
            try:
                os.remove(f"./image_temp/{file_path}")
                print(f"Remove : ./image_temp/{file_path}")
            except OSError as e:
                print(f"Error: {file_path} : {e.strerror}")
        file_paths.clear()
    

def open_image_from_url(image_url):
    response = requests.get(image_url)
    image_data = BytesIO(response.content)
    image = Image.open(image_data)
    return image

def receive_upload(image_file):
        
    image = Image.open(image_file[0][0])

    print(image)
    return image

def index_image_paths(repo_name,directory_path):
    g = Github()  # No token needed for public repos
    repo = g.get_repo(repo_name)
    contents = repo.get_contents(directory_path)

    files = []
    for content_file in contents:
        if content_file.type == "file":
            media_url = content_file.download_url.replace("raw.githubusercontent.com", "media.githubusercontent.com/media")
            files.append(media_url)  # Or content_file.path for just the path
    
    return files

