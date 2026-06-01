# SceneAssist: Real-Time AI Scene Description

SceneAssist is a real-time accessibility-focused computer vision prototype that uses YOLOv8, OpenCV and speech output to generate spoken scene descriptions from a live camera feed.

The project was developed as part of a final year BSc Computer Science dissertation exploring lightweight AI frameworks for visually impaired users.

To run code for realtime camera, use the following command
python -m experiments.realtime_scene

To run code to detect and caption saved images, use the following command
python -m experiments.fusion_test

This is because we are running these files as packages and not regularly, hence the __init__.py files seen in the folder.
