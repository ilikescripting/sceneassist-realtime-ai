from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import time
import os

processor = BlipProcessor.from_pretrained(
"Salesforce/blip-image-captioning-base")

model = BlipForConditionalGeneration.from_pretrained(
"Salesforce/blip-image-captioning-base")

folder = "dataset/test_images"

for img_name in os.listdir(folder):

    path = os.path.join(folder, img_name)
    image = Image.open(path).convert("RGB")

    start = time.time()

    inputs = processor(image, return_tensors="pt")

    output = model.generate(**inputs, max_new_tokens=20)

    caption = processor.decode(output[0], skip_special_tokens=True)

    end = time.time()

    print("Image:", img_name)
    print("Caption:", caption)
    print("Caption Time:", round(end-start,3))
    print()