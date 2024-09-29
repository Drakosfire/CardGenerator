---
title: Drakosfires Dungeons and Dragons Item Card Generator
emoji: 🃏
colorFrom: yellow
colorTo: purple
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
---

# Drakosfire's Cyber Pet Card Generator

This is a tool built to generate custom cyborg pets for an unnanounced creative project.

## Overview

This generator leverages an API call to FAL.ai to generate images with a custom LoRA trained off of my card dataset as well as OpenAI's GPT-4o to generate text and image prompts for the images.

## Key Features

- **Custom Fine-Tuning**: The backbone of this generator is a fine-tuned Flux.1 model, specifically optimized for generating high-quality, pet images on a unique card border that is flavored by your imagination.

- **Consistent Card Design**: To ensure each card maintains a uniform appearance, a LoRA (Low-Rank Adaptation) technique was used. This involved training the model with a hand-crafted dataset of card border images, enabling the system to generate new cards with consistent text and image spaces where the generated text and images can be elegantly integrated.

## How It Works

1. Your intitial text along with the prompt is sent to OpenAI's GPT-4o to generate a JSON.
2. This JSON will be parsed into textboxes to review and edit. 
3. The final text field is the image prompt, these generate like one sentence stories describing the scene of your pet.
4. **Image and Text Generation**: Now generate 4 blank cards in about 15 seconds.
5. Finally, click the add text button to add text to your favorite template.
3. **Result**: The final product is a beautifully crafted collectible pet card.

## Example Cards

Below are a few examples of the item cards I've generated:

![Carved Wooden Dinosaur Toy](https://cdn-lfs-us-1.huggingface.co/repos/cb/b4/cbb436e53a2021c9535cec40c6360a89a1d6f5e42bc18d88bbd2da335dde82bd/aa2ca06939fa4db1c30631f01f389e40f2b3f8018e91cfbb127eed56f31e70e8?response-content-disposition=inline%3B+filename*%3DUTF-8%27%27CarvedWoodenDinosaurToy.png%3B+filename%3D%22CarvedWoodenDinosaurToy.png%22%3B&response-content-type=image%2Fpng&Expires=1714445274&Policy=eyJTdGF0ZW1lbnQiOlt7IkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTcxNDQ0NTI3NH19LCJSZXNvdXJjZSI6Imh0dHBzOi8vY2RuLWxmcy11cy0xLmh1Z2dpbmdmYWNlLmNvL3JlcG9zL2NiL2I0L2NiYjQzNmU1M2EyMDIxYzk1MzVjZWM0MGM2MzYwYTg5YTFkNmY1ZTQyYmMxOGQ4OGJiZDJkYTMzNWRkZTgyYmQvYWEyY2EwNjkzOWZhNGRiMWMzMDYzMWYwMWYzODllNDBmMmIzZjgwMThlOTFjZmJiMTI3ZWVkNTZmMzFlNzBlOD9yZXNwb25zZS1jb250ZW50LWRpc3Bvc2l0aW9uPSomcmVzcG9uc2UtY29udGVudC10eXBlPSoifV19&Signature=gfGIhG1lNGANcRcaRo69v9G2IyT%7ETVaSv69ELCzSQ1r9ybHF-TvZAikiWWjWv1lrfubAPmwF3Wmvih7YreEqMgVr6rbxWmqVK%7EjO%7Eylz5Ow8wQM8a9dyiYn874oV0Uz34inXRejJ6JK7FquX%7EZcm95qcqKUhNjjl6hkN3OqbMRhViYqClDl3VhKOgvI0CPJTSfYxPOfNGwPPZoW2d%7EAQRSYeT6gex3CrE8H73wND4pTfOiDRHy3EfHm3pF%7EGjYcnQRaBm%7EMPSe93I7cmu05EgVwX-LsQAYxDLeFAkCIi3qJTrbBxRG551g%7Ew3%7E1iwfWtcOZi3vqWLWpKkNJcrpBX4g__&Key-Pair-Id=KCD77M1F0VK2B)

![Cookie Mimic](https://cdn-lfs-us-1.huggingface.co/repos/cb/b4/cbb436e53a2021c9535cec40c6360a89a1d6f5e42bc18d88bbd2da335dde82bd/10a137ac3cf8bcb509423f626788af61c27989847cd8c6b23bf36e59443a3bde?response-content-disposition=inline%3B+filename*%3DUTF-8%27%27CookieMimic.png%3B+filename%3D%22CookieMimic.png%22%3B&response-content-type=image%2Fpng&Expires=1714445306&Policy=eyJTdGF0ZW1lbnQiOlt7IkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTcxNDQ0NTMwNn19LCJSZXNvdXJjZSI6Imh0dHBzOi8vY2RuLWxmcy11cy0xLmh1Z2dpbmdmYWNlLmNvL3JlcG9zL2NiL2I0L2NiYjQzNmU1M2EyMDIxYzk1MzVjZWM0MGM2MzYwYTg5YTFkNmY1ZTQyYmMxOGQ4OGJiZDJkYTMzNWRkZTgyYmQvMTBhMTM3YWMzY2Y4YmNiNTA5NDIzZjYyNjc4OGFmNjFjMjc5ODk4NDdjZDhjNmIyM2JmMzZlNTk0NDNhM2JkZT9yZXNwb25zZS1jb250ZW50LWRpc3Bvc2l0aW9uPSomcmVzcG9uc2UtY29udGVudC10eXBlPSoifV19&Signature=YRlqcf2gr0cb1sgJr4O-SXsj0q%7EgcJ6rWc%7E1TOSJoKC11J8LUCj1FRf6yTus5xlXbA97Zek-ynUGFAbOKkfY5TctoHECjX3cB5GJb6VmC47YUQmG4DggamnD2qGwTP37h-120u-uKeciK9FAtOqz1vQZW01IlkZYybaaSuo0pdyqiyaq%7E1ywI-B63gaQbgrN8RelwhB9x%7E0y0x-KiwM80xAD%7E5tBDruHRp2HAIT3AWVKKxLZelAKBNog5KTOrwF9cyE6q1m-IW9LKyrbazUNISU8h8QPts04VQH0hd66ZKg1YaNV5l%7EwhCem9wGkJ18p2ZNMYFEH6W4-85%7EuYsKM5A__&Key-Pair-Id=KCD77M1F0VK2B)

![Ridiculously Cute Kitten](https://cdn-lfs-us-1.huggingface.co/repos/cb/b4/cbb436e53a2021c9535cec40c6360a89a1d6f5e42bc18d88bbd2da335dde82bd/863ef9235c94e60fd7176db237e3939f67c6a22bce3015712ff2336a49065f83?response-content-disposition=inline%3B+filename*%3DUTF-8%27%27Ridiculouslycutekitten.png%3B+filename%3D%22Ridiculouslycutekitten.png%22%3B&response-content-type=image%2Fpng&Expires=1714445494&Policy=eyJTdGF0ZW1lbnQiOlt7IkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTcxNDQ0NTQ5NH19LCJSZXNvdXJjZSI6Imh0dHBzOi8vY2RuLWxmcy11cy0xLmh1Z2dpbmdmYWNlLmNvL3JlcG9zL2NiL2I0L2NiYjQzNmU1M2EyMDIxYzk1MzVjZWM0MGM2MzYwYTg5YTFkNmY1ZTQyYmMxOGQ4OGJiZDJkYTMzNWRkZTgyYmQvODYzZWY5MjM1Yzk0ZTYwZmQ3MTc2ZGIyMzdlMzkzOWY2N2M2YTIyYmNlMzAxNTcxMmZmMjMzNmE0OTA2NWY4Mz9yZXNwb25zZS1jb250ZW50LWRpc3Bvc2l0aW9uPSomcmVzcG9uc2UtY29udGVudC10eXBlPSoifV19&Signature=Awm-rIF7be1FRdKIU2zR-cxZa3KtR7FcYmPgVTqfaa2oMKZhU2vkG3lLHXimFvVuXbiv8Rd4ZnijffjWyEBWs6FV5L2JFQ2jG%7EDhlBIdWj-6skbvYwgxsbAfDclBbBv3zyZs%7EDK0rzEqvIDdd8Avud9NtXvyMpSFZTx2zUzGMp1saHLaYH2uU91z7zWHLhnL0XVW1JvY6RbaNx0Ydtx42r1IWqVpLqpB6yGoeIU2PBQCpNiuY61zwjOCg2iMM3OuXJ56eULFXtnrbJbqDSZnlIibELCZ%7EJQCozeVSvi-OK6HOkD7W7tPSnbfx2f9GIY1FkmzoXh-K7cFNL-CxYnCjw__&Key-Pair-Id=KCD77M1F0VK2B)



