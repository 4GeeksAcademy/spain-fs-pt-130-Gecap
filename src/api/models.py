from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)

    appointments: Mapped[List["Appointment"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.user_id,
            "user_name": self.user_name,
            "email": self.email,
            "is_active": self.is_active
        }


class Patient(db.Model):
    __tablename__ = "patient"

    patient_id: Mapped[int] = mapped_column(primary_key=True)
    patient_name: Mapped[str] = mapped_column(String(30), nullable=False)

    appointments: Mapped[List["Appointment"]] = relationship(back_populates="patient")

    def serialize(self):
        return {
            "id": self.patient_id,
            "patient_name": self.patient_name
        }


class Appointment(db.Model):
    __tablename__ = "appointment"

    appointment_id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patient.patient_id"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"), nullable=False)

    date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)

    user: Mapped["User"] = relationship(back_populates="appointments")
    patient: Mapped["Patient"] = relationship(back_populates="appointments")

    def serialize(self):
        return {
            "id": self.appointment_id,
            "patient_id": self.patient_id,
            "patient_name": self.patient.patient_name,  
            "user_id": self.user_id,
            "date": self.date.isoformat(),
            "status": self.status
        }