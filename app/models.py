
from sqlalchemy import TIMESTAMP, Column, Integer, String, Float, Boolean, Date, LargeBinary, text
from .database import Base

class Student(Base):
    __tablename__ = "students"

    # Primary Key
    registration_no = Column(Integer, primary_key=True, unique=True, index=True)

    password = Column(String, nullable=False)
    
    # Basic Details
    name = Column(String, nullable=False)
    branch = Column(String, nullable=True)
    dob = Column(Date, nullable=True)
    category = Column(String, nullable=True)  # (Gen / SC / ST / OBC)
    gender = Column(String, nullable=True)  # (Male / Female)
    pan_number = Column(String, nullable=True, default="NA")
    adhaar_number = Column(String, nullable=True, default="NA")
    fathers_name = Column(String, nullable=True)

    # Placement Interest
    interested_in_placement = Column(Boolean, nullable=True)
    placement_declaration = Column(Boolean, nullable=True)  # If interested, student agrees to declaration
    reason_not_interested = Column(String, nullable=True)  # If not interested

    # Academic Details
    class_10_percentage = Column(Float, nullable=True)
    class_10_year = Column(Integer, nullable=True)
    class_10_school = Column(String, nullable=True)
    class_10_board = Column(String, nullable=True)
    
    class_12_percentage = Column(Float, nullable=True)
    class_12_year = Column(Integer, nullable=True)
    class_12_school = Column(String, nullable=True)
    class_12_board = Column(String, nullable=True)

    polytechnic_percentage = Column(Float, nullable=True)
    polytechnic_year = Column(Integer, nullable=True)
    polytechnic_institute = Column(String, nullable=True)

    # College Academic Performance
    gpa_1st_sem = Column(Float, nullable=True)
    gpa_2nd_sem = Column(Float, nullable=True)
    gpa_3rd_sem = Column(Float, nullable=True)
    gpa_4th_sem = Column(Float, nullable=True)
    gpa_5th_sem = Column(Float, nullable=True)
    gpa_6th_sem = Column(Float, nullable=True)
    final_cgpa = Column(Float, nullable=True)
    current_cgpa = Column(Float, nullable=True)
    active_backlogs = Column(Integer, nullable=True, default=0)
    academic_gap = Column(Integer, nullable=True, default=0)

    # Contact Information
    mobile_no = Column(String, nullable=True)
    whatsapp_no = Column(String, nullable=True)
    home_contact_no = Column(String, nullable=True)
    email_smit = Column(String, unique=True, nullable=False )
    personal_email = Column(String, unique=True, nullable=True)

    permanent_address = Column(String, nullable=True)
    home_town = Column(String, nullable=True)
    home_state = Column(String, nullable=True)
    home_state_pin = Column(String, nullable=True)
    country = Column(String, nullable=True)

    # TG Details
    tg_name = Column(String, nullable=True)
    tg_contact = Column(String, nullable=True)
    tg_email = Column(String, nullable=True)

    # Uploaded CV
    updated_cv = Column(String, nullable=True)  # Store file path


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    registration_link=Column(String, nullable=False)
    posted_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))   


class Admin(Base):
    __tablename__="admin"

    id=Column(Integer, primary_key=True, nullable=False)
    name= Column(String, nullable=False)
    email=Column(String, nullable=False)
    password = Column(String, nullable=False)