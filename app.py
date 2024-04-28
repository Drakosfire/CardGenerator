import img2img
import card_generator as card
import utilities as u
import os
import user_input as useri
import gradio as gr
import template_builder as tb

initial_name = "A Crowbar"

with gr.Blocks() as demo:
    
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
    def generate_text_update_textboxes(user_input):
        
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
    def assign_img_path(evt: gr.SelectData):          
        img_dict = evt.value
        print(img_dict)
        selected_image_path = img_dict['image']['url']
        print(selected_image_path)
        return selected_image_path   
    
     # Make a list of files in image_temp and delete them
    def delete_temp_images():
        image_list = u.directory_contents('./image_temp')
        u.delete_files(image_list)
        u.image_list.clear()
    
    # Called when pressing button to generate image, updates gallery by returning the list of image URLs
    def generate_image_update_gallery(num_img, sd_prompt,item_name, built_template):
        delete_temp_images()
        print(f"sd_prompt is a {type(sd_prompt)}")
        image_list = []
        
        
        for x in range(num_img):
            preview = img2img.preview_and_generate_image(x,sd_prompt, built_template, item_name)
            image_list.append(preview)
            yield image_list
            
        del preview
       
        #generated_image_list = img2img.generate_image(num_img,sd_prompt,item_name,selected_border)
        return image_list
    
    def build_template(selected_border, selected_seed_image):
        image_list = tb.build_card_template(selected_border, selected_seed_image)
        return image_list, image_list
   

    # Beginning of UI Page
    # Beginning of UI Page
    gr.HTML(""" <div id="inner"> <header>
            <h1>Item Card Generator</h1>
            <p>
            With this AI driven tool you will build a collectible style card of a fantasy flavored item with details.
            </p>
            </div>""")
    markdown_instructions = """## How It Works

1. Your intitial text along with the prompt is sent to Llama 3 70b to generate a python dictionary.
2. This new text will populate in interactive text fields. If it isn't perfect you can edit the text to fit your item.
3. The final text field is the Stable Diffusion prompt, these generate like one sentence stories describing the scene of your item. This field can also be edited.
## The first image generation take about 2 minutes for model to 'cold boot' after that it's ~10s per image.
4. **Image and Text Generation**: Now generate 4 card template without text and pick your favorite.
5. Finally, add text to your favorite template.
3. **Result**: The final product is a beautifully crafted D&D item card, ready for use in your gaming sessions."""

    gr.Markdown(markdown_instructions)

    gr.HTML(""" <div id="inner"> <header>
            <h2><b>First:</b> Build a Card Template</h2>
                </div>""")
    with gr.Row():
        with gr.Column():

    # Template Gallery instructions
            gr.HTML(""" <div id="inner"> <header>
                        <h3>1. Click a border from the 'Card Template Gallery'</h3> 
                        </div>""")
        
    border_gallery = gr.Gallery(label = "Card Template Gallery", 
                                    scale = 2,
                                    value = u.index_image_paths("Drakosfire/CardGenerator", "seed_images/card_templates"),
                                    show_label = True,
                                    columns = [3], rows = [3],
                                    object_fit = "contain",
                                    height = "auto",
                                    elem_id = "Template Gallery")
    
    gr.HTML(""" <div id="inner"> <header>
                <h3>2. Click a image from the Seed Image Gallery</h3><br>
                </div>""")
    
    border_gallery.select(assign_img_path, outputs = selected_border_image)
    seed_image_gallery = gr.Gallery(label= " Image Seed Gallery",
                                    scale = 2,
                                    value = u.index_image_paths("Drakosfire/CardGenerator", "seed_images/item_seeds"),
                                    show_label = True,
                                    columns = [3], rows = [3],
                                    object_fit = "contain",
                                    height = "auto",
                                    elem_id = "Template Gallery",
                                    interactive=True)                 

    gr.HTML(""" <div id="inner"> <header><h4> -Or- Upload your own seed image, by dropping it into the 'Generated Template Gallery' </h4><br>
                <h3>3. Click 'Generate Card Template'</h3><br>
            </div>""")
    
    built_template_gallery = gr.Gallery(label= "Generated Template Gallery",
                                        scale = 1,
                                        value = None,
                                        show_label = True,
                                        columns = [1], rows = [1],
                                        object_fit = "contain",
                                        height = "auto",
                                        elem_id = "Template Gallery",
                                        interactive=True,
                                        type="filepath") 
    
    seed_image_gallery.select(assign_img_path, outputs = selected_seed_image)
    built_template_gallery.upload(u.receive_upload, inputs=built_template_gallery, outputs= selected_seed_image)
    build_card_template_button = gr.Button(value = "Generate Card Template")
    build_card_template_button.click(build_template, inputs = [selected_border_image, selected_seed_image], outputs = [built_template_gallery, built_template]) 
        
    gr.HTML(""" <div id="inner"> <header>
                    <h2><b>Second:</b> Generate Item Text </h2>
                   </div>""")  
    gr.HTML(""" <div id="inner"> <header>
                        <h3>1. Use a few words to describe the item then click 'Generate Text' </h3>
                        </div>""")
    with gr.Row():
        user_input =  gr.Textbox(label = 'Item', lines =1, placeholder= "Flaming Magical Sword", elem_id= "Item", scale =4)
        item_text_generate = gr.Button(value = "Generate item text", scale=1)

    gr.HTML(""" <div id="inner"> <header>
                <h3> 2. Review and Edit the text</h3>
                </div>""") 
    with gr.Row():

    # Build text boxes for the broken up item dictionary values         

    # Build text boxes for the broken up item dictionary values         
        with gr.Column(scale = 1):
            item_name_output = gr.Textbox(value = set_textbox_defaults(textbox_default_dict, 'Name'),label = 'Name', lines = 1, interactive=True, elem_id='Item Name')
            item_type_output = gr.Textbox(value = set_textbox_defaults(textbox_default_dict, 'Type'),label = 'Type', lines = 1, interactive=True, elem_id='Item Type')
            item_rarity_output = gr.Textbox(value = set_textbox_defaults(textbox_default_dict, 'Rarity'),label = 'Rarity : [Common, Uncommon, Rare, Very Rare, Legendary]', lines = 1, interactive=True, elem_id='Item Rarity')
            item_value_output = gr.Textbox(value = set_textbox_defaults(textbox_default_dict, 'Value'),label = 'Value', lines = 1, interactive=True, elem_id='Item Value')
                        
                # Pass the user input and border template to the generator
        with gr.Column(scale = 1):    
            item_damage_output = gr.Textbox(value = set_textbox_defaults(textbox_default_dict, 'Damage'),label = 'Damage', lines = 1, interactive=True, elem_id='Item Damage')
            item_weight_output = gr.Textbox(value = set_textbox_defaults(textbox_default_dict, 'Weight'),label = 'Weight', lines = 1, interactive=True, elem_id='Item Weight')
            item_description_output = gr.Textbox(value = set_textbox_defaults(textbox_default_dict, 'Description'),label = 'Description', lines = 1, interactive=True, elem_id='Item Description')
            item_quote_output = gr.Textbox(value = set_textbox_defaults(textbox_default_dict, 'Quote'),label = 'Quote', lines = 1, interactive=True, elem_id='Item quote')
    item_properties_output = gr.Textbox(value = set_textbox_defaults(textbox_default_dict, 'Properties'),label = 'Properties : [List of comma seperated values]', lines = 1, interactive=True, elem_id='Item Properties')
    
    
    gr.HTML(""" <div id="inner"> <header>
                <h3> 3. This text will be used to generate the card's image.</h3>
                </div>""") 
    item_sd_prompt_output = gr.Textbox(label = 'Putting words or phrases in parenthesis adds weight. Example: (Flaming Magical :1.0) Sword.', value = set_textbox_defaults(textbox_default_dict, 'SD Prompt'), lines = 1, interactive=True, elem_id='SD Prompt')
         
    gr.HTML(""" <div id="inner"> <header>
                <h2> <b>Third:</b> Click 'Generate Cards' to generate 4 cards to choose from. \n First image from a cold boot takes about 2 minutes. \n After that it's 10 seconds per image. </h2>
                </div>""")          
    card_gen_button = gr.Button(value = "Generate Cards", elem_id="Generate Card Button")
           
    # No longer Row Context, in context of entire Block
    gr.HTML(""" <div id="inner"> <header>
                <h2> <b>Fourth:</b> Click your favorite card then add text, or click 'Generate Four Card Options' again.<br>
                 </h2>
                </div>""")       

    with gr.Row():
        generate_gallery = gr.Gallery(label = "Generated Cards",
                                    value = [],
                                    show_label= True,
                                    scale= 5,
                                    columns =[1], rows = [4],
                                    object_fit= "fill",
                                    height = "768",
                                    elem_id = "Generated Cards Gallery",
                                    allow_preview=False
                                    )
        generate_final_item_card = gr.Button(value = "Add Text", elem_id = "Generate user card")
    
    
    card_gen_button.click(fn = generate_image_update_gallery,
                           inputs =[num_image_to_generate,item_sd_prompt_output,item_name_output,
                                    built_template_gallery], outputs= generate_gallery,
                                    show_progress=True)
    generate_gallery.select(assign_img_path, outputs = selected_generated_image)

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
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Gets the directory where the script is located
    print(f"Base Directory :",base_dir)
    list_of_static_dir = [os.path.join(base_dir, "card_parts"), 
                        os.path.join(base_dir, "fonts"), 
                        os.path.join(base_dir, "image_temp")]
    gr.set_static_paths(paths=list_of_static_dir)
    
    
if __name__ == "__main__":
    demo.launch(allowed_paths=list_of_static_dir) 







    


   


