# SceneAssist: Real-Time AI Scene Description for Visually Impaired Users

## Overview

SceneAssist is a real-time computer vision prototype developed as part of a final year BSc Computer Science dissertation.

The project investigates how lightweight artificial intelligence techniques can be combined to provide accessible scene descriptions for visually impaired users without relying on cloud services.

Using a live webcam feed, the system detects objects within the environment, generates contextual descriptions, and delivers spoken feedback through text-to-speech. The objective is to improve situational awareness while maintaining low latency and preserving user privacy through local processing.

---

## Dissertation Title

**A Novel Lightweight AI Framework for Real-Time, Low-Latency Scene Description for Visually Impaired Users: Design, Implementation, and Evaluation**

---

## Key Features

* Real-time object detection using YOLOv8 Nano
* Live webcam scene analysis
* Context-aware scene description generation
* Spatial awareness (left, centre, right positioning)
* Spoken audio feedback using text-to-speech
* Fully local processing with no cloud dependency
* Modular architecture for future AI model integration
* Experimental evaluation using multiple real-world test scenes

---

## Technologies Used

* Python
* OpenCV
* YOLOv8 (Ultralytics)
* PyTorch
* Hugging Face Transformers
* BLIP Image Captioning
* Windows Speech Synthesis
* Computer Vision
* Artificial Intelligence
* Accessibility Technologies

---

## Project Structure

```text
FYP/
│
├── dataset/
│   └── test_images/
│
├── experiments/
│   ├── realtime_scene.py
│   ├── detection_test.py
│   ├── caption_test.py
│   └── fusion_test.py
│
├── utils/
│   └── description_logic.py
│
├── requirements.txt
└── README.md
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/ilikescripting/sceneassist-realtime-ai.git
cd sceneassist-realtime-ai
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Usage

### Real-Time Scene Description

Launch the webcam-based scene description system:

```bash
python -m experiments.realtime_scene
```

Controls:

* Q = Quit
* S = Toggle speech output
* R = Repeat current description

---

### Object Detection Testing

Run object detection against images stored in:

```text
dataset/test_images/
```

```bash
python -m experiments.detection_test
```

---

### Image Captioning Testing

```bash
python -m experiments.caption_test
```

---

### Detection and Caption Fusion Testing

```bash
python -m experiments.fusion_test
```

---

## Experimental Results

The system was evaluated using a collection of indoor and outdoor scenes including:

* Offices
* Classrooms
* Streets
* Cafés
* Parks
* Train stations
* Supermarkets

Results demonstrated:

* Object detection latency typically below 60ms
* End-to-end scene description generation within approximately 0.6–1.1 seconds
* Accurate identification of common everyday objects
* Effective spoken scene summaries suitable for accessibility applications

---

## Research Contributions

This project contributes:

1. A lightweight AI framework for real-time scene understanding.
2. Integration of object detection, image captioning, and speech output within a single pipeline.
3. A privacy-preserving approach that performs processing locally without cloud services.
4. An accessibility-focused design intended to support visually impaired users.

---

## Future Improvements

Potential future developments include:

* Mobile deployment on Android devices
* More advanced vision-language models
* Temporal scene tracking across consecutive frames
* Improved object prioritisation and contextual reasoning
* User testing with visually impaired participants
* GPU and NPU acceleration for mobile hardware

---

## Dataset

The original dissertation dataset contained publicly sourced images used for academic evaluation.

To avoid redistributing third-party content, images are not included in this repository.

Users may add their own images to:

```text
dataset/test_images/
```

for experimentation with the testing scripts.

---

## Author

**Y. Ali**

BSc Computer Science

---

## Licence

This project is provided for educational and research purposes.
