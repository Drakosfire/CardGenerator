from io import BytesIO
import requests
import os
from PIL import Image



image_list = []
# Utility Functions to be called from all modules

# Function to convert a string to a dictionary
def string_to_dict(string):
    return eval(string)

# Function to return a list of keys of a nested dictionary using it's key value (item or creature)
def keys_list(dict, index):
    keys_list=list(dict.keys())
    return keys_list[index]

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
            if file_path != ".keep":
                try:
                    os.remove(f"./image_temp/{file_path}")
                    print(f"Remove : ./image_temp/{file_path}")
                except OSError as e:
                    print(f"Error: {file_path} : {e.strerror}")
        file_paths.clear()
            

def open_image_from_url(url):
    try:
        print(f"Opening image from URL: {url}")
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        if 'image' not in response.headers.get('content-type', ''):
            raise ValueError("URL does not point to an image")
        image_data = BytesIO(response.content)
        image = Image.open(image_data)
        return image
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        raise
    except ValueError as e:
        print(f"Invalid image URL: {e}")
        raise
    except Image.UnidentifiedImageError as e:
        print(f"Cannot identify image file: {e}")
        raise

def receive_upload(image_file):
        
    image = Image.open(image_file[0][0])

    print(image)
    return image

example_image_urls = ["https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/a2f5fcea-1b16-4dc7-1874-3688bf66f900/public",
                      "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/6f37d2ce-74aa-4d4f-c8fd-d2145f6bc700/public",
                      "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/8829b2aa-834b-48c2-c4bb-7f4907ced200/public",
                      "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/f10cbb4f-a00b-480f-38ca-1e3d816c5700/public",
                      "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/29dfd4d3-176e-41d4-d69d-36f3d98e6600/public",
                      "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/d8bf9bf2-6a6a-4451-5ff6-01bd7e36e200/public",
                      "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/ae6cb0e0-d91f-428c-7632-c3f1dea26b00/public",
                      "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/aeb68105-04fe-42ec-df9d-e232b29d0400/public",
                      "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/3df60f6d-9bc9-40de-a028-169d64319400/public",
                      "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/47f79b37-f43a-419f-99d6-5f8f60ba4100/public",
                      "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/6184f9fd-2374-48ec-0bc8-3da2559d8300/public",
                      "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/567b2937-956f-4d74-7321-55f7640b3e00/public",
                      "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/a6d03d18-4202-4e69-4a2d-7c948caa9000/public",
                      "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/7b479f54-94e3-40b5-c214-5de7d56f4a00/public",
                      "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/56ce102c-6186-46ad-594a-5861d69e6500/public",
                      "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/907fde65-9de0-4f77-e370-f80b37818800/public",
                      "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/211b4598-e29a-4947-0b30-6355ca45ea00/public",
                      "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/271b4e40-1a5f-49fc-eeb3-bfe26be80700/public",
                      "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/1d0d09c9-56ae-4323-b8b7-57e60b697d00/public"

]

card_border_urls = ["https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/90293844-4eec-438f-2ea1-c89d9cb84700/public",
                    "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/54d94248-e737-452c-bffd-2d425f803000/public",
                    "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/d0872a5e-91a0-41f8-f819-3d1a0931c900/public",
                    "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/8c113608-2389-4588-2090-d0192c539b00/public",
                    "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/e6253513-b33d-4d9c-1631-38cc46199d00/public",
                    "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/879e240e-4491-42de-8729-5f8899841e00/public",
                    "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/56e91eca-d530-483f-4b62-277486097200/public",
                    "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/5fdfd8cd-51c3-4dde-2d3f-f1b463f05200/public"                  

]

