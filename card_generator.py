import render_card_text as rend
from PIL import Image, ImageFilter
import utilities as u
import ast
from urllib.request import urlopen
import urllib.request
from urllib.parse import urlparse
import os


def save_image(image,item_key):
    image.save(f"{item_key['Name']}.png")


# Import Inventory 
#shop_inventory = inv.inventory
#purchased_item_key = shop_inventory['Shortsword']
#border_path = './card_templates/Shining Sunset Border.png'
base_path = "https://media.githubusercontent.com/media/Drakosfire/CardGenerator/main/card_parts/"
value_overlay_path = f"{base_path}Value_box_transparent.png"
test_item = {'Name': 'Pustulent Raspberry', 'Type': 'Fruit', 'Value': '1 cp', 'Properties': ['Unusual Appearance', 'Rare Taste'], 'Weight': '0.2 lb', 'Description': 'This small fruit has a pustulent appearance, with bumps and irregular shapes covering its surface. Its vibrant colors and strange texture make it an oddity among other fruits.', 'Quote': 'A fruit that defies expectations, as sweet and sour as life itself.', 'SD Prompt': 'A small fruit with vibrant colors and irregular shapes, bumps covering its surface.'}
sticker_path_dictionary = {'Default': "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/451a66ad-5116-4649-137b-aed784e5c700/public",
                            'Common': "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/8b579f17-7f92-4a0a-e891-e8990be9e400/public",
                            'Uncommon': "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/65889c14-dc2b-4b6a-9cbf-7d7704fba100/public",
                            'Rare': "https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/dedf72a3-00b8-43cf-e95f-7b13b899d100/public",
                            'Very Rare':"https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/3b452c8b-e945-448a-f461-48b99c266c00/public",
                            'Legendary':"https://imagedelivery.net/SahcvrNe_-ej4lTB6vsAZA/2c60b814-ab4c-46ac-e479-d3a860413700/public"}


# Function that takes in an image url and a dictionary and uses the values to print onto a card.
def paste_image_and_resize(base_image, sticker_path, x_position, y_position, img_width, img_height, purchased_item_key=None):
    # Check for if item has a Rarity string that is in the dictionary of sticker paths
    if purchased_item_key:
        if sticker_path.get(purchased_item_key):
            sticker_path = sticker_path[purchased_item_key]
        else:
            sticker_path = sticker_path['Default']
    
    # Create a request with a User-Agent header
    request = urllib.request.Request(sticker_path, headers={'User-Agent': 'Mozilla/5.0'})
    
    # Load the image to paste
    image_to_paste = Image.open(urlopen(request))

    # Convert image to RGBA if not already
    if image_to_paste.mode != 'RGBA':
        image_to_paste = image_to_paste.convert('RGBA')

    # Define the new size (scale) for the image you're pasting
    new_size = (img_width, img_height)

    # Resize the image to the new size
    image_to_paste_resized = image_to_paste.resize(new_size)

    # Specify the top-left corner where the resized image will be pasted
    paste_position = (x_position, y_position)

    # Paste the resized image onto the base image
    base_image.paste(image_to_paste_resized, paste_position, image_to_paste_resized)

def render_text_on_card(image_path, item_name,
                                    item_type,
                                    item_rarity,
                                    item_value,
                                    item_properties,
                                    item_damage,
                                    item_weight,
                                    item_description,
                                    item_quote) : 
    # Card Properties 
    image_list = []
    item_properties = ast.literal_eval(item_properties)
    item_properties = '\n'.join(item_properties)
    output_image_path = f"./{item_name}.png"
    print(f"Saving image to {output_image_path}")
    font_path = "./fonts/Balgruf.ttf"
    italics_font_path = './fonts/BalgrufItalic.ttf'
    initial_font_size = 50

    # Title Properties
    title_center_position = (395, 55)
    title_area_width = 600 # Maximum width of the text box
    title_area_height = 60  # Maximum height of the text box

    # Type box properties
    type_center_position = (384, 545)
    type_area_width = 600 
    type_area_height = 45 
    type_text = item_type
    if len(item_weight) >= 1: 
        type_text = type_text + ' '+ item_weight

    if len(item_damage) >= 1 : 
        type_text = type_text + ' '+ item_damage

    # Description box properties
    description_position = (105, 630)
    description_area_width = 590
    description_area_height = 215

    # Value box properties (This is good, do not change unless underlying textbox layout is changing)
    value_position = (660,905)
    value_area_width = 125
    value_area_height = 50

    # Quote test properties
    quote_position = (110,885)
    quote_area_width = 470
    quote_area_height = 60                     

    
    image = u.open_image_from_url(image_path)
    image = rend.render_text_with_dynamic_spacing(image, item_name, title_center_position, title_area_width, title_area_height,font_path,initial_font_size)
    image = rend.render_text_with_dynamic_spacing(image,type_text , type_center_position, type_area_width, type_area_height,font_path,initial_font_size)
    image = rend.render_text_with_dynamic_spacing(image, item_description + '\n\n' + item_properties, description_position, description_area_width, description_area_height,font_path,initial_font_size, description = True)
    #Paste value overlay
    paste_image_and_resize(image, value_overlay_path,x_position= 0,y_position=0, img_width= 768, img_height= 1024)
    image = rend.render_text_with_dynamic_spacing(image, item_value, value_position, value_area_width, value_area_height,font_path,initial_font_size)
    image = rend.render_text_with_dynamic_spacing(image, item_quote, quote_position, quote_area_width, quote_area_height,italics_font_path,initial_font_size, quote = True)
    #Paste Sizzek Sticker
    paste_image_and_resize(image, sticker_path_dictionary,x_position= 0,y_position=909, img_width= 115, img_height= 115, purchased_item_key= item_rarity)

    # Add blur, gives it a less artificial look, put into list and return the list since gallery requires lists
    image = image.filter(ImageFilter.GaussianBlur(.5))
    image_list.append(image)
   
    return image_list
    





