from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime,date

class StudentSchema(BaseModel):
    registration_no: int
    name: str
    email_smit: EmailStr
    password: str
    
    branch: Optional[str] = None
    dob: Optional[date] = None
    category: Optional[str] = None
    gender: Optional[str] = None
    pan_number: Optional[str] = "NA"
    adhaar_number: Optional[str] = "NA"
    fathers_name: Optional[str] = None
    interested_in_placement: Optional[bool] = None
    placement_declaration: Optional[bool] = None
    reason_not_interested: Optional[str] = None
    class_10_percentage: Optional[float] = None
    class_10_year: Optional[int] = None
    class_10_school: Optional[str] = None
    class_10_board: Optional[str] = None
    class_12_percentage: Optional[float] = None
    class_12_year: Optional[int] = None
    class_12_school: Optional[str] = None
    class_12_board: Optional[str] = None
    polytechnic_percentage: Optional[float] = None
    polytechnic_year: Optional[int] = None
    polytechnic_institute: Optional[str] = None
    gpa_1st_sem: Optional[float] = None
    gpa_2nd_sem: Optional[float] = None
    gpa_3rd_sem: Optional[float] = None
    gpa_4th_sem: Optional[float] = None
    gpa_5th_sem: Optional[float] = None
    gpa_6th_sem: Optional[float] = None
    final_cgpa: Optional[float] = None
    current_cgpa: Optional[float] = None
    active_backlogs: Optional[int] = 0
    academic_gap: Optional[int] = 0
    mobile_no: Optional[str] = None
    whatsapp_no: Optional[str] = None
    home_contact_no: Optional[str] = None
    personal_email: Optional[EmailStr] = None
    permanent_address: Optional[str] = None
    home_town: Optional[str] = None
    home_state: Optional[str] = None
    home_state_pin: Optional[str] = None
    country: Optional[str] = None
    tg_name: Optional[str] = None
    tg_contact: Optional[str] = None
    tg_email: Optional[EmailStr] = None
    updated_cv: Optional[str] = None
    
    class Config:
        from_attributes = True

class StudentResponse(BaseModel):
    name: str
    email_smit: EmailStr  # Exclude password from response

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]

class StudentUpdate(BaseModel):
    branch: str | None = None
    dob: str | None = None
    category: str | None = None
    gender: str | None = None
    pan_number: str | None = None
    adhaar_number: str | None = None
    fathers_name: str | None = None
    interested_in_placement: bool | None = None
    placement_declaration: bool | None = None
    reason_not_interested: str | None = None
    class_10_percentage: float | None = None
    class_10_year: int | None = None
    class_10_school: str | None = None
    class_10_board: str | None = None
    class_12_percentage: float | None = None
    class_12_year: int | None = None
    class_12_school: str | None = None
    class_12_board: str | None = None
    polytechnic_percentage: float | None = None
    polytechnic_year: int | None = None
    polytechnic_institute: str | None = None
    gpa_1st_sem: float | None = None
    gpa_2nd_sem: float | None = None
    gpa_3rd_sem: float | None = None
    gpa_4th_sem: float | None = None
    gpa_5th_sem: float | None = None
    gpa_6th_sem: float | None = None
    final_cgpa: float | None = None
    current_cgpa: float | None = None
    active_backlogs: int | None = None
    academic_gap: int | None = None
    mobile_no: str | None = None
    whatsapp_no: str | None = None
    home_contact_no: str | None = None
    personal_email: str | None = None
    permanent_address: str | None = None
    home_town: str | None = None
    home_state: str | None = None
    home_state_pin: str | None = None
    country: str | None = None
    tg_name: str | None = None
    tg_contact: str | None = None
    tg_email: str | None = None
    updated_cv: str | None = None

class JobResponse(BaseModel):
    id: int
    title: str
    description: str
    registration_link: str
    posted_at: datetime

    class Config:
        from_attributes = True

class JobCreate(BaseModel):
    title: str
    description: str
    registration_link: str
    
class Admin(BaseModel):

    id: int
    name: str
    email: EmailStr
    password: str


class AdminCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

