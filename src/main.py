from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from pydantic import EmailStr
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from .database import get_db
from .models import Users, Profile
from passlib.context import CryptContext
import io, base64, re


app = FastAPI()


@app.post("/register")
async def create(
    full_name: str,
    email: EmailStr,
    password: str,
    phone: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed_password = pwd_context.hash(password)
    # check email exist
    is_email_exists = db.query(Users).filter_by(email=email).first()
    if is_email_exists:
        raise HTTPException(status_code=400, detail="Email already taken")
    # Check phone number exist
    is_phone_exists = db.query(Users).filter_by(phone=phone).first()
    if is_phone_exists:
        raise HTTPException(status_code=400, detail="Phone number already taken")
    # user object
    user_object = Users(
        full_name=full_name,
        email=email,
        password=hashed_password,
        phone=phone,
    )
    # saving user details
    db.add(user_object)
    db.commit()
    # reading file content
    file_content = await file.read()
    # inserting file and user id
    if file_content:
        profile_object = Profile(user_id=user_object.id, profile_picture=file_content)
        db.add(profile_object)
        db.commit()
    return {"success": True, "id": user_object.id}


@app.get("/get_user")
async def users(id: int, db: Session = Depends(get_db)):
    # finding an object with provinded id
    user_object = (
        db.query(Users, Profile)
        .join(Profile, Users.id == Profile.user_id)
        .filter(Users.id == id)
        .first()
    )

    user, profile = user_object

    if user_object:
        if profile:
            file_content = profile.profile_picture
            user_details = {
                "id": user.id,
                "name": user.full_name,
                "email": user.email,
                "phone": user.phone,
            }
            # Return file as json response by encoding file using base64
            file_stream = io.BytesIO(file_content)
            encoded_file_content = base64.b64encode(file_stream.getvalue()).decode()
            response_data = {
                "file_content": encoded_file_content,
                "data": user_details,
            }
            response = JSONResponse(content=response_data)
            return response
        return {user_object}
    return {"status": "no user found"}
