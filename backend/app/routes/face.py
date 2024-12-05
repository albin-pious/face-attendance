from fastapi import APIRouter, Form, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session
from ..database import SessionLocal
from ..services.face_utils import extract_face_embedding, verify_face
from ..models import FaceData
import numpy as np

router = APIRouter()

# Dependency for getting the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register-face")
async def register_face(
    name: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Call extract_face_embedding with the UploadFile object
    embedding = await extract_face_embedding(file)
    
    if embedding is None:
        raise HTTPException(status_code=400, detail="No face detected")
    
    # Convert the embedding to bytes and save it to the database
    db_face = FaceData(name=name, face_embedding=np.array(embedding).tobytes())
    db.add(db_face)
    db.commit()
    return {"message": "Face registered successfully"}

@router.post("/verify-face")
async def verify_face_api(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # Call extract_face_embedding as an async function
    embedding = await extract_face_embedding(file.file)
    
    if embedding is None:
        raise HTTPException(status_code=400, detail="No face detected")
    
    # Retrieve all registered faces from the database
    known_faces = db.query(FaceData).all()
    for face in known_faces:
        # Decode the face embedding from the database
        known_embedding = np.frombuffer(face.face_embedding)
        
        # Verify face similarity
        if verify_face(known_embedding, embedding):
            return {"message": f"Face matched with {face.name}"}
    
    return {"message": "No match found"}
