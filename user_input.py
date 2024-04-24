import item_dict_gen as igen 
import img2img 
import card_generator as card
import utilities as u
import sys
import tempfile
from PIL import Image
from github import Github

image_path = str
end_phrase = """<|end_of_turn|>"""
# Indexing the contents of Card templates and temp images
card_template_path = "./card_templates/"
temp_image_path = "./image_temp"

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

user_pick_template_prompt = "Pick a template number from this list : "
user_pick_image_prompt = "Select an image : "

# Check if the user wants to exit the chatbot

def user_exit_question(user_input):
    if user_input.lower() in ['exit', 'quit']:
        print("Chatbot session ended.")
        sys.exit()
# Process the list of files in the card_template directory and print with corresponding numbers to index    
def process_list_for_user_response(list_of_items):
    x = 0
    for item in list_of_items:
        print(f"{x} : {item}")
        x += 1

def user_pick_item(user_prompt,list_of_items):
    process_list_for_user_response(list_of_items)
    user_input = input(user_prompt)
    # Check if the user wants to exit the chatbot
    user_exit_question(user_input)
    return list_of_items[int(user_input)]

def call_llm(user_input):
    # Process the query and get the response
    llm_call = igen.call_llm_and_cleanup(user_input)
    response = llm_call
        
        # Find the index of the phrase
    index = response.find(end_phrase)
    print(f"index = {index}")
    if index != -1:
        # Slice the string from the end of the phrase onwards
        response = response[index + len(end_phrase):]
    else:
        # Phrase not found, optional handling
        response = response
    
    response = response.replace("GPT4 Assistant: ", "")
    print(response)
    response = igen.convert_to_dict(response)
    if not response:
        response = call_llm(user_input)
    del llm_call
    return response

def prompt_user_input():
    mimic = None
    while True:
        user_input_item = input("Provide an item : ")
        user_exit_question(user_input_item) 
            
        if 'mimic' in user_input_item.lower():
            mimic = True

        #user_input_template = input(f"Pick a template number from this list : {process_list_for_user_response(list_of_card_templates)}")
        
        user_input_template = user_pick_item(user_pick_template_prompt,list_of_card_templates)
        response = call_llm(user_input_item)        
        print(response[u.keys_list(response,0)])
        output_dict = response[u.keys_list(response,0)]
        u.reclaim_mem()
        item_name = response[u.keys_list(response,0)]['Name']
        sd_prompt = response[u.keys_list(response,0)]['SD Prompt']    
        image_path = img2img.generate_image(4,sd_prompt,item_name,user_input_template, mimic)
        user_card_image = user_pick_item(user_pick_image_prompt, image_path)
        
        print(image_path)
        
        card.render_text_on_card(user_card_image, output_dict)
        u.delete_files(img2img.image_list)





