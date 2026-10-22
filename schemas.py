from pydantic import BaseModel

# --- USER SCHEMAS ---
class UserBase(BaseModel):
    name: str
    email: str
    is_professor: bool = False

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        from_attributes = True  # Allows Pydantic to read data from SQLAlchemy models

# --- ASSIGNMENT SCHEMAS ---
class AssignmentBase(BaseModel):
    title: str
    description: str

class AssignmentCreate(AssignmentBase):
    professor_id: int

class Assignment(AssignmentBase):
    id: int
    professor_id: int

    class Config:
        from_attributes = True
class SubmissionCreate(BaseModel):
    content: str
    assignment_id: int
    student_id: int

class Submission(SubmissionCreate):
    id: int

    class Config:
        from_attributes = True