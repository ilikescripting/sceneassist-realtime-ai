from ultralytics import YOLO
import cv2
import time
import os

model = YOLO("yolov8n.pt")

image_folder = "dataset/test_images"

for img_name in os.listdir(image_folder):

    path = os.path.join(image_folder, img_name)
    img = cv2.imread(path)

    start = time.time()

    results = model(img)

    end = time.time()

    objects = []

    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            label = model.names[cls]
            objects.append(label)

    print("Image:", img_name)
    print("Objects:", objects)
    print("Detection Time:", round(end - start, 3), "seconds")
    print()