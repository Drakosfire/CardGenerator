import ast
import gc
from openai import OpenAI
from prompts import prompt_instructions
client = OpenAI()

def load_llm(user_input):
    prompt = f"{user_input}"
    print(prompt)
    response = client.chat.completions.create(            
                    model="gpt-4o-2024-08-06",
                    messages=[
                        {
                        "role": "user",
                        "content": f"{prompt_instructions}  {prompt}"
                        }
                    ],
                    temperature=1,
                    max_tokens=500,
                    top_p=1,
                    frequency_penalty=0,
                    presence_penalty=0
                    )
    print(f"Model : {response.model}")
    return response.choices[0].message.content
# Call the LLM and store its output
def call_llm_and_cleanup(user_input, inventory = False): 
    
    llm_output = load_llm(user_input)
    llm_output = "".join(llm_output)
    print(f"llm_output = {llm_output}")
    # llm_output is still available for use here
    return llm_output


