from fastapi import HTTPException
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models, schemas
from database import engine, SessionLocal

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Assignment Manager API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows requests from any origin (like your Flutter web app)
    allow_credentials=True,
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Dependency to open and close the database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- API ROUTES ---

@app.get("/")
async def root():
    return {"message": "Backend is running successfully"}

# Route to create a new user
@app.post("/api/v1/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Create the SQLAlchemy model instance
    db_user = models.User(name=user.name, email=user.email, is_professor=user.is_professor)
    # Save it to the database
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
# Route to create a new assignment
@app.post("/api/v1/assignments/", response_model=schemas.Assignment)
def create_assignment(assignment: schemas.AssignmentCreate, db: Session = Depends(get_db)):
    db_assignment = models.Assignment(
        title=assignment.title, 
        description=assignment.description, 
        professor_id=assignment.professor_id
    )
    db.add(db_assignment)
    db.commit()
    db.refresh(db_assignment)
    return db_assignment

# Route to get all assignments
@app.get("/api/v1/assignments/", response_model=list[schemas.Assignment])
def read_assignments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    assignments = db.query(models.Assignment).offset(skip).limit(limit).all()
    return assignments

# Route to simulate login by fetching a user by email
@app.get("/api/v1/users/{email}", response_model=schemas.User)
def get_user_by_email(email: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
# Route to submit an assignment answer
@app.post("/api/v1/submissions/", response_model=schemas.Submission)
def create_submission(submission: schemas.SubmissionCreate, db: Session = Depends(get_db)):
    db_submission = models.Submission(
        content=submission.content,
        assignment_id=submission.assignment_id,
        student_id=submission.student_id
    )
    db.add(db_submission)
    db.commit()
    db.refresh(db_submission)
    return db_submission
# Route to fetch all submissions for a specific assignment
@app.get("/api/v1/assignments/{assignment_id}/submissions", response_model=list[schemas.Submission])
def get_submissions_for_assignment(assignment_id: int, db: Session = Depends(get_db)):
    submissions = db.query(models.Submission).filter(models.Submission.assignment_id == assignment_id).all()
    return submissions