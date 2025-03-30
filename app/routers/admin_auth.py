from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, admin_oauth2

router = APIRouter(prefix= '/admin',tags=['Admin Authentication'])

@router.post('/login', response_model=schemas.Token)
def admin_login(admin_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    # Fetch admin by email
    admin = db.query(models.Admin).filter(models.Admin.email == admin_credentials.username).first()
    
    if not admin or not utils.verify(admin_credentials.password, admin.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid email or password"
        )

    # Create access token
    access_token = admin_oauth2.create_access_token(data={"email": admin.email})

    return {"access_token": access_token, "token_type": "bearer"}
