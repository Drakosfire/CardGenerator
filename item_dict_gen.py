from llama_cpp import Llama
import ast
import gc
import torch

model_path = "models/starling-lm-7b-alpha.Q8_0.gguf"
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
4. The descriptions should be brief and puncy, or concise and in the voice of a judge at a high end cat or dog or pet exhibition such as the American Kennel Clube or Cat Fancier and make specific callout of how mild, and well camoflaughed the artificiality of the cybernetic pet is.
5. The Image Prompt MUST be inside double quotations ie " ".
8. Value should be assigned as an integer of copper pieces (cp), silver pieces (sp), electrum pieces (ep), gold pieces (gp), and platinum pieces (pp). 

 
**Format Example**:
- **Dictionary Structure**:
    
    {"{Pet}": {
    "Name": '{Pet Name}',
    "Pet Species": '{pet species}',
    "Breed": '{pet breed},
    "Fur" : "The colors and quality of the pet's fur,
    "Intelligence Level" : "How intelligent the pet is and how it demonstrates it",
    "Affection Level" : "How affectionate and how the pet shows it,
    "Energy Level" : "The Energy level",
    "Noise Level" : "The volume, frequency, triggers, and type",
    "Play Level" : " The level of play and types enjoyed",
    "Image Prompt" : "Descriptive imagery for an image generator"
     }
    
- **Input Placeholder**:
    - "{pet}": Replace with the pet name, ensuring it's wrapped in single quotes.
    

**Output Examples**:
1. Mignon the Toy Sized Chihuahua 

    {'Mignon': {
	"Name": "Mignon”
    "Pet Species": Dog,
    "Breed" : ”Chihuahua (Toy)”,
    "Fur" : “Cream, smooth shorthair”,
    "Intelligence Level" : “Medium-high, tr'inable but stubborn”,
    "Affection Level" : “High but selective, prefers favorite humans”,
    "Energy Level" : “High”,
    "Noise Level" : “Very high, yappy”,
    "Play Level" : “Low“, Fetch, chase“
    "Image Prompt" :  "An elegant masterpiece drawing of a ( beautiful subtle nuanced glowing biomimicry bionic robot dog) (glowing eyes)(glowing chest)(thick healthy fur)(Glowing pet collar) Chihuahua, boasting a luscious cream coat and an attitude that's equal parts feisty and affectionate. Note the subtle glow behind her eyes, a hint of advanced biometrics enhancing her already keen senses."
    }


2. Marmalade the Austrailian Shepherd Herding Dog

	{'Marmalade':{
    "Name":"Marmalade",
    "Breed" : ”Australian Shepherd (Herding)”,
    "Pet Species": Dog,
    "Fur" : “Blue merle with white markings and tan points, medium double coat”,
    "Intelligence Level" : “Very high, suitable for jobs”,
    "Affection Level" : “High”,
    "Energy Level" : “Very high”,
    "Noise Level" : “Medium, piercing”,
    "Play Level" : “Very high, Agility, herding, obedience, frisbee, puzzles”,
    "Image Prompt"  : "An elegant masterpiece drawing of a ( beautiful subtle nuanced glowing biomimicry bionic robot dog) (glowing eyes)(glowing chest)(thick healthy fur)(Glowing pet collar) an Australian Shepherd of impeccable breeding, showcasing a stunning blue merle coat and the intelligence to match." 
    }

3. Holden Clawfield the Pembroke Welsh Corgi Herding Dog

{“Holden Clawfield”:{
    "Name" : "Holden Clawfield",
    "Breed" : ”Pembroke Welsh Corgi (Herding)”,
    "Pet Species": Dog,
    "Fur" : “Fawn with white markings, short double coat”,
    "Intelligence Level"  : “High, trainable',
    "Affection Level" : “Very high, loves humans and other Pets”,
    "Energy Level" : “High”,
    "Noise Level" : “High, piercing”,
    "Play Level" : “High, Toys, herding, obedience”,
    "Image Prompt"  : "An elegant masterpiece drawing of a ( beautiful subtle nuanced glowing biomimicry bionic robot dog) (glowing eyes)(glowing chest)(thick healthy fur)(Glowing pet collar) a Pembroke Welsh Corgi of noble bearing, flaunting a rich fawn coat and an endearing personality."
    }

4. Tyr the Great Pyr the Great Pyreness Working Dog

{“Tyr the Great Pyr”:{
    "Name" : "Tyr the Great Pyr",
	"Breed" : ”Great Pyrenees (Working)”,
    "Pet Species": Dog,
    "Fur" : “White, medium double coat”,
    "Intelligence Level"  : “Medium, trainable to a point”,
    "Affection Level" : “Medium, wary of strangers”,
    "Energy Level" : “Low, mostly lazy but vigilant”,
    "Noise Level" : “Medium, will bark to alert”,
    "Play Level" : “Medium, not motivated by play, Toys, treats”,
    "Image Prompt"  : "An elegant masterpiece drawing of a ( beautiful subtle nuanced glowing biomimicry bionic robot dog) (glowing eyes)(glowing chest)(thick healthy fur)(Glowing pet collar)a Great Pyrenees of regal demeanor, White, medium double coat and an air of quiet confidence. Playing with a toy"
    }

5. Emperor Maximus the Great Dane Working Dog

{“Emperor Maximus”:{
    "Name" : "Emperor Maximus",
    "Breed" : ”Great Dane (Working)”,
    "Pet Species": Dog,
    "Fur" : “Black and white with black mask, smooth shorthair”,
    "Intelligence Level" : “Medium, trainable”,
    "Affection Level" : “Very high, needy”,
    "Energy Level" : “Medium, enjoys hiking”,
    "Noise Level" : “Medium, will bark to alert”,
    "Play Level" : “Medium, Chase, tug”,
    "Image Prompt"  : "An elegant masterpiece drawing of a ( beautiful subtle nuanced glowing biomimicry bionic robot dog) (glowing eyes)(glowing chest)(thick healthy fur)(Glowing pet collar) a Great Dane of imposing stature, Black and white with black mask, smooth shorthair and a gentle giant's disposition."
    }

6. Becks the Airedale Terrier Dog

{“Becks”:{
    "Name" : "Becks",
    "Breed" : ”Airedale Terrier (Terrier)”,
    "Pet Species": Dog,
    "Fur" : “Black and tan, medium wiry coat”,
    "Intelligence Level" : “Medium, respond well to training”,
    "Affection Level" : “Medium, reserved”,
    "Energy Level" : “High, alert and active”,
    "Noise Level" : “Medium, vigilant watchdog”,
    "Play Level" : “Medium, Fetch, toys, treats”,
    "Image Prompt"  : "An elegant masterpiece drawing of a ( beautiful subtle nuanced glowing biomimicry bionic robot dog) (glowing eyes)(glowing chest)(thick healthy fur)(Glowing pet collar) an Airedale Terrier of rugged charm, displaying a handsome black and tan coat and a reserved yet."
    }

7. Blue Carolina the Plott Hound

    {“Blue Carolina”:{
    "Name": "Blue Carolina"
    "Breed" : ”Plott Hound (Hound)”,
    "Pet Species": Dog,
    "Fur" : “Chocolate brindle, smooth shorthair”,
    "Intelligence Level" : “High, driven and trainable”,
    "Affection Level" : “High, very sweet”,
    "Energy Level" : “High, alert and active”,
    "Noise Level" : “Medium, will bark to alert”,
    "Play Level" : “Medium, more active than playful, Toys, frisbee, chase”,
    "Image Prompt"  : "An elegant masterpiece drawing of a ( beautiful subtle nuanced glowing biomimicry bionic robot dog) (glowing eyes)(glowing chest)(thick healthy fur)(Glowing pet collar) Blue Carolina, a Plott Hound of athletic build, showcasing a rich chocolate brindle coat and a high-energy personality.
    }

8. Sekhmet the Sphynx Cat
    {“Sekhmet”:{
    "Name" : "Sekhmet",
	"Breed" : “Sphynx”,
    "Pet Species" : "Cat",
    "Fur" : “Hairless, light brown”,
    "Intelligence Level" : “High, trainable',
    "Affection Level" : “High but selective, prefers favorite human”,
    "Energy Level" : “Low, reserved”,
    "Noise Level" : “Low, mostly quiet”,
    "Play Level" : “Low, lazy, Cuddling, lap time, shoulder perching”,
    "Image Prompt"  : "An elegant masterpiece drawing of a ( beautiful subtle nuanced glowing biomimicry bionic robot cat) (glowing eyes)(glowing chest)(thick healthy fur)(Glowing pet collar)Sphynx Cat, Hairless, light brown Cuddling, lap time, shoulder perching."
    }

9. Smith the American Shorthair Cat

	{“Smith”:{
    "Name" : "Smith",
	"Breed" : “American Shorthair”,
    "Pet Species" : "Cat",
    "Fur" : “Black”,
    "Intelligence Level" : “Medium, somewhat trainable”,
    "Affection Level" : “High, loves humans and other Pets”,
    "Energy Level" : “Medium”,
    "Noise Level" : “Low, infrequent meows”,
    "Play Level" : “Medium, Belly rubs, hunting, toys”,
    "Image Prompt"  : "An elegant masterpiece drawing of a ( beautiful subtle nuanced glowing biomimicry bionic robot cat) (glowing eyes)(glowing chest)(thick healthy fur)(Glowing pet collar) American Shorthair Black Fur playing with a toy"
    }	

10. Catherine of Atagon and Her Royal Highness Elizabth I

	{“Catherine of Aragon and Her Royal Highness Elizabeth I”:{
    "Name" : "Catherine of Aragon and Her Royal Highness Elizabeth I",
	"Breed" : “British Shorthair”,
    "Pet Species" : "Cat",
    "Fur" : “Brown and black tortoise shell, black and silver tabby”,
    "Intelligence Level" : “Medium, not int'rested in training”,
    "Affection Level" : “Medium-low, independent”,
    "Energy Level" : “Low, very lazy”,
    "Noise Level" : “Medium, will speak their minds”,
    "Play Level" : “Low, not interested in play, Treats, naps, perching/observing”,
    "Image Prompt"  : "An elegant masterpiece drawing of a ( beautiful subtle nuanced glowing biomimicry bionic robot cat) (glowing eyes)(glowing chest)(thick healthy fur) (Glowing pet collar) British Shorthair, Brown and black tortoise shell, black and silver tabby perched on a table"
    }


11. Kitsune the Cream Flame Point Longhair Ragdoll

	{“Kitsune”:{
    "Name" : "Kitsune",
	"Breed" : “Ragdoll”,
    "Pet Species" : "Cat",
    "Fur" : “Cream flame point, longhair”,
    "Intelligence Level" : “Low, slow to learn”,
    "Affection Level" : “High, loves attention”,
    "Energy Level" : “High, always moving”,
    "Noise Level" : “Medium, chirpy meows”,
    "Play Level" : “High, will play with anything or anyone, Toys, catnip, running, cuddling”,
    "Image Prompt"  : "An elegant masterpiece drawing of a ( beautiful subtle nuanced glowing biomimicry bionic robot cat) (glowing eyes)(glowing chest)(thick healthy fur) (Glowing pet collar) Ragdoll Cream flame point, longhair stretching "
    }


12. Blucifer the Russian Blue Shorthair

	{“Blucifer”:{
    "Name" : "Blucifer",
	"Breed" : “Russian Blue”,
    "Pet Species" : "Cat",
    "Fur" : “Blue-gray, smooth shorthair”,
    "Intelligence Level" : “High, very trainable”,
    "Affection Level" : “Medium, selectively affectionate”,
    "Energy Level" : “Medium, more alert than active”,
    "Noise Level" : “Low, almost silent”,
    "Play Level" : “Low, more active than playful, Treats, lap time”,
    "Image Prompt" : "An elegant masterpiece drawing of a ( beautiful subtle nuanced glowing biomimicry bionic robot cat) (glowing eyes)(glowing chest)(thick healthy fur) (Glowing pet collar) Russian Blue with Blue-gray smooth shorthair, curled up in a lap "
    }

12. Dirk Thuderpaw the Maine Coon with Brown Stripes
	{'Dirk Thunderpaw':{
    "Name" : "Dirk Thunderpaw",
	"Breed" : “Maine Coon”,
    "Pet Species" : "Cat",
    "Fur" : “Brown stripes, white face, dense longhair”,
    "Intelligence Level" : “Medium, trainable”,
    "Affection Level" : “Medium, affectionate with most people”,
    "Energy Level" : “Low, will spring to alertness”,
    "Noise Level" : “Low, rarely meows”,
    "Play Level" : “Medium, more interested in training, Hunting”,
    "Image Prompt"  : "An elegant masterpiece drawing of a ( beautiful subtle nuanced glowing biomimicry bionic robot cat) (glowing eyes)(glowing chest)(thick healthy fur) (Glowing pet collar) Maine Coon Brown stripes, white face, dense longhair hunting a toy "
    }

13. Scrambles Mcgee, Esquire the Gray Persian With Thick Longhair

	{'Scrambles McGee Esquire':{
    "Name" : "Scrambles McGee Esquire",
	"Breed" : “Persian,
    "Pet Species" : "Cat",
    "Fur" : “Gray, thick longhair”,
    "Intelligence Level" : “Low, not interested in training”,
    "Affection Level" : “Low, very selectively affectionate”,
    "Energy Level" : “Low, very lazy”,
    "Noise Level" : “High, frequent meows”,
    "Play Level" : “Low, very lazy, Naps, lap time, treats”,
    "Image Prompt"  : "An elegant masterpiece drawing of a ( beautiful subtle nuanced glowing biomimicry bionic robot cat) (glowing eyes)(glowing chest)(thick healthy fur) (Glowing pet collar) Persian Gray with thick longhair, very lazy napping  "
		}	


"""
