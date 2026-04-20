from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User, Doctor, Patient, Appointment
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from sqlalchemy import select
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt
from flask import current_app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt() 

api = Blueprint('api', __name__)

CORS(api, resources={r"/*": {"origins": "*"}})

@api.route('/appointments', methods=['POST'])
@jwt_required()
def create_appointment():
    data = request.get_json()
    user_id = get_jwt_identity()

    doctor = Doctor.query.filter_by(user_id=user_id).first()

    if not doctor:
        return jsonify({"msg": "Perfil de médico no encontrado"}), 404

    try:
        new_app = Appointment(
            patient_id=data.get("patient_id"),
            doctor_id=doctor.doctor_id,
            date=data.get("date"),
            time=data.get("time"),
            reason=data.get("reason"),
            status="pendiente"
        )
        db.session.add(new_app)
        db.session.commit()
        return jsonify({"msg": "Cita agendada correctamente", "appointment": new_app.serialize()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error al crear la cita", "error": str(e)}), 500

@api.route('/appointments', methods=['GET'])
@jwt_required()
def get_my_appointments():
    user_id = get_jwt_identity()
    doctor = Doctor.query.filter_by(user_id=user_id).first()

    if not doctor:
        return jsonify({"msg": "Médico no encontrado"}), 404

    appointments = Appointment.query.filter_by(
        doctor_id=doctor.doctor_id).all()
    return jsonify([a.serialize() for a in appointments]), 200

@api.route('/external-appointment', methods=['POST'])
def create_external_appointment():
    data = request.get_json()

    doctor = Doctor.query.first()
    if not doctor:
        return jsonify({"msg": "Debe haber al menos un médico registrado en el sistema"}), 400

    try:
        new_app = Appointment(
            doctor_id=doctor.doctor_id,
            patient_id=None,
            date=None,
            time=None,
            reason=f"NUEVA SOLICITUD WEB: {data.get('nombre')} - TEL: {data.get('telefono')} - MOTIVO: {data.get('motivo')}",
            status="pendiente"
        )
        db.session.add(new_app)
        db.session.commit()
        return jsonify({"msg": "Solicitud enviada"}), 201
    except Exception as e:
        db.session.rollback()
        print(f"Error en DB: {str(e)}")
        return jsonify({"msg": "Error interno del servidor", "error": str(e)}), 500

@api.route('/public-appointments/<string:dni>', methods=['GET'])
def get_public_appointments(dni):
    patient = Patient.query.filter(Patient.dni.ilike(dni)).first()

    if not patient:
        return jsonify({"msg": "No se encontró el paciente"}), 404

    appointments = Appointment.query.filter_by(
        patient_id=patient.patient_id).all()

    return jsonify({
        "paciente": patient.nombre,
        "citas": [a.serialize() for a in appointments if a.status != "cancelada"]
    }), 200

@api.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    email = data.get("email")    
    pw_hash = bcrypt.generate_password_hash(data.get("password")).decode('utf-8')
    
    try:       
        new_user = User(email=email, password=pw_hash, role=data.get("role"), is_active=True)
        db.session.add(new_user)
        db.session.flush()

        if data.get("role") == "medico":
            new_profile = Doctor(
                doctor_name=f"{data.get('nombre')} {data.get('apellidos')}", 
                user_id=new_user.id,
                
            )
        else:
            new_profile = Patient(
                nombre=data.get("nombre"), 
                apellidos=data.get("apellidos"), 
                user_id=new_user.id, 
                dni=data.get("dni")
            )

        db.session.add(new_profile)
        db.session.commit()
        
        token = create_access_token(identity=str(new_user.id), additional_claims={"role": data.get("role")})
        return jsonify({
            "token": token, 
            "role": data.get("role"), 
            "user": new_profile.serialize()
        }), 201
    except Exception as e:
        db.session.rollback()
        print(f"🛑 ERROR: {str(e)}")
        return jsonify({"error": str(e)}), 500

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get("email")).first()
        
    if user and bcrypt.check_password_hash(user.password, data.get("password")):
       
        if user.role == "medico":
            perfil = Doctor.query.filter_by(user_id=user.id).first()
        else:
            perfil = Patient.query.filter_by(user_id=user.id).first()
               
        token = create_access_token(identity=str(user.id), additional_claims={"role": user.role})
        
        return jsonify({
            "token": token, 
            "role": user.role, 
            "user": perfil.serialize() if perfil else {"nombre": "Usuario"}
        }), 200
    
    return jsonify({"msg": "Email o contraseña incorrectos"}), 401

@api.route('/perfil', methods=['GET'])
@jwt_required()
def get_user_profile():
    current_user_id = get_jwt_identity() 
    
    user_base = User.query.get(current_user_id)
    if not user_base:
        return jsonify({"msg": "Usuario no encontrado"}), 404

    if user_base.role == "medico":
        perfil = Doctor.query.filter_by(user_id=user_base.id).first()
    else:
        perfil = Patient.query.filter_by(user_id=user_base.id).first()

    return jsonify({
        "id": user_base.id,
        "email": user_base.email,
        "role": user_base.role,
        "perfil": perfil.serialize() if perfil else None
    }), 200

@api.route('/pacientes', methods=['GET'])
@jwt_required()
def get_pacientes():
    pacientes = Patient.query.all()
    return jsonify([p.serialize() for p in pacientes]), 200

def clean_num(val):
    if val is None or str(val).strip() in ["", "--"]:
        return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None

@api.route('/pacientes', methods=['POST'])
@jwt_required()
def create_patient():
    data = request.get_json()    
    if Patient.query.filter_by(dni=data.get("dni")).first():
        return jsonify({"msg": "El DNI ya pertenece a un paciente registrado"}), 400

    try:
        nuevo_p = Patient(
            nombre=data.get("nombre"),
            apellidos=data.get("apellidos"),
            dni=data.get("dni"),
            email=data.get("email"),
            telefono=data.get("telefono"),
            nacimiento=data.get("nacimiento") or None,
            peso=clean_num(data.get("peso")),
            altura=clean_num(data.get("altura")),
            glucosa=clean_num(data.get("glucosa")),
            spo2=clean_num(data.get("spo2")),
            tension=data.get("tension", ""),
            grupo_sanguineo=data.get("grupoSanguineo", ""),
            # Usamos .get con valor por defecto "NO"
            embarazo=data.get("embarazo", "NO"),
            hepatitis=data.get("hepatitis", "NO"),
            tuberculosis=data.get("tuberculosis", "NO"),
            vih=data.get("vih", "NO"),
            radiacion_cabeza=data.get("radiacion_cabeza", "NO"),
            cancer=data.get("cancer", "NO"),
            alergia_penicilina=data.get("alergia_penicilina", "NO"),
            alergia_terramicina=data.get("alergia_terramicina", "NO"),
            alergia_anestesia=data.get("alergia_anestesia", "NO"),
            alergia_latex=data.get("alergia_latex", "NO"),
            alergia_aines=data.get("alergia_aines", "NO"),
            alergia_otros=data.get("alergia_otros", ""),
            anotaciones=data.get("anotaciones", "")
        )
        db.session.add(nuevo_p)
        db.session.commit()
        return jsonify({"msg": "Paciente creado", "id": nuevo_p.patient_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error al crear", "error": str(e)}), 500

@api.route('/pacientes/<int:id>', methods=['PUT'])
@jwt_required()
def update_patient(id):   
    paciente = db.session.get(Patient, id)
    if not paciente:
        return jsonify({"msg": "No encontrado"}), 404

    data = request.get_json()
        
    numeric_fields = ["peso", "altura", "glucosa", "spo2"]

    for key, value in data.items():
        if hasattr(paciente, key):
            if key in numeric_fields:
                setattr(paciente, key, clean_num(value))
            else:
                setattr(paciente, key, value)

    db.session.commit()
    return jsonify({"msg": "Paciente actualizado"}), 200