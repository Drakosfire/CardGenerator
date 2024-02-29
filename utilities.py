# Create a list of hashmap key values .
import torch
import time
import gc
import os

# Utility Functions to be called from all modules

# Function to return a list of keys of a nested dictionary using it's key value (item or creature)
def keys_list(dict, index):
    keys_list=list(dict.keys())
    return keys_list[index]

def reclaim_mem():
    
    print(f"Memory before del {torch.cuda.memory_allocated()}")
    torch.cuda.ipc_collect()
    gc.collect()
    torch.cuda.empty_cache()
    time.sleep(0.01)
    print(f"Memory after del {torch.cuda.memory_allocated()}")

def del_object(object):
        del object
        gc.collect()

def directory_contents(directory_path):
    if os.path.isdir(directory_path) :
          contents = os.listdir(directory_path)
          return contents
    else : pass

def delete_files(file_paths):
     
    for file_path in file_paths:
        try:
            os.remove(file_path)
        except OSError as e:
            print(f"Error: {file_path} : {e.strerror}")
    file_paths.clear()