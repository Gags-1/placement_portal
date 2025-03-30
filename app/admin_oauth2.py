from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import schemas, database, models
from .config import settings

# Define OAuth2 scheme for admin login
oauth2_scheme_admin = OAuth2PasswordBearer(tokenUrl="admin/login")

# Load security settings from config
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    """
    Generates a JWT access token with expiration time.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # Removed role
    
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_access_token(token: str, credentials_exception):
    """
    Verifies the JWT access token and extracts email.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("email")  # Fetching only email

        if email is None:
            raise credentials_exception
        
        return schemas.TokenData(id=email)  # Keeping it consistent with Student authentication
    
    except JWTError:
        raise credentials_exception

def get_current_admin(
    token: str = Depends(oauth2_scheme_admin),
    db: Session = Depends(database.get_db)
):
    """
    Retrieves the current authenticated admin from the database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"}
    )

    token_data = verify_access_token(token, credentials_exception)

    admin = db.query(models.Admin).filter(models.Admin.email == token_data.id).first()

    if admin is None:
        raise credentials_exception

    return admin
