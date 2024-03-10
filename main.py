
import img2img 
import card_generator as card
import utilities as u
import ctypes
import user_input as useri
import gradio as gr
import template_builder as tb



# This is a fix for the way that python doesn't release system memory back to the OS and it was leading to locking up the system
libc = ctypes.cdll.LoadLibrary("libc.so.6")
M_MMAP_THRESHOLD = -3

# Set malloc mmap threshold.
libc.mallopt(M_MMAP_THRESHOLD, 2**20)
initial_name = "A Crowbar"


    


with gr.Blocks() as app:
    
    # Functions and State Variables
    # Build functions W/in the Gradio format, because it only allows modification within it's context
    # Define inputs to match what is called on click, and output of the function as a list that matches the list of outputs
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
    item_rarity_var = gr.State()
    item_value_var = gr.State()
    item_properties_var = gr.State()
    item_damage_var = gr.State()
    item_weight_var = gr.State()
    item_description_var = gr.State()
    item_quote_var = gr.State()
    item_sd_prompt_var = gr.State('')
    selected_border_image = gr.State('./card_templates/Moonstone Border.png')
    num_image_to_generate = gr.State(4)
    generated_image_list = gr.State([])
    selected_generated_image = gr.State()
    selected_seed_image = gr.State()
    built_template = gr.State()
    mimic = None

    def set_textbox_defaults(textbox_default_dict, key):
        item_name = textbox_default_dict[key]
        return item_name
    
    
                
    # Function called when user generates item info, then assign values of dictionary to variables, output once to State, twice to textbox
    def generate_text_update_textboxes(user_input, progress = gr.Progress()):
        u.reclaim_mem()
        
        progress(0, desc = "Thinking")
        # Start the progress simulation in a separate thread
        
        llm_output=useri.call_llm(user_input)
        item_key = list(llm_output.keys())
        
        item_key_values = list(llm_output[item_key[0]].keys())
        item_name = llm_output[item_key[0]]['Name']
        item_type = llm_output[item_key[0]]['Type']
        item_rarity = llm_output[item_key[0]]['Rarity']            
        item_value = llm_output[item_key[0]]['Value']
        item_properties = llm_output[item_key[0]]['Properties']
        
        if 'Damage' in item_key_values: 
            item_damage = llm_output[item_key[0]]['Damage']
        else: item_damage = ''
        item_weight = llm_output[item_key[0]]['Weight']
        item_description = llm_output[item_key[0]]['Description']
        item_quote = llm_output[item_key[0]]['Quote']    

        sd_prompt = llm_output[item_key[0]]['SD Prompt']
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
    
    # Called on user selecting an image from the gallery, outputs the path of the image
    def assign_img(evt: gr.SelectData):          
        img_dict = evt.value
        selected_border_path = img_dict['image']['url']
        return selected_border_path  
    
     # Make a list of files in image_temp and delete them
    def delete_temp_images():
        image_list = u.directory_contents('./image_temp')
        u.delete_files(image_list)
        img2img.image_list.clear()
    
    # Called when pressing button to generate image, updates gallery by returning the list of image URLs
    def generate_image_update_gallery(num_img, sd_prompt,item_name, built_template):
        delete_temp_images()
        print(type(built_template))
        image_list = []
        img_gen, prompt = img2img.load_img_gen(sd_prompt, item_name)
        for x in range(num_img):
            preview = img2img.preview_and_generate_image(x,img_gen, prompt, built_template, item_name)
            image_list.append(preview)
            yield image_list
            #generate_gallery.change(image_list)
        del preview
        u.reclaim_mem()

        #generated_image_list = img2img.generate_image(num_img,sd_prompt,item_name,selected_border)
        return image_list
    
    def build_template(selected_border, selected_seed_image):
        image_list = tb.build_card_template(selected_border, selected_seed_image)
        return image_list, image_list
   

    # Beginning of page format
    # Title
    gr.HTML(""" <div id="inner"> <header>
            <h1>Item Card Generator</h1>
                </div>""")
    with gr.Row():

    # Template Gallery instructions
        gr.HTML(""" <div id="inner"> <header>
                <h3>Step 1 : We need to build a card tempalte, click a border style</h3>
                    </div>""")
        
        gr.HTML(""" <div id="inner"> <header>
                <h3>Step 2 : Click a seed image </h3>
                    </div>""")
    # Holding place for reset button for template builder.
    # reset_button = gr.Button(value = "Reset Template")
    # delete_gallery_button.click(delete_temp_images)

    with gr.Row():
        
        
        border_gallery = gr.Gallery(label = "Card Template Choices", 
                                    value = useri.index_image_paths("./seed_images/card_templates/", "card_templates/"),
                                    show_label = True,
                                    columns = [5], rows = [2],
                                    object_fit = "contain",
                                    height = "auto",
                                    elem_id = "Template Gallery")
        
        border_gallery.select(assign_img, outputs = selected_border_image)

        seed_image_gallery = gr.Gallery(label= "Item Image Seed",
                                        value = useri.index_image_paths("./seed_images/item_seeds/","item_seeds/"),
                                        show_label = True,
                                        columns = [5], rows = [4],
                                        object_fit = "contain",
                                        height = "auto",
                                        elem_id = "Template Gallery") 
        
        built_template_gallery = gr.Gallery(label= "Built Template",
                                        value = None,
                                        show_label = True,
                                        columns = [5], rows = [4],
                                        object_fit = "contain",
                                        height = "auto",
                                        elem_id = "Template Gallery") 
        
        seed_image_gallery.select(assign_img, outputs = selected_seed_image)

    build_card_template_button = gr.Button(value = "Build Card Template")
    build_card_template_button.click(build_template, inputs = [selected_border_image, selected_seed_image], outputs = [built_template_gallery, built_template]) 
        
    gr.HTML(""" <div id="inner"> <header>
                    <h3>Step 3 : Use some words to name your item </h3>
                    </div>""")  
    
    user_input =  gr.Textbox(label = 'What is the item?', lines =1, placeholder= "Spoon of Tasting", elem_id= "Item")
    item_text_generate = gr.Button(value = "Step 3 : Generate my item text, takes about 10 seconds")
    with gr.Row():
        with gr.Column(scale = 1):
    
             # Build text boxes for the broken up item dictionary values
            gr.HTML(""" <div id="inner"> <header>
                    <h3>Step 4 : Review the generated text, edit as desired</h3>
                    </div>""")  
            
            item_name_output = gr.Textbox(value = set_textbox_defaults(textbox_default_dict, 'Name'),label = 'Name', lines = 1, interactive=True, elem_id='Item Name')
            item_type_output = gr.Textbox(value = set_textbox_defaults(textbox_default_dict, 'Type'),label = 'Type', lines = 1, interactive=True, elem_id='Item Type')
            item_rarity_output = gr.Textbox(value = set_textbox_defaults(textbox_default_dict, 'Rarity'),label = 'Rarity : [Common, Uncommon, Rare, Very Rare, Legendary]', lines = 1, interactive=True, elem_id='Item Rarity')
            item_value_output = gr.Textbox(value = set_textbox_defaults(textbox_default_dict, 'Value'),label = 'Value', lines = 1, interactive=True, elem_id='Item Value')
            item_properties_output = gr.Textbox(value = set_textbox_defaults(textbox_default_dict, 'Properties'),label = 'Properties : [List of comma seperated values]', lines = 1, interactive=True, elem_id='Item Properties')
                        
                # Pass the user input and border template to the generator
        with gr.Column(scale = 1):    
            item_damage_output = gr.Textbox(value = set_textbox_defaults(textbox_default_dict, 'Damage'),label = 'Damage', lines = 1, interactive=True, elem_id='Item Damage')
            item_weight_output = gr.Textbox(value = set_textbox_defaults(textbox_default_dict, 'Weight'),label = 'Weight', lines = 1, interactive=True, elem_id='Item Weight')
            item_description_output = gr.Textbox(value = set_textbox_defaults(textbox_default_dict, 'Description'),label = 'Description', lines = 1, interactive=True, elem_id='Item Description')
            item_quote_output = gr.Textbox(value = set_textbox_defaults(textbox_default_dict, 'Quote'),label = 'Quote', lines = 1, interactive=True, elem_id='Item quote')
            item_sd_prompt_output = gr.Textbox(label = 'Image Generation Prompt : (word or phrase : 1.0) is control weight in the generation', value = set_textbox_defaults(textbox_default_dict, 'SD Prompt'), lines = 1, interactive=True, elem_id='SD Prompt')
           
            
            card_gen_button = gr.Button(value = "Step 5 : Generate 4 possible blank cards, takes about 65 seconds", elem_id="Generate Card Button")
           
    # No longer Row Context, in context of entire Block

    generate_final_item_card = gr.Button(value = "Generate my item card!", elem_id = "Generate user card")
    generate_gallery = gr.Gallery(label = "Generated Cards",
                                value = [],
                                show_label= True,
                                scale= 2,
                                columns =[2], rows = [2],
                                object_fit= "fill",
                                height = "768",
                                elem_id = "Generated Cards Gallery"
                                )
    
    card_gen_button.click(fn = generate_image_update_gallery, inputs =[num_image_to_generate,item_sd_prompt_output,item_name_output,built_template], outputs= generate_gallery)
    generate_gallery.select(assign_img, outputs = selected_generated_image)

        # Button logice calls function when button object is pressed, passing inputs and passing output to components
    llm_output = item_text_generate.click(generate_text_update_textboxes, 
                                                inputs = [user_input], 
                                                outputs= [item_name_var, 
                                                        item_name_output,
                                                        item_type_var,
                                                        item_type_output, 
                                                        item_rarity_var,
                                                        item_rarity_output,
                                                        item_value_var,
                                                        item_value_output,
                                                        item_properties_var,
                                                        item_properties_output,
                                                        item_damage_var,
                                                        item_damage_output,
                                                        item_weight_var,
                                                        item_weight_output,
                                                        item_description_var,
                                                        item_description_output,
                                                        item_quote_var,
                                                        item_quote_output,                                                     
                                                        item_sd_prompt_var,
                                                        item_sd_prompt_output])          
        
       
   
    generate_final_item_card.click(card.render_text_on_card, inputs = [selected_generated_image,
                                                                        item_name_output, 
                                                                        item_type_output, 
                                                                        item_rarity_output, 
                                                                        item_value_output,
                                                                        item_properties_output, 
                                                                        item_damage_output,
                                                                        item_weight_output,
                                                                        item_description_output,
                                                                        item_quote_output
                                                                        ], 
                                                                        outputs = generate_gallery )
    


if __name__ == '__main__':
    app.launch(server_name = "localhost", server_port = 8000, share = False, allowed_paths = ["/media/drakosfire/Shared/","/media/drakosfire/Shared/MerchantBot/card_templates"])
        







    


   


