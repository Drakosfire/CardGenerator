from llama_cpp import Llama
import ast
import gc
import torch

model_path = "models/starling-lm-7b-alpha.Q8_0.gguf"
# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.


# Simple inference example
def load_llm(user_input):
  llm = Llama(
  model_path=model_path,
  n_ctx=8192,  # The max sequence length to use - note that longer sequence lengths require much more resources
  n_threads=8,            # The number of CPU threads to use, tailor to your system and the resulting performance
  n_gpu_layers=-1         # The number of layers to offload to GPU, if you have GPU acceleration available
)
  return llm(
  f"GPT4 User: {prompt_instructions}  the item is {user_input}: <|end_of_turn|>GPT4 Assistant:", # Prompt
  max_tokens=512,  # Generate up to 512 tokens
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
            print("Item dictionary is valid")
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
prompt_instructions = """ **Purpose**: Generate a structured inventory entry for a specific item as a hashmap. Follow the format provided in the examples below.

**Instructions**:
1. Replace `{item}` with the name of the user item, DO NOT CHANGE THE USER ITEM NAME enclosed in single quotes (e.g., `'Magic Wand'`).
2. Ensure your request is formatted as a hashmap. 
3. Weapons MUST have a key 'Damage' 
4. The description should be brief and puncy, or concise and thoughtful.
5. The quote and SD Prompt MUST be inside double quotations ie " ".
6. The quote is from the perspective of someone commenting on the impact of the {item} on their life
7. Value should be assigned as an integer of copper pieces (cp), silver pieces (sp), electrum pieces (ep), gold pieces (gp), and platinum pieces (pp). 
8. Use this table for reference on value : 
1 cp 	1 lb. of wheat
2 cp 	1 lb. of flour or one chicken
5 cp 	1 lb. of salt
1 sp 	1 lb. of iron or 1 sq. yd. of canvas
5 sp 	1 lb. of copper or 1 sq. yd. of cotton cloth
1 gp 	1 lb. of ginger or one goat
2 gp 	1 lb. of cinnamon or pepper, or one sheep
3 gp 	1 lb. of cloves or one pig
5 gp 	1 lb. of silver or 1 sq. yd. of linen
10 gp 	1 sq. yd. of silk or one cow
15 gp 	1 lb. of saffron or one ox
50 gp 	1 lb. of gold
500 gp 	1 lb. of platinum


300 gp +1 Melee or Ranged Weapon 
2000 gp +2 Melee or Ranged Weapon 
10000 gp  +3 Melee or Ranged Weapon 
300 gp +1 Armor Uncommon
2000 gp +2 Armor Rare
10000 gp +3 Armor Very Rare
300 gp +1 Shield Uncommon
2000 gp +2 Shield Rare
10000 gp +3 Shield Very Rare

9. Examples of Magical Scroll Value:
    Common: 50-100 gp
    Uncommon: 101-500 gp
    Rare: 501-5000 gp
    Very rare: 5001-50000 gp
    Legendary: 50001+ gp

A scroll's rarity depends on the spell's level:
    Cantrip-1: Common
    2-3: Uncommon
    4-5: Rare
    6-8: Very rare
    9: Legendary

10. Explanation of Mimics:
Mimics are shapeshifting predators able to take on the form of inanimate objects to lure creatures to their doom. In dungeons, these cunning creatures most often take the form of doors and chests, having learned that such forms attract a steady stream of prey.
Imitative Predators. Mimics can alter their outward texture to resemble wood, stone, and other basic materials, and they have evolved to assume the appearance of objects that other creatures are likely to come into contact with. A mimic in its altered form is nearly unrecognizable until potential prey blunders into its reach, whereupon the monster sprouts pseudopods and attacks.
When it changes shape, a mimic excretes an adhesive that helps it seize prey and weapons that touch it. The adhesive is absorbed when the mimic assumes its amorphous form and on parts the mimic uses to move itself.
Cunning Hunters. Mimics live and hunt alone, though they occasionally share their feeding grounds with other creatures. Although most mimics have only predatory intelligence, a rare few evolve greater cunning and the ability to carry on simple conversations in Common or Undercommon. Such mimics might allow safe passage through their domains or provide useful information in exchange for food.

11. 
**Format Example**:
- **Dictionary Structure**:
    
    {"{item}": {
    'Name': "{item name}",
    'Type': '{item type}',
    'Rarity': '{item rarity},
    'Value': '{item value}',
    'Properties': ["{property1}", "{property2}", ...],
    'Damage': '{damage formula} , '{damage type}',
    'Weight': '{weight}',
    'Description': "{item description}",
    'Quote': "{item quote}",
    'SD Prompt': "{special description for the item}"
    } }
    
- **Input Placeholder**:
    - "{item}": Replace with the item name, ensuring it's wrapped in single quotes.

**Output Examples**:
1. Cloak of Whispering Shadows Entry:
    
    {"Cloak of Whispering Shadows": {
    'Name': 'Cloak of Whispering Shadows',
    'Type': 'Cloak',
    'Rarity': 'Very Rare', 
    'Value': '7500 gp',
    'Properties': ["Grants invisibility in dim light or darkness","Allows communication with shadows for gathering information"],
    'Weight': '1 lb',
    'Description': "A cloak woven from the essence of twilight, blending its wearer into the shadows. Whispers of the past and present linger in its folds, offering secrets to those who listen.",
    'Quote': "In the embrace of night, secrets surface in the silent whispers of the dark.",
    'SD Prompt': " Cloak of deep indigo almost black, swirling patterns that shift and move with every step. As it drapes over one's shoulders, an eerie connection forms between the wearer and darkness itself." 
    } }   
    
2. Health Potion Entry:
    
    {"Health Potion": {
    'Name' : "Health Portion",
    'Type' : 'Potion',
    'Rarity' : 'Common',
    'Value': '50 gp',
    'Properties': ["Quafable", "Restores 1d4 + 2 HP upon consumption"],
    'Weight': '0.5 lb',
    'Description': "Contained within this small vial is a crimson liquid that sparkles when shaken, a life-saving elixir for those who brave the unknown.",
    'Quote': "To the weary, a drop of hope; to the fallen, a chance to stand once more.",
    'SD Prompt' : " a small, delicate vial containing a sparkling crimson liquid. Emit a soft glow, suggesting its restorative properties. The vial is set against a dark, ambiguous background." 
    } }     
    
3. Wooden Shield Entry:
    
    {"Wooden Shield": {
    'Name' : "Wooden Shield",
    'Type' : 'Armor, Shield',
    'Rarity': 'Common',
    'Value': '10 gp',
    'Properties': ["+2 AC"],
    'Weight': '6 lb',
    'Description': "Sturdy and reliable, this wooden shield is a simple yet effective defense against the blows of adversaries.",
    'Quote': "In the rhythm of battle, it dances - a barrier between life and defeat.",
    'SD Prompt': " a sturdy wooden shield, a symbol of defense, with a simple yet solid design. The shield, has visible grain patterns and a few battle scars. It stands as a steadfast protector, embodying the essence of a warrior's resilience in the face of adversity." 
    } }
     
4.  Helmet of Perception Entry:
    
    {"Helmet of Perception": {
    'Name' : "Helmet of Perception",
    'Type' : 'Magical Item (armor, helmet)',
    'Rarity': 'Very Rare', 
    'Value': '3000 gp',
    'Properties': ["+ 1 to AC", "Grants the wearer advantage on perception checks", "+5 to passive perception"],
    'Weight': '3 lb',
    'Description': "Forged from mystic metals and enchanted with ancient spells, this helmet offers protection beyond the physical realm.",
    'Quote': "A crown not of royalty, but of unyielding vigilance, warding off the unseen threats that lurk in the shadows.",
    'SD Prompt': " a mystical helmet crafted from enchanted metals, glowing with subtle runes.  imbued with spells, radiates a mystical aura, symbolizing enhanced perception and vigilance,elegant,formidable" 
    } }
    
5. Longbow Entry:
    
    {"Longbow": {
    'Name': "Longbow",
    'Type': 'Ranged Weapon (martial, longbow)',
    'Rarity': 'Common',
    'Value': '50 gp',
    'Properties': ["2-handed", "Range 150/600", "Loading"],
    'Damage': '1d8 + Dex, piercing',
    'Weight': '6 lb',
    'Description': "With a sleek and elegant design, this longbow is crafted for speed and precision, capable of striking down foes from a distance.",
    'Quote': "From the shadows it emerges, a silent whisper of steel that pierces the veil of darkness, bringing justice to those who dare to trespass.",
    'SD Prompt' : "a longbow with intricate carvings and stone inlay with a black string" 
    } }
    

6. Mace Entry:
    
    {"Mace": {
    'Name': "Mace",
    'Type': 'Melee Weapon (martial, bludgeoning)',
    'Rarity': 'Common',
    'Value': '25 gp',
    'Properties': ["Bludgeoning", "One-handed"],
    'Damage': '1d6 + str, bludgeoning',
    'Weight': '6 lb', 
    'Description': "This mace is a fearsome sight, its head a heavy and menacing ball of metal designed to crush bone and break spirits.", 
    'Quote': "With each swing, it sings a melody of pain and retribution, an anthem of justice to those who wield it.", 
    'SD Prompt': "a menacing  metal spike ball mace, designed for bludgeoning, with a heavy, intimidating head, embodying a tool for bone-crushing and spirit-breaking." 
    } }
    
7. Flying Carpet Entry:
    
    {"Flying Carpet": {
    'Name': "Flying Carpet", 
    'Type': 'Magical Item (transportation)', 
    'Rarity': 'Very Rare',
    'Value': '3000 gp', 
    'Properties': ["Flying", "Personal Flight", "Up to 2 passengers", Speed : 60 ft], 
    'Weight': '50 lb', 
    'Description': "This enchanted carpet whisks its riders through the skies, providing a swift and comfortable mode of transport across great distances.",
    'Quote': "Soar above the mundane, and embrace the winds of adventure with this magical gift from the heavens.", 
    'SD Prompt': "a vibrant, intricately patterned flying carpet soaring high in the sky, with clouds and a clear blue backdrop, emphasizing its magical essence and freedom of flight" 
    } }
    
8. Tome of Endless Stories Entry:
    
    {"Tome of Endless Stories": {
    'Name': "Tome of Endless Stories",
    'Type': 'Book',
    'Rarity': 'Uncommon'
    'Value': '500 gp',
    'Properties': [
        "Generates a new story or piece of lore each day",
        "Reading a story grants insight or a hint towards solving a problem or puzzle"
    ],
    'Weight': '3 lbs',
    'Description': "An ancient tome bound in leather that shifts colors like the sunset. Its pages are never-ending, filled with tales from worlds both known and undiscovered.",
    'Quote': "Within its pages lie the keys to a thousand worlds, each story a doorway to infinite possibilities.",
    'SD Prompt': "leather-bound with gold and silver inlay, pages appear aged but are incredibly durable, magical glyphs shimmer softly on the cover." 
    } }    
    
9. Ring of Miniature Summoning Entry:
    
    {"Ring of Miniature Summoning": {
    'Name': "Ring of Miniature Summoning",
    'Type': 'Ring',
    'Rarity': 'Rare',
    'Value': '1500 gp',
    'Properties': ["Summons a miniature beast ally once per day", "Beast follows commands and lasts for 1 hour", "Choice of beast changes with each dawn"],
    'Weight': '0 lb',
    'Description': "A delicate ring with a gem that shifts colors. When activated, it brings forth a small, loyal beast companion from the ether.",
    'Quote': "Not all companions walk beside us. Some are summoned from the depths of magic, small in size but vast in heart.",
    'SD Prompt': "gemstone with changing colors, essence of companionship and versatility." 
    } } 
     

10. Spoon of Tasting Entry:
    
    {"Spoon of Tasting": {
    'Name': "Spoon of Tasting",
    'Type': 'Spoon',
    'Rarity': 'Uncommon',
    'Value': '200 gp',
    'Properties': ["When used to taste any dish, it can instantly tell you all the ingredients", "Provides exaggerated compliments or critiques about the dish"],
    'Weight': '0.2 lb',
    'Description': "A culinary critic’s dream or nightmare. This spoon doesn’t hold back its opinions on any dish it tastes.",
    'Quote': "A spoonful of sugar helps the criticism go down.",
    'SD Prompt': "Looks like an ordinary spoon, but with a mouth that speaks more than you’d expect."
    } }
    
11. Infinite Scroll Entry: 
    
    {"Infinite Scroll": {
    'Name': "Infinite Scroll",
    'Type': 'Magical Scroll',
    'Rarity': 'Legendary',
    'Value': '25000',
    'Properties': [
        "Endlessly Extends with New Knowledge","Reveals Content Based on Reader’s Need or Desire","Cannot be Fully Transcribed"],
    'Weight': '0.5 lb',
    'Description': "This scroll appears to be a standard parchment at first glance. However, as one begins to read, it unrolls to reveal an ever-expanding tapestry of knowledge, lore, and spells that seems to have no end.",
    'Quote': "In the pursuit of knowledge, the horizon is ever receding. So too is the content of this scroll, an endless journey within a parchment’s bounds.",
    'SD Prompt': "A seemingly ordinary scroll that extends indefinitely" 
    } }
    
12. Mimic Treasure Chest Entry:
    
    {"Mimic Treasure Chest": {
    'Name': "Mimic Treasure Chest",
    'Type': 'Trap',
    'Rarity': 'Rare',
    'Value': '1000 gp',  # Increased value reflects its dangerous and rare nature
    'Properties': ["Deceptively inviting","Springs to life when interacted with","Capable of attacking unwary adventurers"],
    'Weight': '50 lb',  # Mimics are heavy due to their monstrous nature
    'Description': "This enticing treasure chest is a deadly Mimic, luring adventurers with the promise of riches only to unleash its monstrous true form upon those who dare to approach, turning their greed into a fight for survival.",
    'SD Prompt': "A seemingly ordinary treasure chest that glimmers with promise. Upon closer inspection, sinister, almost living edges move with malice, revealing its true nature as a Mimic, ready to unleash fury on the unwary."
    } }
    
13. Hammer of Thunderbolts Entry:
    
    {'Hammer of Thunderbolts': {
    'Name': 'Hammer of Thunderbolts',
    'Type': 'Melee Weapon (maul, bludgeoning)',
    'Rarity': 'Legendary',
    'Value': '16000',
    'Damage': '2d6 + 1 (martial, bludgeoning)',
    'Properties': ["requires attunement","Giant's Bane","must be wearing a belt of giant strength and gauntlets of ogre power","Str +4","Can excees 20 but not 30","20 against giant, DC 17 save against death","5 charges, expend 1 to make a range attack 20/60","ranged attack releases thunderclap on hit, DC 17 save against stunned 30 ft","regain 1d4+1 charges at dawn"],
    'Weight': 15 lb',
    'Description': "God-forged and storm-bound, a supreme force, its rune-etched head blazing with power. More than a weapon, it's a symbol of nature's fury, capable of reshaping landscapes and commanding elements with every strike.",
    'Quote': "When the skies rage and the earth trembles, know that the Hammer of Thunderbolts has found its mark. It is not merely a weapon, but the embodiment of the storm\'s wrath wielded by those deemed worthy.",
    'SD Prompt': "It radiates with electric energy, its rune-etched head and storm-weathered leather grip symbolizing its dominion over storms. In its grasp, it pulses with the potential to summon the heavens' fury, embodying the tempest's raw power."
    } }

14. Shadow Lamp Entry:  

    {'Shadow Lamp': {
    'Name': 'Shadow Lamp',
    'Type': 'Magical Item',
    'Rarity': 'Uncommon',
    'Value': '500 gp',
    'Properties': ["Provides dim light in a 20-foot radius", "Invisibility to darkness-based senses", "Can cast Darkness spell once per day"],
    'Weight': '1 lb',
    'Description': "A small lamp carved from obsidian and powered by a mysterious force, it casts an eerie glow that illuminates its surroundings while making the wielder invisible to those relying on darkness-based senses.",
    'Quote': "In the heart of shadow lies an unseen light, casting away darkness and revealing what was once unseen.",
    'SD Prompt': "Glass lantern filled with inky swirling shadows, black gaseous clouds flow out, blackness flows from it, spooky, sneaky"
    } }

15. Dark Mirror:

    {'Dark Mirror': {
    'Name': 'Dark Mirror',
    'Type': 'Magical Item',
    'Rarity': 'Rare',
    'Value': '600 gp',
    'Properties': ["Reflects only darkness when viewed from one side", "Grants invisibility to its reflection", "Can be used to cast Disguise Self spell once per day"],
    'Weight': '2 lb',
    'Description': "An ordinary-looking mirror with a dark, almost sinister tint. It reflects only darkness and distorted images when viewed from one side, making it an ideal tool for spies and those seeking to hide their true identity.",
    'Quote': "A glass that hides what lies within, a surface that reflects only darkness and deceit.",
    'SD Prompt': "Dark and mysterious black surfaced mirror with an obsidian flowing center with a tint of malice, its surface reflecting nothing but black and distorted images, swirling with tendrils, spooky, ethereal"
    } }

16. Moon-Touched Greatsword Entry:
    
    {'Moon-Touched Greatsword':{
    'Name': 'Moontouched Greatsword',
    'Type': 'Melee Weapon (greatsword, slashing)',
    'Rarity': 'Very Rare',
    'Value': '8000 gp',
    'Damage': '2d6 + Str slashing',
    'Properties': ["Adds +2 to attack and damage rolls while wielder is under the effects of Moonbeam or Daylight spells", "Requires attunement"],
    'Weight': '6 lb',
    'Description': "Forged from lunar metal and imbued with celestial magic, this greatsword gleams like a silver crescent moon, its edge sharp enough to cut through the darkest shadows.",
    'Quote': "With each swing, it sings a melody of light that pierces the veil of darkness, a beacon of hope and justice.",
    'SD Prompt': "A silver greatsword with a crescent moon-shaped blade that reflects a soft glow, reminiscent of the moon's radiance. The hilt is wrapped in silvery leather, and the metal seems to shimmer and change with the light, reflecting the lunar cycles."
    } }
"""
