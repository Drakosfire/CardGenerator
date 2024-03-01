import item_dict_gen as igen 
import img2img 
import card_generator as card
import utilities as u
import ctypes
import user_input as useri
import gradio as gr
from gradio import State
import sys

# This is a fix for the way that python doesn't release system memory back to the OS and it was leading to locking up the system
libc = ctypes.cdll.LoadLibrary("libc.so.6")
M_MMAP_THRESHOLD = -3

# Set malloc mmap threshold.
libc.mallopt(M_MMAP_THRESHOLD, 2**20)
initial_name = "A Crowbar"


    


with gr.Blocks() as app:
    # Title
    gr.HTML(""" <div id="inner"> <header>
    <h1>Item Card Generator</h1>
                </div>""")
    
    

    with gr.Row():
# What is working is create a variable that is gr.State() which can be updated and moves around the program
        # Build functions W/in the Gradio format, because it only allows modification within it's context
        #define inputs to match what is called on click, and output of the function as a list that matches the list of outputs
        textbox_default_dict = {'Name':'', \
                                'Type': '',
                                'Rarity':'',
                                'Value':'',
                                'Properties':'',
                                'Damage':'',
                                'Weight':'',
                                'Description':'',
                                'Quote':'',
                                'SD Prompt':''
                                }
        
        item_name_var = gr.State()
        item_type_var = gr.State()
        item_rarity_var = State()
        item_value_var = State()
        item_properties_var = State()
        item_damage_var = State()
        item_weight_var = State()
        item_description_var = State()
        item_quote_var = State()
        item_sd_prompt_var = gr.State('')
        selected_border_image = gr.State('./card_templates/Moonstone Border.png')
        num_image_to_generate = gr.State(4)
        mimic = None

        def set_textbox_defaults(textbox_default_dict, key):
            item_name = textbox_default_dict[key]
            return item_name

        # Function called when user generates item info, then assign values of dictionary to variables, output once to State, twice to textbox
        def generate_text_update_textboxes(user_input):
            llm_output=useri.call_llm(user_input)
            item_name = llm_output[user_input]['Name']
            item_type = llm_output[user_input['Type']]
            item_rarity = llm_output[user_input]['Rarity']            
            item_value = llm_output[user_input]['Value']
            item_properties = llm_output[user_input['Properties']]
            item_damage = llm_output[user_input]['Damage']
            item_weight = llm_output[user_input]['Weight']
            item_description = llm_output[user_input['Description']]
            item_quote = llm_output[user_input]['Quote']    

            sd_prompt = llm_output[user_input]['SD Prompt']
            return [item_name, item_name,
                    item_type, item_type,
                    item_rarity, item_rarity,
                    item_value, item_value,
                    item_properties, item_properties,
                    item_damage, item_damage,
                    item_weight, item_weight,
                    item_description, item_description,
                    item_quote, item_quote,
                    sd_prompt, sd_prompt]
        # Function called on user selecting an image from the gallery, outputs the path of the image
        def assign_img(evt: gr.SelectData):  
             
            img_dict = evt.value
            selected_border_path = img_dict['image']['url']
            print(selected_border_path)
            return selected_border_path
            
                
        user_input =  gr.Textbox(label = 'What is the item?', lines =1, placeholder= "A Crowbar", elem_id= "Item")
        item_text_generate = gr.Button(value = "Generate my item text")
        with gr.Column(scale = 1):          
            
            item_name_output = gr.Textbox('Item Values', value = set_textbox_defaults(textbox_default_dict, 'Name'), lines = 1, interactive=True, elem_id='Item Name')
            item_type_output = gr.Textbox(value = set_textbox_defaults(textbox_default_dict, 'Type'), lines = 1, interactive=True, elem_id='Item Type')
            item_rarity_output = gr.Textbox(value = set_textbox_defaults(textbox_default_dict, 'Rarity'), lines = 1, interactive=True, elem_id='Item Rarity')
            item_value_output = gr.Textbox(label = 'Item Name', value = set_textbox_defaults(textbox_default_dict, 'Rarity'), lines = 1, interactive=True, elem_id='Item Type')
            sd_prompt_output = gr.Textbox(label = 'Image Generation Prompt', value = set_textbox_defaults(textbox_default_dict, 'SD Prompt'), lines = 1, interactive=True, elem_id='SD Prompt')
            llm_output = item_text_generate.click(generate_text_update_textboxes, 
                                                  inputs = [user_input], 
                                                  outputs= [item_name_var, 
                                                            item_name_output, 
                                                            sd_prompt_var,
                                                            sd_prompt_output])          
            
            
    border_gallery = gr.Gallery(label = "Card Templates", 
                                value = useri.paths_of_card_templates_list,
                                show_label = False,
                                elem_id = "template gallery",
                                columns = [5], rows = [4],
                                object_fit = "contatin",
                                height = "auto")
    
    border_gallery.select(assign_img, outputs = selected_border_image)
    card_gen = gr.Button(value = "Generate my card", elem_id="Generate Card Button")
    # Pass the user input and border tempalte to the generator
    card_gen.click(fn = img2img.generate_image, inputs =[num_image_to_generate,sd_prompt_var,item_name_var,selected_border_image])

if __name__ == '__main__':
    app.launch(server_name = "0.0.0.0", server_port = 8000, share = False, allowed_paths = ["/media/drakosfire/Shared/"])
        







    


   


