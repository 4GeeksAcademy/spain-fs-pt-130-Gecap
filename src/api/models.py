from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey, Integer, Float, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "user"
    user_id: Mapped[int] = mapped_column(primary_key=True)
    user_name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), default=True)

class Doctor(db.Model):
    __tablename__ = "doctor"
    doctor_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
    doctor_name: Mapped[str] = mapped_column(String(100), nullable=False)
    especialidad: Mapped[str] = mapped_column(String(100), nullable=True)
    num_colegiado: Mapped[str] = mapped_column(String(50), nullable=True)
    appointments: Mapped[List["Appointment"]] = relationship(back_populates="doctor")

    def serialize(self):
        return {"id": self.doctor_id, "nombre": self.doctor_name, "especialidad": self.especialidad}

class Patient(db.Model):
    __tablename__ = "patient"
    patient_id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"), nullable=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    apellidos: Mapped[str] = mapped_column(String(100), nullable=False)
    dni: Mapped[str] = mapped_column(String(20), unique=True, nullable=True)
    email: Mapped[str] = mapped_column(String(120), nullable=True)
    telefono: Mapped[str] = mapped_column(String(20), nullable=True)
    appointments: Mapped[List["Appointment"]] = relationship(back_populates="patient")

    def serialize(self):
        return {"id": self.patient_id, "nombre": self.nombre, "apellidos": self.apellidos, "dni": self.dni or "Sin DNI"}

class Appointment(db.Model):
    __tablename__ = "appointment"
    appointment_id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(ForeignKey("patient.patient_id"), nullable=True)
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctor.doctor_id"), nullable=False)
    date: Mapped[str] = mapped_column(String(20), nullable=True)
    status: Mapped[str] = mapped_column(String(20), default="pendiente")
    doctor = relationship("Doctor", back_populates="appointments")
    patient = relationship("Patient", back_populates="appointments")

    def serialize(self):
        nombre_paciente = f"{self.patient.nombre} {self.patient.apellidos}" if self.patient else "Solicitud Web"
        return {"id": self.appointment_id, "patient_name": nombre_paciente, "status": self.status}
