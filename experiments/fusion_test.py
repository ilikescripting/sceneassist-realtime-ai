from ultralytics import YOLO
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import cv2
import os
import time

from utils.description_logic import generate_description


yolo = YOLO("yolov8n.pt")

processor = BlipProcessor.from_pretrained(
"Salesforce/blip-image-captioning-base")

caption_model = BlipForConditionalGeneration.from_pretrained(
"Salesforce/blip-image-captioning-base")

folder = "dataset/test_images"


for img_name in os.listdir(folder):

    path = os.path.join(folder, img_name)

    img = cv2.imread(path)
    pil = Image.open(path).convert("RGB")

    start = time.time()

    results = yolo(img)

    objects = []

    for r in results:
        for box in r.boxes:
            label = yolo.names[int(box.cls[0])]
            objects.append(label)

    inputs = processor(pil, return_tensors="pt")

    caption_start = time.time()
    out = caption_model.generate(**inputs, max_new_tokens=20)
    caption_end = time.time()

    caption = processor.decode(out[0], skip_special_tokens=True)

    description = generate_description(objects, caption)

    end = time.time()

    print("Image:", img_name)
    print("Description:", description)
    print("Caption Time:", round(caption_end - caption_start, 3))
    print("Total Time:", round(end-start,3))
    print()