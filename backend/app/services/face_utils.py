import face_recognition
from io import BytesIO
import numpy as np
from PIL import Image

async def extract_face_embedding(image_file):
    try:
        # Read file contents asynchronously
        image_data = await image_file.read()
        print(f"File size: {len(image_data)} bytes")
        
        # Save image for debugging (optional)
        with open("uploaded_image.jpg", "wb") as f:
            f.write(image_data)
        
        # Debug: Try opening and verifying the image
        image = Image.open("uploaded_image.jpg")
        image.show()  # Opens the image to visually inspect it
        
        # Process the image using face_recognition
        image = face_recognition.load_image_file(BytesIO(image_data))
        print(f"Image dimensions: {image.shape}")
        
        embeddings = face_recognition.face_encodings(image)
        print(f"Number of faces detected: {len(embeddings)}")
        
        if not embeddings:
            print("No face detected.")
            return None  # No face detected
        
        return embeddings[0]
    except Exception as e:
        print(f"Error in extracting embedding: {e}")
        return None

# Function to verify if two face embeddings are similar
def verify_face(known_embedding, unknown_embedding, threshold=0.6):
    # Calculate the Euclidean distance between embeddings
    distance = np.linalg.norm(known_embedding - unknown_embedding)
    return distance < threshold  # Return True if distance is below the threshold
