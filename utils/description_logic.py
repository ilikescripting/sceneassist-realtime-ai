from collections import Counter


def clean_caption(caption):
    if not caption:
        return ""
    caption = caption.strip()
    return caption[0].upper() + caption[1:]


def generate_description(detected_objects, caption):
    # Count occurrences of detected objects
    counts = Counter(detected_objects)

    # Get top 3 most common objects
    most_common = counts.most_common(3)

    object_phrases = []
    for obj, count in most_common:
        if count == 1:
            object_phrases.append(obj)
        else:
            object_phrases.append(f"{count} {obj}s")

    # Build base description
    if object_phrases:
        description = "I can see " + ", ".join(object_phrases)
    else:
        description = "I can see a scene"

    # Clean caption
    caption = clean_caption(caption)

    # Avoid repeating same info
    if caption:
        if not any(obj in caption.lower() for obj, _ in most_common):
            description += ". " + caption
        else:
            description += "."
    else:
        description += "."

    return description


# Test (optional)
if __name__ == "__main__":
    objects = ["person", "person", "chair", "table", "person"]
    caption = "a group of people sitting at a table"
    print(generate_description(objects, caption))