import time
import utilities as u
import card_generator as card
from PIL import Image
import replicate
from pathlib import Path


start_time = time.time()
temp_image_path = "./image_temp/"



def preview_and_generate_image(num_images,sd_prompt, user_input_template, item):    
    # Replicate is expecting a path
    card_template = Path(user_input_template[0][0])
    print(card_template)
    img_start = time.time()   
    output=replicate.run(
            "drakosfire/card-generator-v1:4e46bb44e6444d104b58e34a6d2ab66833aa84ba0dfe84ae57ef63d8e15da467",
            input={
            "item":item,
            "sd_prompt":sd_prompt,
            "num_images":num_images,
            "input_template":card_template

        }
    )
    
    
    img_time = time.time() - img_start
    img_its = 35/img_time
    print(f"image gen time = {img_time} and {img_its} it/s")
    
    total_time = time.time() - start_time
    print(total_time)

    return output








          