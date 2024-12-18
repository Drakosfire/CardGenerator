import item_dict_gen as igen 
import img2img 
import card_generator as card
import utilities as u
import sys

image_path = str
end_phrase = """<|end_of_turn|>"""
# Indexing the contents of Card templates and temp images
card_template_path = "./card_templates/"
temp_image_path = "./image_temp"



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
    response = u.string_to_dict(llm_call)
    print(f"response = {response}")

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
        
        user_input_template = user_pick_item(user_pick_template_prompt)
        response = call_llm(user_input_item)        
        print(response[u.keys_list(response,0)])
        output_dict = response[u.keys_list(response,0)]
        item_name = response[u.keys_list(response,0)]['Name']
        sd_prompt = response[u.keys_list(response,0)]['SD Prompt']    
        image_path = img2img.generate_image(4,sd_prompt,item_name,user_input_template, mimic)
        user_card_image = user_pick_item(user_pick_image_prompt, image_path)
        
        print(image_path)
        
        card.render_text_on_card(user_card_image, output_dict)
        u.delete_files(u.image_list)





