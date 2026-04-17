"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Patient, Appointment
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from sqlalchemy import select
from datetime import datetime

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/appointments', methods=['GET'])
def get_all_appointment():
    result_all_appointment = db.session.execute(
        select(Appointment)).scalars().all()
    return jsonify([appointment.serialize() for appointment in result_all_appointment]), 200


@api.route('/appointment/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    appointment = db.session.get(Appointment, appointment_id)
    if appointment is None:
        return jsonify({"msg": "Cita no encontrada"}), 404
    return jsonify(appointment.serialize()), 200


@api.route('/appointment', methods=['POST'])
def add_appointment():
    data = request.get_json()
    patient = Patient.query.filter_by(
        patient_name=data["patient_name"]
    ).first()

    if not patient:
        patient = Patient(patient_name=data["patient_name"])
        db.session.add(patient)
        db.session.commit()

    new_appointment = Appointment(
        patient_id=patient.patient_id,
        user_id=data["user_id"],
        date=datetime.fromisoformat(data["date"]),
        status=data["status"]
    )

    db.session.add(new_appointment)
    db.session.commit()

    return jsonify({
        "message": "Appointment created successfully",
        "appointment": new_appointment.serialize()
    }), 201


@api.route('/appointment/<int:appointment_id>', methods=['PUT'])
def update_appointment(appointment_id):
    datos = request.get_json()
    return jsonify({"mensaje": f"Usuario {appointment_id} actualizado", "datos": datos}), 200


@api.route('/appointment/<int:appointment_id>', methods=['DELETE'])
def delete_appointment(appointment_id):

    appointment_to_delete = db.session.execute(select(Appointment).where(
        appointment_id == appointment_id)).scalar_one_or_none()
    if appointment_to_delete is None:
        return jsonify({"msg": "la cita no existe"}), 404

    db.session.delete(appointment_to_delete)
    db.session.commit()
    return jsonify({"msg": "Eliminado con exito"}), 200
