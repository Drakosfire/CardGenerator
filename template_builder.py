from PIL import Image
import utilities as u

# Function to initialize image canvas

# Function to scale the seed image

# Paste seed image onto blank canvas at specific location

# Paste the selected border on top

# Save and return

# Function that takes in an image url and a dictionary and uses the values to print onto a card.

# Seed Image starting x,y
seed_x = 56
seed_y = 128
seed_width = 657
seed_height = 422

def paste_image_and_resize(base_image,sticker, x_position, y_position,img_width, img_height):    
            
    # Load the image to paste
    # image_to_paste = Image.open(sticker_path)

    # Define the new size (scale) for the image you're pasting
    
    new_size = (img_width, img_height)

    # Resize the image to the new size
    sticker = sticker.resize(new_size)

    # Specify the top-left corner where the resized image will be pasted
    paste_position = (x_position, y_position)  # Replace x and y with the coordinates

    # Paste the resized image onto the base image
    base_image.paste(sticker, paste_position)
    
    return base_image

def build_card_template(selected_border, selected_seed_image):
    selected_border = u.open_image_from_url(selected_border)
    print(f"Selected Border is : {selected_border}")
    if type(selected_seed_image) == str:      
        print(f"String : {selected_seed_image}")      
        selected_seed_image = u.open_image_from_url(selected_seed_image)
    
    # Convert palette-based images to RGBA
    if selected_border.mode == 'P':
        selected_border = selected_border.convert('RGBA')
        print("Converted palette-based image to RGBA.")

    # Resize the border to match the canvas size
    width = 768
    height = 1024
    selected_border = selected_border.resize((width, height))

    # Check if the image has an alpha channel
    if selected_border.mode == 'RGBA':
        mask = selected_border.split()[3]
    else:
        mask = None
        print("Warning: Selected border does not have an alpha channel.")

    image_list = []

    # Set canvas as transparent
    background_color = (0,0,0,0)

    # Initialize canvas
    canvas = Image.new('RGB', (width, height), background_color)
    
    canvas = paste_image_and_resize(canvas, selected_seed_image, seed_x, seed_y, seed_width, seed_height)
    
    # Use the mask only if it exists
    if mask:
        canvas.paste(selected_border, (0, 0), mask=mask)
    else:
        canvas.paste(selected_border, (0, 0))

    print(f"Canvas is : {canvas}")
    print(f"Canvas is : {type(canvas)}")

    image_list.append(canvas)

    return image_list

 