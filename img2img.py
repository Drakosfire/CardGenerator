import time
import utilities as u
import card_generator as card
from PIL import Image
import fal_client
from pathlib import Path
import tempfile
import os
import base64
import io
import logging
import requests
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

start_time = time.time()
temp_image_path = "./image_temp/"



def preview_and_generate_image(num_images, sd_prompt, user_input_template):
    print(f"num_images: {num_images}")
    print(f"sd_prompt: {sd_prompt}")
    print(f"user_input_template: {user_input_template}")
    num_images = int(4)
    sd_prompt = f"magnum opus, blank card, no text, blank textboxes, detailed high quality animal properties borders, {sd_prompt}"
    try:
        # Save the image to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            user_input_template[0].save(temp_file.name, format="PNG")
            temp_path = temp_file.name

        logger.info(f"Image saved to temporary file: {temp_path}")

        # Upload the file using fal_client
        url = fal_client.upload_file(temp_path)
        logger.info(f"Image uploaded. URL: {url}")

        # Remove the temporary file
        os.unlink(temp_path)

        request_handle = fal_client.submit(
            "fal-ai/flux-lora/image-to-image",
            arguments={
                "num_inference_steps": 35,
                "prompt": sd_prompt,
                "num_images": num_images,
                "image_url": url,
                "strength": 0.85
            }
        )
        
        logger.info(f"Type of request_handle: {type(request_handle)}")
        logger.info(f"Content of request_handle: {request_handle}")
        
        # Get the result from the SyncRequestHandle
        result = request_handle.get()
        
        logger.info(f"Type of result: {type(result)}")
        logger.info(f"Content of result: {json.dumps(result, indent=2)}")
        
        # Extract the image URLs from the result
        image_urls = [img['url'] for img in result.get('images', [])]
        
        logger.info(f"Extracted image URLs: {image_urls}")
        
        if not image_urls:
            logger.warning("No images were generated.")
            return []
        
        # Download and process the images
        images = []
        for i, url in enumerate(image_urls):
            try:
                response = requests.get(url)
                response.raise_for_status()  # Raises an HTTPError for bad responses
                img = Image.open(io.BytesIO(response.content))
                images.append((img, f"Generated Image {i+1}"))  # Add a tuple with image and caption
                logger.info(f"Successfully downloaded and processed image {i+1}")
            except Exception as e:
                logger.error(f"Error processing image {i+1} from URL {url}: {str(e)}")
        
        if not images:
            logger.warning("No images could be downloaded and processed.")
            return []
        
        logger.info(f"Returning {len(images)} processed images")
        return images
    
    except Exception as e:
        logger.error(f"Error during API call or processing: {str(e)}")
        logger.exception("Full traceback:")
        return []








          