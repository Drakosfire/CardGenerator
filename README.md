---
title: Drakosfires Dungeons and Dragons Item Card Generator
emoji: 🃏
colorFrom: yellow
colorTo: purple
sdk: gradio
sdk_version: 4.26.0
app_file: app.py
pinned: false
---

# Drakosfire's Dungeons and Dragons Item Card Generator

Welcome to the Drakosfire's Dungeons and Dragons Item Card Generator! This innovative tool harnesses the power of AI to generate unique item cards for your D&D adventures. 

## Overview

This generator leverages an API call to [Replicate](https://replicate.com/) using Llama 3 70b, combined with a custom fine-tuned version of the Stable Diffusion SDXL model. You can find more about the specific modelthis project was based on at [Civitai](https://civitai.com/models/129681/sdxl-faetastic).

## Key Features

- **Custom Fine-Tuning**: The backbone of this generator is a fine-tuned Stable Diffusion SDXL model, specifically optimized for generating high-quality, fantasy-themed images on a unique card border that is themed by your imagination.

- **Consistent Card Design**: To ensure each card maintains a uniform appearance, a LoRA (Locally Optimized Representation Approximation) technique was used. This involved training the model with a hand-crafted dataset of card border images, enabling the system to generate new cards with consistent text and image spaces where the generated text and images can be elegantly integrated.

## How It Works

1. Your intitial text along with the prompt is sent to Llama 3 70b to generate a structured python dictionary.
2. This new text will populate in interactive text fields. If it isn't perfect you can edit the text to fit your item.
3. THe final text field is the Stable Diffusion prompt, these generate like one sentence stories describing the scene of your item. This field can also be edited.
4. **Image and Text Generation**: Now generate 4 card template without text and pick your favorite.
5. Finally, add text to your favorite template.
3. **Result**: The final product is a beautifully crafted D&D item card, ready for use in your gaming sessions.

## Example Cards

Below are a few examples of the item cards generated using our tool:

![Example Card 1](url-to-example-card1)
![Example Card 2](url-to-example-card2)

We hope you enjoy enhancing your Dungeons and Dragons experience with this unique tool. Happy adventuring!
