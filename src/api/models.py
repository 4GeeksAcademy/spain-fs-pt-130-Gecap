from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)


    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Doctor(db.Model):
    __tablename__ = "doctor"
    doctor_id: Mapped[int] = mapped_column(primary_key=True)
    doctor_name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    appointment: Mapped[List["Appointment"]] = relationship(back_populates="doctor")

    def serialize(self):
        return {
            "id": self.doctor_id,
            "doctor_name": self.doctor_name,
            "email": self.email,
            "is_active": self.is_active,
        }


class Patient(db.Model):
    __tablename__ = "patient"
    patient_id: Mapped[int] = mapped_column(primary_key=True)
    patient_name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)
    appointment: Mapped[List["Appointment"]] = relationship(back_populates="patient")

    def serialize(self):
        return {
            "id": self.patient_id,
            "patient_name": self.patient_name,
            "email": self.email,
            "is_active": self.is_active,
        }


class Appointment(db.Model):
    __tablename__ = "appointment"
    appointment_id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patient.patient_id"))
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctor.doctor_id"))
    date: Mapped[datetime] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(String, nullable=False)
    doctor: Mapped["Doctor"] = relationship(back_populates="appointment")
    patient: Mapped["Patient"] = relationship(back_populates="appointment")

    def serialize(self):
        return {
            "id": self.appointment_id,
            "patient_id": self.patient_id,
            "doctor_id": self.doctor_id,
            "date": self.date,
            "status": self.status,
        }