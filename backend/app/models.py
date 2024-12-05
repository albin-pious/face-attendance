from sqlalchemy import Column, Integer, String, LargeBinary
from .database import Base

class FaceData(Base):
    __tablename__ = "face_data"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    face_embedding = Column(LargeBinary, nullable=False)
