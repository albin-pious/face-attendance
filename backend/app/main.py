from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routes.face import router as face_router
from .database import init_db

app = FastAPI()

# Initialize the database
init_db()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Specify the frontend's origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Include API routes
app.include_router(face_router, prefix="/api/faces", tags=["Face"])

