
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
initial_name = "Sekhmet the Sphinx Cat"

with gr.Blocks() as demo:
    
    # Functions and State Variables
    # Build functions W/in the Gradio format, because it only allows modification within it's context
    # Define inputs to match what is called on click, and output of the function as a list that matches the list of outputs
    textbox_default_dict = {'Name':'', 
                            'Pet Species': '',
                            'Breed':'',
                            'Fur':'',
                            'Intelligence Level':'',
                            'Affection Level':'',
                            'Energy Level':'',
                            'Noise Level':'',
                            'Play Level':'',
                            'image Prompt':''
                            }
    # Text states
    pet_name_state = gr.State()
    pet_species_state = gr.State()
    pet_breed_state = gr.State()
    pet_fur_state = gr.State()
    pet_intelligence_level_state = gr.State()
    pet_affection_level_state = gr.State()
    pet_energy_level_state = gr.State()
    pet_noise_level_state = gr.State()
    pet_play_level_state = gr.State()
    image_prompt_var = gr.State('')

    # Image States
    selected_border_image = gr.State('./card_templates/Moonstone Border.png')
    num_image_to_generate = gr.State(4)
    generated_image_list = gr.State([])
    selected_generated_image = gr.State()
    selected_seed_image = gr.State()
    built_template = gr.State()  
    

    def set_textbox_defaults(textbox_default_dict, key):
        pet_name = textbox_default_dict[key]
        return pet_name

    # Function called when user generates item info, then assign values of dictionary to variables, output once to State, twice to textbox
    def generate_text_update_textboxes(user_input):
        u.reclaim_mem()

        llm_output=useri.call_llm(user_input)
        pet_key = list(llm_output.keys())
        #This is for creating a list of key values in the returned hashmap to search for specific keys.
        # pet_key_values = list(llm_output[pet_key[0]].keys())
        pet_name = llm_output[pet_key[0]]['Name']
        pet_species = llm_output[pet_key[0]]['Pet Species']
        pet_breed = llm_output[pet_key[0]]['Breed']            
        pet_fur = llm_output[pet_key[0]]['Fur']
        pet_intelligence_level = llm_output[pet_key[0]]['Intelligence Level']
        pet_affection_level = llm_output[pet_key[0]]['Affection Level']
        pet_energy_level = llm_output[pet_key[0]]['Energy Level']
        pet_noise_level = llm_output[pet_key[0]]['Noise Level']
        pet_play_level = llm_output[pet_key[0]]['Play Level']
        image_prompt = llm_output[pet_key[0]]['Image Prompt']

        return [pet_name, pet_name,
                pet_species, pet_species,
                pet_breed, pet_breed,
                pet_fur, pet_fur,
                pet_intelligence_level, pet_intelligence_level,
                pet_affection_level, pet_affection_level,
                pet_energy_level, pet_energy_level,
                pet_noise_level, pet_noise_level,
                pet_play_level, pet_play_level,
                image_prompt, image_prompt]
    
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
        img2img.image_list.clear()
    
    # Called when pressing button to generate image, updates gallery by returning the list of image URLs
    def generate_image_update_gallery(num_img, image_prompt,pet_name, built_template):
        delete_temp_images()
        print(type(built_template))
        image_list = []
        img_gen, prompt = img2img.load_img_gen(image_prompt, pet_name)
        for x in range(num_img):
            preview = img2img.preview_and_generate_image(x,img_gen, prompt, built_template, pet_name)
            image_list.append(preview)
            yield image_list
        del preview
        u.reclaim_mem()
        return image_list
    
    def build_template(selected_border, selected_seed_image):
        image_list = tb.build_card_template(selected_border, selected_seed_image)
        return image_list, image_list
   

    # Beginning of UI Page
    gr.HTML(""" <div id="inner"> <header>
            <h1>Item Card Generator</h1>
            <p>
            With this AI driven tool you will build a collectible style card of a fantasy flavored item with details.
            </p>
            </div>""")
    
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
                                            value = useri.index_image_paths("Drakosfire/CardGenerator", "seed_images/card_templates"),
                                            show_label = True,
                                            columns = [3], rows = [3],
                                            object_fit = "contain",
                                            height = "auto",
                                            elem_id = "Template Gallery")
        with gr.Column():
            gr.HTML(""" <div id="inner"> <header>
                        <h3>2. Click a image from the Seed Image Gallery</h3><br>
                        </div>""")
            
            border_gallery.select(assign_img_path, outputs = selected_border_image)
            seed_image_gallery = gr.Gallery(label= " Image Seed Gallery",
                                            scale = 2,
                                            value = useri.index_image_paths("Drakosfire/CardGenerator", "seed_images/item_seeds"),
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
                                        columns = [4], rows = [4],
                                        object_fit = "contain",
                                        height = "auto",
                                        elem_id = "Template Gallery",
                                        interactive=True) 
    
    seed_image_gallery.select(assign_img_path, outputs = selected_seed_image)
    built_template_gallery.upload(u.receive_upload, inputs=built_template_gallery, outputs= selected_seed_image)
    build_card_template_button = gr.Button(value = "Generate Card Template")
    build_card_template_button.click(build_template, inputs = [selected_border_image, selected_seed_image], outputs = [built_template_gallery, built_template]) 
        
    gr.HTML(""" <div id="inner"> <header>
                    <h2><b>Second:</b> Generate Item Text </h2>
                   </div>""")  
    gr.HTML(""" <div id="inner"> <header>
                        <h3>1. Use a name, a breed, some coloring and the animal type, Ex: 'Hermione the Stormy Grey English Shorthair Cat' then click 'Generate Text' </h3>
                        </div>""")
    with gr.Row():
        user_input =  gr.Textbox(label = 'Item', lines =1, placeholder= "Sekhmet the Sphinx Cat", elem_id= "Item", scale =4)
        item_text_generate = gr.Button(value = "Generate item text", scale=1)

    gr.HTML(""" <div id="inner"> <header>
                <h3> 2. Review and Edit the text</h3>
                </div>""") 
    with gr.Row():

    # Build text boxes for the broken up item dictionary values         
        with gr.Column(scale = 1):
            pet_name_output = gr.Textbox(value = set_textbox_defaults(
                textbox_default_dict, 'Name'),label = 'Name', lines = 1, interactive=True, elem_id='Pet Name')
            
            pet_species_output = gr.Textbox(value = set_textbox_defaults(
                textbox_default_dict, 'Pet Species'),label = 'Type', lines = 1, interactive=True, elem_id='Pet Species')
            
            pet_breed_output = gr.Textbox(value = set_textbox_defaults(
                textbox_default_dict, 'Breed'),label = 'Breed : [Common, Uncommon, Rare, Very Rare, Legendary]',
                lines = 1, interactive=True, elem_id='Pet Breed')
            
            pet_fur_output = gr.Textbox(value = set_textbox_defaults(
                textbox_default_dict, 'Fur'),label = 'Fur Quality', lines = 1, interactive=True, elem_id='Pet Fur')
                        
                # Pass the user input and border template to the generator
        with gr.Column(scale = 1):    
            pet_affection_level_output = gr.Textbox(value = set_textbox_defaults(
                textbox_default_dict, 'Affection Level'),label = 'Affection Level', lines = 1, interactive=True, elem_id='Affection Level')
            
            pet_energy_level_output = gr.Textbox(value = set_textbox_defaults(
                textbox_default_dict, 'Energy Level'),label = 'Energy Level', lines = 1, interactive=True, elem_id='Energy Level')
            
            pet_noise_level_output = gr.Textbox(value = set_textbox_defaults(
                textbox_default_dict, 'Noise Level'),label = 'Noise Level', lines = 1, interactive=True, elem_id='Noise Level')
            
            pet_play_level_output = gr.Textbox(value = set_textbox_defaults(
                textbox_default_dict, 'Play Level'),label = 'Play Level', lines = 1, interactive=True, elem_id='Play Level')
            
            pet_intelligence_level_output = gr.Textbox(value = set_textbox_defaults(
                textbox_default_dict, 'Intelligence Level'),label = 'Intelligence Level',
                lines = 1, interactive=True, elem_id='Intelligence Level')
    
    gr.HTML(""" <div id="inner"> <header>
                <h3> 3. This text will be used to generate the card's image.</h3>
                </div>""") 
    image_prompt_output = gr.Textbox(label = 'Putting words or phrases in parenthesis adds weight. Example: (Flaming Magical :1.0) Sword.', value = set_textbox_defaults(textbox_default_dict, 'image Prompt'), lines = 1, interactive=True, elem_id='image Prompt')
         
    gr.HTML(""" <div id="inner"> <header>
                <h2> <b>Third:</b> Click 'Generate Cards' to generate 4 cards to choose from. </h2>
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
                                    columns =[2], rows = [2],
                                    object_fit= "fill",
                                    height = "768",
                                    elem_id = "Generated Cards Gallery"
                                    )
        generate_final_item_card = gr.Button(value = "Add Text", elem_id = "Generate user card")
    
    card_gen_button.click(fn = generate_image_update_gallery, inputs =[num_image_to_generate,image_prompt_output,pet_name_output,built_template], outputs= generate_gallery)
    generate_gallery.select(assign_img_path, outputs = selected_generated_image)

        # Button logice calls function when button object is pressed, passing inputs and passing output to components
    llm_output = item_text_generate.click(generate_text_update_textboxes, 
                                                inputs = [user_input], 
                                                outputs= [pet_name_state, 
                                                        pet_name_output,
                                                        pet_species_state,
                                                        pet_species_output, 
                                                        pet_breed_state,
                                                        pet_breed_output,
                                                        pet_fur_state,
                                                        pet_fur_output,
                                                        pet_intelligence_level_state,
                                                        pet_intelligence_level_output,
                                                        pet_affection_level_state,
                                                        pet_affection_level_output,
                                                        pet_energy_level_state,
                                                        pet_energy_level_output,
                                                        pet_noise_level_state,
                                                        pet_noise_level_output,
                                                        pet_play_level_state,
                                                        pet_play_level_output,                                                     
                                                        image_prompt_var,
                                                        image_prompt_output])          
        
    generate_final_item_card.click(card.render_text_on_card, inputs = [selected_generated_image,
                                                                        pet_name_output, 
                                                                        pet_species_output, 
                                                                        pet_breed_output, 
                                                                        pet_fur_output,
                                                                        pet_intelligence_level_output, 
                                                                        pet_affection_level_output,
                                                                        pet_energy_level_output,
                                                                        pet_noise_level_output,
                                                                        pet_play_level_output
                                                                        ],
                                                                        outputs = generate_gallery )
 
  
if __name__ == '__main__':
    demo.launch(server_name = "0.0.0.0", server_port = 8000, share = False, allowed_paths = ["/media/drakosfire/Shared/","/media/drakosfire/Shared/MerchantBot/card_templates"])
        





   


