#This independent from streamlit runs full speed ~ 5it/s /w StableDiffusionXLPipeline
from diffusers import StableDiffusionXLPipeline, StableDiffusionPipeline
import torch
import time
import inventory as inv
import utilities as u

start_time = time.time()
card_pre_prompt = " blank magic card,high resolution, detailed high quality intricate border, decorated textbox, high quality magnum opus cgi drawing of"
torch.backends.cuda.matmul.allow_tf32 = True
image_list = []
item = inv.inventory['Shortsword']
def generate_image(num_img, prompt, item) :
    prompt = card_pre_prompt + prompt
    print(prompt)
    model_path = ("../models/stable-diffusion/SDXLFaetastic_v20.safetensors")
    lora_path = ("../models/stable-diffusion/Loras/blank-card-template.safetensors")
    pipe = StableDiffusionXLPipeline.from_single_file(model_path,
                                                       custom_pipeline="low_stable_diffusion",                                                       
                                                         torch_dtype=torch.float16, 
                                                         variant="fp16" ).to("cuda")
    pipe.load_lora_weights(lora_path)
    pipe.enable_vae_slicing()


    for x in range(num_img):
        img_start = time.time()
        image = pipe(prompt=prompt,num_inference_steps=50, height = 1024, width = 768).images[0]
        image = image.save(str(x) + f"{item}.png")
        img_time = time.time() - img_start
        img_its = 50/img_time
        print(f"image gen time = {img_time} and {img_its} it/s")
        print(f"Memory after image {x} = {torch.cuda.memory_allocated()}")
        image_path = str(os.path.abspath(image))
        # image_list.append(image_path)
        del image
        del pipe
        u.reclaim_mem()
        
        print(f"Memory after del {torch.cuda.memory_allocated()}")
        print(image_list)
    total_time = time.time() - start_time
    
    print(f"Total Time to generate{x} images = {total_time} ")   
    return image_path




          