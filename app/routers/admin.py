from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.utils import hash_password 
from app.admin_oauth2 import get_current_admin 
from app.mail import send_email

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.post("/create-admin")
def create_admin(admin_data: schemas.AdminCreate, db: Session = Depends(get_db)):
    existing_admin = db.query(models.Admin).filter(models.Admin.email == admin_data.email).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="Admin with this email already exists")

    hashed_password = hash_password(admin_data.password)

    new_admin = models.Admin(
        name=admin_data.name,
        email=admin_data.email,
        password=hashed_password
    )

    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)

    return {"message": "✅ Admin created successfully!", "admin_id": new_admin.id}


def send_job_notifications(email_list, job_data):
    subject = f"New Job Posted: {job_data.title}"
    message = f"""
    Hello,

    A new job opportunity has been posted.

    📌 Job Title: {job_data.title}
    📝 Description: {job_data.description}
    🔗 Apply Here: {job_data.registration_link}

    Best Regards,
    Placement Portal Team
    """

    for email in email_list:
        send_email(email, subject, message)


@router.post("/create-job")
def create_job(
    job_data: schemas.JobCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db),
    current_admin: models.Admin = Depends(get_current_admin)
):
    new_job = models.Job(
        title=job_data.title,
        description=job_data.description,
        registration_link=job_data.registration_link
    )
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    student_emails = db.query(models.Student.email_smit).distinct().all()
    email_list = [email[0] for email in student_emails]

    background_tasks.add_task(send_job_notifications, email_list, job_data)

    return {"message": "✅ Job created! Emails are being sent in the background.", "job_id": new_job.id}


@router.get("/jobs", response_model=list[schemas.JobResponse])
def get_jobs(db: Session = Depends(get_db)):
    jobs = db.query(models.Job).all()
    return jobs

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    total_jobs = db.query(models.Job).count()
    total_students = db.query(models.Student).count()
    return {"total_jobs": total_jobs, "total_students": total_students}

@router.delete("/jobs/{job_id}", status_code=200)
def delete_job(job_id: int, db: Session = Depends(get_db)):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    db.delete(job)
    db.commit()
    
    return {"message": "Job deleted successfully"}
