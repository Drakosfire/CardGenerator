from llama_cpp import Llama
import ast
import gc
import torch

model_path = "./models/starling-lm-7b-alpha.Q8_0.gguf"
# Add variable for User Style prompt ie GPT4 User
# Add variable for end of input and response name ie <|end_of_turn|>GPT4 Assistant:
# Make prompt a variable

def load_llm(user_input):
  llm = Llama(
  model_path=model_path,
  n_ctx=8192,  # The max sequence length to use - note that longer sequence lengths require much more resources
  n_threads=8,            # The number of CPU threads to use, tailor to your system and the resulting performance
  n_gpu_layers=32 # The number of layers to offload to GPU, if you have GPU acceleration available
  )
  return llm(
  f"GPT4 User: {prompt_instructions}  the pet is {user_input}: <|end_of_turn|>GPT4 Assistant:", # Prompt
  max_tokens=768,  # Generate up to 512 tokens

  stop=["</s>"],   # Example stop token - not necessarily correct for this specific model! Please check before using.
  echo=False        # Whether to echo the prompt
  )

def call_llm_and_cleanup(user_input):
    # Call the LLM and store its output
    llm_output = load_llm(user_input)
    print(llm_output['choices'][0]['text'])
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()  # Clear VRAM allocated by PyTorch
    
    # llm_output is still available for use here
    
    return llm_output

def convert_to_dict(string):
  # Evaluate if string is dictionary literal
    try: 
        result = ast.literal_eval(string)
        if isinstance(result, dict):
            print("pet dictionary is valid")
            return result
        # If not, modify by attempting to add brackets to where they tend to fail to generate.
        else: 
            modified_string = '{' + string
            if isinstance(modified_string, dict):  
                return modified_string
            modified_string = string + '}'
            if isinstance(modified_string, dict):  
                return modified_string
            modified_string = '{' + string + '}'
            if isinstance(modified_string, dict):  
                return modified_string
    except (ValueError, SyntaxError) :
        print("Dictionary not valid")
        return None
  

# Instructions past 4 are not time tested and may need to be removed.
### Meta prompted : 
prompt_instructions = """ **Purpose**: Generate a structured inventory entry for a model of cybernetic pet made by the imaginary Cavall technology company.

**Instructions**:
1. Replace `{pet}` with the name of the user pet, DO NOT CHANGE THE USER pet NAME enclosed in single quotes (e.g., `'Magic Wand'`).
2. Ensure your request is formatted as a hashmap. 
3. The cybernetic pets are friendly and cute, they are products and toys. 
4. The description should be brief and puncy, or concise and in the voice of a judge at a high end cat or dog or pet exhibition such as the American Kennel Clube or Cat Fancier and make specific callout of how mild, and well camoflaughed the artificiality of the cybernetic pet is.
5. The quote and SD Prompt MUST be inside double quotations ie " ".
8. Value should be assigned as an integer of copper pieces (cp), silver pieces (sp), electrum pieces (ep), gold pieces (gp), and platinum pieces (pp). 

 
**Format Example**:
- **Dictionary Structure**:
    
    {"{Pet}": {
    'Name': "{Pet Name}",
    'Pet Species': '{pet species}',
    'Breed': '{pet breed},
    'Fur': '{pet fur qualities}',
    'Intelligence Level': ["{property1}", "{property2}", ...],
    'Affection Level': '{property1} , '{property2}',
    'Energy Level': '{energy level}',
    'Noise Level': "{pet description}",
    'Play Level': "{play level}",
    'SD Prompt': "{special description for the pet}"
    } }
    
- **Input Placeholder**:
    - "{pet}": Replace with the pet name, ensuring it's wrapped in single quotes.

**Output Examples**:
1. Mignon the Toy Sized Chihuahua 

    {“Mignon”: {
	'Name': "Mignon”
    'Pet Species': Dog,
    “Breed” : ”Chihuahua (Toy)”,
    “Fur”: “Cream, smooth shorthair”,
    “Intelligence Level”: “Medium-high, trainable but stubborn”,
    “Affection Level”: “High but selective, prefers favorite humans”,
    “Energy Level”: “High”,
    “Noise Level” : “Very high, yappy”,
    “Play Level” : “Low“, Fetch, chase“
    }


2. Marmalade the Austrailian Shepherd Herding Dog

	{“Marmalade”:{
    “Breed” : ”Australian Shepherd (Herding)”,
    'Pet Species': Dog,
    “Fur”: “Blue merle with white markings and tan points, medium double coat”,
    “Intelligence Level”: “Very high, suitable for jobs”,
    “Affection Level”: “High”,
    “Energy Level”: “Very high”,
    “Noise Level” : “Medium, piercing”,
    “Play Level” : “Very high, Agility, herding, obedience, frisbee, puzzles”
    }

3. Holden Clawfield the Pembroke Welsh Corgi Herding Dog

{“Holden Clawfield”:{
    “Breed” : ”Pembroke Welsh Corgi (Herding)”,
    'Pet Species': Dog,
    “Fur”: “Fawn with white markings, short double coat”,
    “Intelligence Level”: “High, trainable”,
    “Affection Level”: “Very high, loves humans and other Pets”,
    “Energy Level”: “High”,
    “Noise Level” : “High, piercing”,
    “Play Level” : “High, Toys, herding, obedience”
    }

4. Tyr the Great Pyr the Great Pyreness Working Dog

{“Tyr the Great Pyr”:{
	“Breed” : ”Great Pyrenees (Working)”,
    'Pet Species': Dog,
    “Fur”: “White, medium double coat”,
    “Intelligence Level”: “Medium, trainable to a point”,
    “Affection Level”: “Medium, wary of strangers”,
    “Energy Level”: “Low, mostly lazy but vigilant”,
    “Noise Level and Style” : “Medium, will bark to alert”,
    “Play Level” : “Medium, not motivated by play, Toys, treats”
    }

5. Emperor Maximus the Great Dane Working Dog

{“Emperor Maximus”:{
    “Breed” : ”Great Dane (Working)”,
    'Pet Species': Dog,
    “Fur”: “Black and white with black mask, smooth shorthair”,
    “Intelligence Level”: “Medium, trainable”,
    “Affection Level”: “Very high, needy”,
    “Energy Level”: “Medium, enjoys hiking”,
    “Noise Level and Style” : “Medium, will bark to alert”,
    “Play Level” : “Medium, Chase, tug”
    }

6. Becks the Airedale Terrier Dog

{“Becks”:{
    “Breed” : ”Airedale Terrier (Terrier)”,
    'Pet Species': Dog,
    “Fur”: “Black and tan, medium wiry coat”,
    “Intelligence Level”: “Medium, responds well to training”,
    “Affection Level”: “Medium, reserved”,
    “Energy Level”: “High, alert and active”,
    “Noise Level and Style” : “Medium, vigilant watchdog”,
    “Play Level” : “Medium, Fetch, toys, treats”
    }

7. Blue Carolina the Plott Hound

    {“Blue Carolina”:{
    “Breed” : ”Plott Hound (Hound)”,
    'Pet Species': Dog,
    “Fur”: “Chocolate brindle, smooth shorthair”,
    “Intelligence Level”: “High, driven and trainable”,
    “Affection Level”: “High, very sweet”,
    “Energy Level”: “High, alert and active”,
    “Noise Level and Style” : “Medium, will bark to alert”,
    “Play Level” : “Medium, more active than playful, Toys, frisbee, chase”
    }
"""
