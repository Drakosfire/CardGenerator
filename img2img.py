from diffusers import (StableDiffusionXLImg2ImgPipeline, AutoencoderKL)                   
from diffusers.utils import load_image
import torch
import time
import utilities as u
import card_generator as card
from PIL import Image

pipe = None
start_time = time.time()
torch.backends.cuda.matmul.allow_tf32 = True
model_path = ("/home/user/app/models/stable-diffusion/card-generator-v1.safetensors")
lora_path = "/home/user/app/models/stable-diffusion/Loras/blank-card-template-5.safetensors"
detail_lora_path = "/home/user/app/models/stable-diffusion/Loras/add-detail-xl.safetensors"
mimic_lora_path = "/home/user/app/models/stable-diffusion/Loras/EnvyMimicXL01.safetensors"
temp_image_path = "/home/user/app/image_temp/"
card_pre_prompt = " blank magic card,high resolution, detailed intricate high quality border, textbox, high quality detailed magnum opus drawing of a "
negative_prompts = "text, words, numbers, letters"
image_list = []


def load_img_gen(prompt, item, mimic = None):
    prompt = card_pre_prompt + item + ' ' + prompt
    print(prompt)
    # image_path = f"{user_input_template}"
    # init_image = load_image(image_path).convert("RGB")
    
    pipe = StableDiffusionXLImg2ImgPipeline.from_single_file(model_path,
                                                       custom_pipeline="low_stable_diffusion",                                                       
                                                         torch_dtype=torch.float16, 
                                                         variant="fp16").to("cuda")  
    # Load LoRAs for controlling image
    #pipe.load_lora_weights(lora_path, weight_name = "blank-card-template-5.safetensors",adapter_name = 'blank-card-template')    
    pipe.load_lora_weights(detail_lora_path, weight_name = "add-detail-xl.safetensors", adapter_name = "add-detail-xl")
    
    # If mimic keyword has been detected, load the mimic LoRA and set adapter values
    if mimic:
        pipe.load_lora_weights(mimic_lora_path, weight_name = "EnvyMimicXL01.safetensors", adapter_name = "EnvyMimicXL")
        pipe.set_adapters(['blank-card-template', "add-detail-xl", "EnvyMimicXL"], adapter_weights = [0.9,0.9,1.0])
    else : 
        pipe.set_adapters([ "add-detail-xl"], adapter_weights = [0.9])       
    pipe.enable_vae_slicing()
    return pipe, prompt

def preview_and_generate_image(x,pipe, prompt, user_input_template, item):    
    img_start = time.time()   
    image = pipe(prompt=prompt,
                strength = .9,
                guidance_scale = 5,
                image= user_input_template,
                negative_promt = negative_prompts,
                num_inference_steps=40,
                height = 1024, width = 768).images[0]
    
    image = image.save(temp_image_path+str(x) + f"{item}.png")
    output_image_path = temp_image_path+str(x) + f"{item}.png"
    img_time = time.time() - img_start
    img_its = 50/img_time
    print(f"image gen time = {img_time} and {img_its} it/s")
        
    # Delete the image variable to keep VRAM open to load the LLM
    del image
    print(f"Memory after del {torch.cuda.memory_allocated()}")
    print(image_list)
    total_time = time.time() - start_time
    print(total_time)

    return output_image_path








          