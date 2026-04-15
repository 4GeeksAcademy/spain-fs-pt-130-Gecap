"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, Doctor, Patient, Appointment
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from sqlalchemy import select

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)



# @api.route('/hello', methods=['POST', 'GET'])
# def handle_hello():

#     response_body = {
#         "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
#     }

#     return jsonify(response_body), 200


@api.route('/appointments', methods=['GET'])
def get_all_appointment():
    result_all_appointment=db.session.execute(select(Appointment)).scalars().all()
    return jsonify([appointment.serialize() for appointment in result_all_appointment]), 200

@api.route('/appointment/<int:appointment_id>', methods=['GET'])
def get_appointment(appointment_id):
    appointment= db.session.get(Appointment, appointment_id)
    if appointment is None:
        return jsonify({"msg": "Cita no encontrada"}),404
    return jsonify(appointment.serialize()),200



