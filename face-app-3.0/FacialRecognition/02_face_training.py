import face_recognition
import os
import numpy as np
import pickle

# Path for the face image dataset
dataset_path = 'dataset'
trainer_path = 'trainer'

print("Face recognition version:", face_recognition.__version__)

# Ensure the trainer directory exists
if not os.path.exists(trainer_path):
    os.makedirs(trainer_path)

# Initialize the face encodings and labels list
face_encodings = []
ids = []

# Function to encode images and associate them with unique IDs
def encode_images_and_labels(dataset_path):
    image_paths = [os.path.join(dataset_path, f) for f in os.listdir(dataset_path)]
    for image_path in image_paths:
        # Extract ID from the image filename (e.g., 'User.1.jpg' -> ID = 1)
        try:
            id = int(os.path.split(image_path)[-1].split(".")[1])
        except ValueError:
            print(f"Skipping {image_path}: Unable to extract ID.")
            continue
        
        # Load the image using face_recognition
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)
        
        # If a face is detected, encode it
        if len(face_locations) > 0:
            face_encoding = face_recognition.face_encodings(image, face_locations)[0]
            face_encodings.append(face_encoding)
            ids.append(id)
        else:
            print(f"No face detected in {image_path}. Skipping...")

    return face_encodings, ids

print("\n[INFO] Encoding faces. This might take a while...")
face_encodings, ids = encode_images_and_labels(dataset_path)

# Save the encodings and IDs for later use
trained_data = {
    "encodings": face_encodings,
    "ids": ids
}

with open(os.path.join(trainer_path, "trainer.pkl"), "wb") as f:
    pickle.dump(trained_data, f)

print(f"\n[INFO] {len(ids)} faces encoded and saved to {os.path.join(trainer_path, 'trainer.pkl')}")
