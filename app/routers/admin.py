from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.utils import hash_password  # Function to hash password

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/create-admin")
def create_admin(admin_data: schemas.AdminCreate, db: Session = Depends(get_db)):
    # Check if admin with the same email exists
    existing_admin = db.query(models.Admin).filter(models.Admin.email == admin_data.email).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="Admin with this email already exists")

    # Hash password
    hashed_password = hash_password(admin_data.password)

    # Create admin object
    new_admin = models.Admin(
        name=admin_data.name,
        email=admin_data.email,
        password=hashed_password
    )

    # Add and commit to database
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return {"message": "✅ Admin created successfully!", "admin_id": new_admin.id}

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.utils import hash_password
from app.admin_oauth2 import get_current_admin  # Function to verify token

router = APIRouter(prefix="/admin", tags=["Admin"])

# Create Admin Endpoint (Public)
@router.post("/create-admin")
def create_admin(admin_data: schemas.AdminCreate, db: Session = Depends(get_db)):
    existing_admin = db.query(models.Admin).filter(models.Admin.email == admin_data.email).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="Admin with this email already exists")

    hashed_password = hash_password(admin_data.password)
    new_admin = models.Admin(name=admin_data.name, email=admin_data.email, password=hashed_password)

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return {"message": "✅ Admin created successfully!", "admin_id": new_admin.id}


# Create Job Endpoint (Protected)
@router.post("/create-job")
def create_job(
    job_data: schemas.JobCreate,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(get_current_admin)  # Require login
):
    new_job = models.Job(
        title=job_data.title,
        description=job_data.description,
        registration_link=job_data.registration_link
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return {"message": "✅ Job created successfully!", "job_id": new_job.id}


# Get All Jobs Endpoint (Protected)
@router.get("/jobs", response_model=list[schemas.JobResponse])
def get_jobs(
    db: Session = Depends(get_db)   
):
    jobs = db.query(models.Job).all()
    return jobs

@router.delete("/jobs/{job_id}", status_code=200)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db.delete(job)
    db.commit()
    
    return {"message": "Job deleted successfully"}