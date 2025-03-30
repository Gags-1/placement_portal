from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # Fetch user based on registration_no instead of email
    user = db.query(models.Student).filter(models.Student.registration_no == user_credentials.username).first()
    
    # If user does not exist
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid registration number or password"
        )
    
    # Verify password
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid registration number or password"
        )

    # Create an access token
    access_token = oauth2.create_access_token(data={"registration_no": user.registration_no})


    return {"access_token": access_token, "token_type": "bearer"}
