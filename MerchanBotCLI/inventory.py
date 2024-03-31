

inventory = {
    'Shortsword': {
            'Name' : 'Shortsword',
            'Type' : 'Melee Weapon (martial, sword)',
            'Value': '10 gp',
            'Properties': ['Finesse, Light '],
            'Damage': '1d6 + proficiency + Dex or Str',
            'Weight': '2 lb',
            'Description': 'Gleaming with a modest radiance, the shortsword boasts a keen edge and a leather-wrapped hilt, promising both grace and reliability in the heat of combat.',
            'Quote': 'In the heart of battle, the shortsword proves not just a weapon, but a steadfast companion, whispering paths of valor to those who wield it.',
            'SD Description' : 'high resolution, blank magic card,detailed high quality intricate border, decorated textbox, high quality magnum opus cgi drawing of a steel shortsword'
                    },          
            
    'Health Potion': {
        'Name' : 'Health Portion',
        'Type' : 'Potion',
        'Value': '50 gp',
        'Properties': ['Quafable', 'Restores 1d4 + 2 HP upon consumption'],
        'Weight': '0.5 lb',
        'Description': 'Contained within this small vial is a crimson liquid that sparkles when shaken, a life-saving elixir for those who brave the unknown.',
        'Quote': 'To the weary, a drop of hope; to the fallen, a chance to stand once more.'
            },
            
            
    'Wooden Shield': {
        'Name' : 'Wooden Shield',
        'Type' : 'Armor, Shield',
        'Value': '15 gp',
        'Properties': ['+2 AC'],
        'Weight': '6 lb',
        'Description': 'Sturdy and reliable, this wooden shield is a simple yet effective defense against the blows of adversaries.',
        'Quote': 'In the rhythm of battle, it dances - a barrier between life and defeat.'
        },
                
    'Magical Helmet': {
        'Name' : 'Magical Helmet of Perception',
        'Type' : 'Magical Item (armor, helmet)',
        'Value': '120 gp',
        'Properties': ['+ 1 to AC', 'Grants the wearer enhanced perception'],
        'Weight': '3 lb',
        'Description': 'Forged from mystic metals and enchanted with ancient spells, this helmet offers protection beyond the physical realm.',
        'Quote': 'A crown not of royalty, but of unyielding vigilance, warding off the unseen threats that lurk in the shadows.'
                }
            }
   
{'id': 'cmpl-5b0ed6c7-2326-473f-8f11-32d3f079edc2',
  'object': 'text_completion', 
  'created': 1709094107, 
  'model': '../models/starling-lm-7b-alpha.Q8_0.gguf', 
  'choices': [{'text': ' Here\'s an example of a structured inventory entry for a Mimic Treasure Chest as per your request:\n\n```python\n{\n    \'Mimic Treasure Chest\': {\n        \'Name\': \'Mimic Treasure Chest\',\n        \'Type\': \'Trap\',\n        \'Rarity\': \'Rare\',\n        \'Value\': \'1000 gp\', \n        \'Properties\': [\n            \'Deceptively inviting\', \n            \'Springs to life when interacted with\', \n            \'Capable of attacking unwary adventurers\'\n            ],\n        \'Weight\': \'50 lb\', \n        \'Description\': \'At first glance, this chest appears to be laden with treasure, beckoning to all who gaze upon it. However, it harbors a deadly secret: it is a Mimic, a cunning and dangerous creature that preys on the greed of adventurers. With its dark magic, it can perfectly imitate a treasure chest, only to reveal its true, monstrous form when approached. Those who seek to plunder its contents might find themselves in a fight for their lives.\',\n        \'Quote\': \'"Beneath the guise of gold and riches lies a predator, waiting with bated breath for its next victim."\',\n        \'SD Prompt\': \'A seemingly ordinary treasure chest that glimmers with promise. Upon closer inspection, sinister, almost living edges move with malice, revealing its true nature as a Mimic, ready to unleash fury on the unwary.\'\n    }\n}\n```\n\nKeep in mind that mimics are typically found in dungeons and are known to take on the form of doors and chests. This example follows that theme while also providing information on the mimic\'s rarity, value, properties, and weight.', 'index': 0, 'logprobs': None, 'finish_reason': 'stop'}], 'usage': {'prompt_tokens': 4287, 'completion_tokens': 405, 'total_tokens': 4692}}