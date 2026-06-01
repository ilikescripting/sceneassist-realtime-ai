# Test Images

This folder is intentionally left empty.

The original dissertation dataset contained publicly sourced images used for academic evaluation. These images are not included in this repository to avoid redistributing third-party content.

To run the testing scripts (`caption_test.py`, `detection_test.py`, and `fusion_test.py`), add your own image files to:

```
dataset/test_images/
```

Supported formats include:

* JPG
* JPEG
* PNG

Example:

```
dataset/
└── test_images/
    ├── image1.jpg
    ├── image2.jpg
    └── image3.png
```

The real-time webcam prototype (`realtime_scene.py`) does not require any images and can be run directly using a connected webcam.
