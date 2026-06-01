import cv2
from ultralytics import YOLO
import time
from collections import Counter
import textwrap
import subprocess

# ---------------------------
# Settings
# ---------------------------
CAMERA_INDEX = 0
SPEAK_EVERY_SECONDS = 5
CONFIDENCE_THRESHOLD = 0.35
MAX_OBJECTS_TO_DESCRIBE = 5

# ---------------------------
# Load YOLO model
# ---------------------------
model = YOLO("yolov8n.pt")

# ---------------------------
# TTS setup using Windows PowerShell speech
# ---------------------------
speech_enabled = True
tts_process = None


def speak_now(text):
    global tts_process

    # If previous speech is still running, do not start another one
    if tts_process is not None and tts_process.poll() is None:
        return

    safe_text = text.replace("'", "''")

    command = (
        "Add-Type -AssemblyName System.Speech; "
        "$speaker = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
        "$speaker.Rate = 0; "
        f"$speaker.Speak('{safe_text}');"
    )

    print(f"[TTS] Speaking: {text}")

    tts_process = subprocess.Popen(
        ["powershell", "-NoProfile", "-Command", command],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


# ---------------------------
# Scene Detection Logic
# ---------------------------
def detect_scene_type(objects):
    if "keyboard" in objects and "mouse" in objects:
        return "a computer workstation"

    if "keyboard" in objects or "laptop" in objects or "tv" in objects:
        return "a technology workspace"

    if "cup" in objects and ("dining table" in objects or "chair" in objects):
        return "a dining or desk area"

    if "car" in objects or "bus" in objects:
        return "an outdoor street scene"

    if "person" in objects:
        return "a scene with people"

    return "an indoor scene"


def get_position(x_center, width):
    if x_center < width * 0.33:
        return "on the left"
    elif x_center < width * 0.66:
        return "in the centre"
    else:
        return "on the right"


def pluralise(label, count):
    if count == 1:
        if label == "person":
            return "a person"
        return f"a {label}"

    irregular = {
        "person": "people",
        "mouse": "mice",
    }

    if label in irregular:
        return f"{count} {irregular[label]}"

    if label.endswith("s"):
        return f"{count} {label}"

    return f"{count} {label}s"


def generate_smart_caption(detections, frame_width):
    labels = [d["label"] for d in detections]
    counts = Counter(labels)

    scene = detect_scene_type(labels)

    object_parts = []
    for obj, count in counts.most_common(MAX_OBJECTS_TO_DESCRIBE):
        object_parts.append(pluralise(obj, count))

    if object_parts:
        sentence = f"This appears to be {scene} with " + ", ".join(object_parts)
    else:
        sentence = "No clear objects detected"

    spatial_parts = []
    used_spatial_labels = set()

    for d in detections:
        label = d["label"]

        if label in ["person", "cup", "mouse", "keyboard", "laptop", "cell phone", "tv"] and label not in used_spatial_labels:
            pos = get_position(d["x_center"], frame_width)
            spatial_parts.append(f"{label} {pos}")
            used_spatial_labels.add(label)

        if len(spatial_parts) >= 3:
            break

    if spatial_parts:
        sentence += ". Notably, " + ", ".join(spatial_parts)

    return sentence + "."


def draw_multiline_text(frame, text, x, y):
    wrapped_lines = textwrap.wrap(text, width=70)

    for i, line in enumerate(wrapped_lines[:3]):
        cv2.putText(
            frame,
            line,
            (x, y + i * 28),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2
        )


# ---------------------------
# Open webcam
# ---------------------------
cap = cv2.VideoCapture(CAMERA_INDEX)

if not cap.isOpened():
    print("Camera not working")
    exit()

next_speak_time = time.monotonic() + 2
current_description = "Starting SceneAssist."

print("SceneAssist running.")
print("Press Q to quit.")
print("Press S to toggle speech on/off.")
print("Press R to repeat current caption immediately.")

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame_height, frame_width, _ = frame.shape

    results = model(frame, verbose=False)

    detections = []

    for r in results:
        for box in r.boxes:
            confidence = float(box.conf[0])

            if confidence < CONFIDENCE_THRESHOLD:
                continue

            cls_id = int(box.cls[0])
            label = model.names[cls_id]

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            x_center = (x1 + x2) / 2

            detections.append({
                "label": label,
                "x_center": x_center,
                "confidence": confidence
            })

            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            cv2.putText(
                frame,
                f"{label} {confidence:.2f}",
                (x1, max(y1 - 5, 20)),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

    if detections:
        current_description = generate_smart_caption(detections, frame_width)
    else:
        current_description = "No clear objects detected."

    draw_multiline_text(frame, current_description, 10, 30)

    status_text = "Speech: ON" if speech_enabled else "Speech: OFF"
    cv2.putText(
        frame,
        status_text,
        (10, frame_height - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 255) if speech_enabled else (0, 0, 255),
        2
    )

    now = time.monotonic()

    if speech_enabled and now >= next_speak_time:
        speak_now(current_description)
        next_speak_time = now + SPEAK_EVERY_SECONDS

    cv2.imshow("Scene Assist - Real Time", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("q"):
        break

    if key == ord("s"):
        speech_enabled = not speech_enabled
        print("Speech enabled:", speech_enabled)

    if key == ord("r"):
        if speech_enabled:
            speak_now(current_description)
            next_speak_time = time.monotonic() + SPEAK_EVERY_SECONDS

cap.release()
cv2.destroyAllWindows()