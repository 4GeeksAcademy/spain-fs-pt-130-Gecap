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
    apellidos: Mapped[str] = mapped_column(String(100), nullable=True)
    dni: Mapped[str] = mapped_column(String(20), unique=True, nullable=True)
    email: Mapped[str] = mapped_column(String(120), nullable=True)
    telefono: Mapped[str] = mapped_column(String(20), nullable=True)
    nacimiento: Mapped[str] = mapped_column(String(20), nullable=True)
    appointments: Mapped[List["Appointment"]] = relationship(back_populates="patient")

    # Biometría y Constantes
    peso: Mapped[float] = mapped_column(Float, nullable=True)
    altura: Mapped[float] = mapped_column(Float, nullable=True)
    glucosa: Mapped[int] = mapped_column(Integer, nullable=True)
    tension: Mapped[str] = mapped_column(String(20), nullable=True)
    spo2: Mapped[int] = mapped_column(Integer, nullable=True)
    grupo_sanguineo: Mapped[str] = mapped_column(String(10), nullable=True)

    # Riesgos y Bioseguridad (Guardamos "SI" o "NO")
    embarazo: Mapped[str] = mapped_column(String(5), default="NO", nullable=True)
    hepatitis: Mapped[str] = mapped_column(String(5), default="NO", nullable=True)
    tuberculosis: Mapped[str] = mapped_column(String(5), default="NO", nullable=True)
    vih: Mapped[str] = mapped_column(String(5), default="NO", nullable=True)
    radiacion_cabeza: Mapped[str] = mapped_column(String(5), default="NO", nullable=True)
    cancer: Mapped[str] = mapped_column(String(5), default="NO", nullable=True)

    # Alergias
    alergia_penicilina: Mapped[str] = mapped_column(String(5), default="NO", nullable=True)
    alergia_terramicina: Mapped[str] = mapped_column(String(5), default="NO", nullable=True)
    alergia_anestesia: Mapped[str] = mapped_column(String(5), default="NO", nullable=True)
    alergia_latex: Mapped[str] = mapped_column(String(5), default="NO", nullable=True)
    alergia_aines: Mapped[str] = mapped_column(String(5), default="NO", nullable=True)
    alergia_otros: Mapped[str] = mapped_column(Text, nullable=True)

    anotaciones: Mapped[str] = mapped_column(Text, nullable=True)

   

    def serialize(self):
        return {"id": self.patient_id, "nombre": self.nombre, "apellidos": self.apellidos, "dni": self.dni or "Sin DNI"}

class Appointment(db.Model):
    __tablename__ = "appointment"
    appointment_id: Mapped[int] = mapped_column(primary_key=True)
    patient_id: Mapped[int] = mapped_column(
        ForeignKey("patient.patient_id"), nullable=False)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.user_id"), nullable=False)
    date: Mapped[str] = mapped_column(String(50), nullable=False)
    start: Mapped[str] = mapped_column(String(50), nullable=False)
    end: Mapped[str] = mapped_column(String(50), nullable=False)
    reason: Mapped[str] = mapped_column(String(200), nullable=True)
    status: Mapped[str] = mapped_column(String(50), default="pendiente")
    user: Mapped["User"] = relationship(back_populates="appointments")
    patient: Mapped["Patient"] = relationship(back_populates="appointments")

    def serialize(self):
        return {
            "id": self.appointment_id,
            "patient_id": self.patient_id,
            "patient_name": f"{self.patient.nombre} {self.patient.apellidos}" if self.patient else "Desconocido",
            "user_id": self.user_id,
            "date": self.date,
            "start": self.start,
            "end": self.end,
            "status": self.status,
            "reason": self.reason
        }
