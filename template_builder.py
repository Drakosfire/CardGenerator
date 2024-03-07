from PIL import Image, ImageDraw, ImageFont

# Function to initialize image canvas

# Function to scale the seed image

# Paste seed image onto blank canvas at specific location

# Paste the selected border on top

# Save and return

# Function that takes in an image url and a dictionary and uses the values to print onto a card.

# Seed Image starting x,y
seed_x = 56
seed_y = 128
seed_width = 648
seed_height = 425

def paste_image_and_resize(base_image,sticker_path, x_position, y_position,img_width, img_height):    
        
    # Load the image to paste
    image_to_paste = Image.open(sticker_path)

    # Define the new size (scale) for the image you're pasting
    
    new_size = (img_width, img_height)

    # Resize the image to the new size
    image_to_paste_resized = image_to_paste.resize(new_size)

    # Specify the top-left corner where the resized image will be pasted
    paste_position = (x_position, y_position)  # Replace x and y with the coordinates

    # Paste the resized image onto the base image
    base_image.paste(image_to_paste_resized, paste_position, image_to_paste_resized)

def build_card_template(selected_border, selected_seed_image):
    image_list = []

    # Image size parameters
    width = 768
    height = 1024

    # Set canvas as transparent

    background_color = (0,0,0,0)

    #initialize canvas
    canvas = Image.new('RGB', (width, height), background_color)

    canvas = paste_image_and_resize(canvas, selected_seed_image,seed_x,seed_y, seed_width, seed_height)
    canvas = paste_image_and_resize(canvas, selected_border,0,0,width,height)

    image_list.append(canvas)

    return image_list


 