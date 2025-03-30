import csv
from io import StringIO
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from app.database import get_db
from app import models, schemas, utils

router = APIRouter(prefix="/students", tags=["Students"])

@router.post("/", response_model=schemas.StudentResponse)
def create_student(student: schemas.StudentSchema, db: Session = Depends(get_db)):
    # Ensure the email_smit domain is "smit.smu.edu.in"
    if not student.email_smit.endswith("@smit.smu.edu.in"):
        raise HTTPException(status_code=400, detail="Email must be from the domain smit.smu.edu.in")

    # Check if student already exists by email or registration number
    existing_student = db.query(models.Student).filter(
        (models.Student.email_smit == student.email_smit) |
        (models.Student.registration_no == student.registration_no)
    ).first()

    if existing_student:
        raise HTTPException(status_code=400, detail="Student with this email or registration number already exists")

    # Hash the password before storing it
    hashed_password = utils.hash_password(student.password)

    # Create a new student with only required fields
    new_student = models.Student(
        registration_no=student.registration_no,
        name=student.name,
        email_smit=student.email_smit,
        password=hashed_password
    )

    db.add(new_student)
    db.commit()
    db.refresh(new_student)

    return new_student


@router.get("/{reg_number}")
async def get_student(reg_number: str, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.registration_no == reg_number).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")

    return student  # Returns all fields automatically


@router.put("/{reg_number}")
async def update_student(reg_number: str, student_data: schemas.StudentUpdate, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(models.Student.registration_no == reg_number).first()
    
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    
    for field, value in student_data.dict(exclude_unset=True).items():
        setattr(student, field, value)
    
    db.commit()
    db.refresh(student)

    return {"message": "Student details updated successfully"}


@router.get("/")
async def get_all_students(db: Session = Depends(get_db)):
    students = db.query(models.Student).all()

    if not students:
        raise HTTPException(status_code=404, detail="No students found")

    students_data = []
    for student in students:
        student_dict = {
            "registration_no": student.registration_no,
            "name": student.name,
            "branch": student.branch,
            "dob": student.dob,
            "category": student.category,
            "gender": student.gender,
            "pan_number": student.pan_number,
            "adhaar_number": student.adhaar_number,
            "fathers_name": student.fathers_name,
            "interested_in_placement": student.interested_in_placement,
            "placement_declaration": student.placement_declaration,
            "reason_not_interested": student.reason_not_interested,
            "class_10_percentage": student.class_10_percentage,
            "class_10_year": student.class_10_year,
            "class_10_school": student.class_10_school,
            "class_10_board": student.class_10_board,
            "class_12_percentage": student.class_12_percentage,
            "class_12_year": student.class_12_year,
            "class_12_school": student.class_12_school,
            "class_12_board": student.class_12_board,
            "polytechnic_percentage": student.polytechnic_percentage,
            "polytechnic_year": student.polytechnic_year,
            "polytechnic_institute": student.polytechnic_institute,
            "gpa_1st_sem": student.gpa_1st_sem,
            "gpa_2nd_sem": student.gpa_2nd_sem,
            "gpa_3rd_sem": student.gpa_3rd_sem,
            "gpa_4th_sem": student.gpa_4th_sem,
            "gpa_5th_sem": student.gpa_5th_sem,
            "gpa_6th_sem": student.gpa_6th_sem,
            "final_cgpa": student.final_cgpa,
            "current_cgpa": student.current_cgpa,
            "active_backlogs": student.active_backlogs,
            "academic_gap": student.academic_gap,
            "mobile_no": student.mobile_no,
            "whatsapp_no": student.whatsapp_no,
            "home_contact_no": student.home_contact_no,
            "email_smit": student.email_smit,
            "personal_email": student.personal_email,
            "permanent_address": student.permanent_address,
            "home_town": student.home_town,
            "home_state": student.home_state,
            "home_state_pin": student.home_state_pin,
            "country": student.country,
            "tg_name": student.tg_name,
            "tg_contact": student.tg_contact,
            "tg_email": student.tg_email,
        }
        students_data.append(student_dict)

    return students_data

