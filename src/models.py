from sqlalchemy import Integer, String, LargeBinary, ForeignKey
from sqlalchemy.sql.schema import Column, CheckConstraint
from .database import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(Integer, nullable=False)

    __table_args__ = (
        CheckConstraint(
            "LENGTH(CAST(phone_number AS VARCHAR)) = 10",
            name="phone_number_length_check",
        ),
    )


class Profile(Base):
    __tablename__ = "profile"

    id = Column(Integer, primary_key=True, index=True)
    profile_picture = Column(LargeBinary, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
