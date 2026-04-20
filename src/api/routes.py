from flask import Flask, request, jsonify, url_for, Blueprint, current_app
from api.models import db, User, Patient, Appointment
from api.utils import generate_sitemap, APIException
from flask_cors import CORS
from sqlalchemy import select
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

api = Blueprint('api', __name__)

CORS(api, resources={r"/*": {"origins": "*"}})

@api.route('/external-appointment', methods=['POST'])
def create_external_appointment():
    data = request.get_json()
    
    medico = User.query.filter_by(role="medico").first()

    if not medico:
        return jsonify({"msg": "Debe haber al menos un médico registrado en el sistema"}), 400

    try:
        new_app = Appointment(
            user_id=medico.id,  
            patient_id=None,
            date=data.get("date"),            
            start=data.get("start") or "00:00",
            end=data.get("end") or "00:00",
            reason=f"SOLICITUD WEB: {data.get('nombre')} - TEL: {data.get('telefono')} - MOTIVO: {data.get('motivo')}",
            status="pendiente"
        )
        db.session.add(new_app)
        db.session.commit()
        return jsonify({"msg": "Solicitud enviada"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error interno", "error": str(e)}), 500

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
    password = data.get("password")
    nombre = data.get("nombre")
    role = data.get("role")

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "El correo electrónico ya está registrado"}), 400

    pw_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    try:
        
        new_user = User(
            email=email, 
            password=pw_hash,
            user_name=nombre, 
            role=role, 
            is_active=True
        )
        db.session.add(new_user)
                
        if role != "medico":
            new_profile = Patient(
                nombre=data.get("nombre"),
                apellidos=data.get("apellidos"),
                user_id=new_user.id, 
                dni=data.get("dni")
            )
            db.session.add(new_profile)
            db.session.flush()
        
        db.session.commit()

        token = create_access_token(identity=str(new_user.id), additional_claims={"role": role})
        
        user_data = new_user.serialize() if role == "medico" else new_profile.serialize()

        return jsonify({
            "token": token,
            "role": role,
            "user": user_data
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error en el registro", "error": str(e)}), 500

@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get("email")).first()

    if user and bcrypt.check_password_hash(user.password, data.get("password")):
        
        if user.role == "medico":
            user_data = user.serialize()
        else:           
            perfil = Patient.query.filter_by(user_id=user.id).first()
            user_data = perfil.serialize() if perfil else {"nombre": "Paciente"}

        token = create_access_token(
            identity=str(user.id), 
            additional_claims={"role": user.role}
        )

        return jsonify({
            "token": token,
            "role": user.role,
            "user": user_data
        }), 200

    return jsonify({"msg": "Email o contraseña incorrectos"}), 401


@api.route('/perfil', methods=['GET'])
@jwt_required()
def get_user_profile():
    current_user_id = get_jwt_identity()

    user_base = db.session.get(User, current_user_id)
    if not user_base:
        return jsonify({"msg": "Usuario no encontrado"}), 404
   
    if user_base.role == "medico":
        perfil_data = user_base.serialize()
    else:
        perfil = Patient.query.filter_by(user_id=user_base.id).first()
        perfil_data = perfil.serialize() if perfil else None

    return jsonify({
        "id": user_base.id,
        "email": user_base.email,
        "role": user_base.role,
        "perfil": perfil_data
    }), 200

@api.route('/pacientes', methods=['GET'])
@jwt_required()
def get_pacientes():
    pacientes = Patient.query.all()
    return jsonify([p.serialize() for p in pacientes]), 200

@api.route('/pacientes', methods=['POST'])
@jwt_required()
def create_patient():
    data = request.get_json()

    existing_patient = Patient.query.filter_by(dni=data.get("dni")).first()
    if existing_patient:
        return jsonify({"msg": "El DNI introducido ya pertenece a un paciente registrado"}), 400

    def clean_num(val):
        if val is None or str(val).strip() in ["", "--"]:
            return None
        try:
            return float(val)
        except (ValueError, TypeError):
            return None

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
            tension=data.get("tension") or "",
            grupo_sanguineo=data.get("grupoSanguineo") or "",
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
    for key, value in data.items():
        if hasattr(paciente, key):
            setattr(paciente, key, value)

    db.session.commit()
    return jsonify({"msg": "Paciente actualizado"}), 200

@api.route('/pacientes/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_patient(id):
    paciente = db.session.get(Patient, id)
    if not paciente:
        return jsonify({"msg": "Paciente no encontrado"}), 404

    try:
        db.session.delete(paciente)
        db.session.commit()
        return jsonify({"msg": "Paciente eliminado correctamente"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": "Error al eliminar", "error": str(e)}), 500

@api.route('/appointments', methods=['GET'])
@jwt_required()
def get_all_appointments():
    appointments = Appointment.query.all()
    return jsonify([a.serialize() for a in appointments]), 200

@api.route('/appointment/<int:appointment_id>', methods=['GET'])
@jwt_required()
def get_appointment(appointment_id):
    appointment = db.session.get(Appointment, appointment_id)
    if not appointment:
        return jsonify({"msg": "Cita no encontrada"}), 404
    return jsonify(appointment.serialize()), 200

@api.route('/appointments', methods=['POST'])
@jwt_required()
def add_appointment():
    data = request.get_json()
   
    patient = db.session.get(Patient, data.get("patient_id"))
    if not patient:
        return jsonify({"msg": "Paciente no encontrado"}), 404
    
    user_id = get_jwt_identity()

    try:       
        new_appointment = Appointment(
            patient_id=patient.patient_id,
            user_id=user_id, 
            date=data.get("date"),
            start=data.get("start") or "00:00", 
            end=data.get("end") or "00:00",     
            status="pendiente",
            reason=data.get("reason")
        )
        db.session.add(new_appointment)
        db.session.commit()
        return jsonify({
            "msg": "Cita creada con éxito", 
            "appointment": new_appointment.serialize()
        }), 201
    except Exception as e:
        db.session.rollback()
        print(f"🛑 ERROR AL CREAR CITA: {str(e)}")
        return jsonify({"msg": "Error al crear cita", "error": str(e)}), 500


@api.route('/appointment/<int:appointment_id>', methods=['PUT'])
@jwt_required()
def update_appointment(appointment_id):
    data = request.get_json()
    appointment = db.session.get(Appointment, appointment_id)

    if not appointment:
        return jsonify({"msg": "Cita no encontrada"}), 404

    if "date" in data:
        appointment.date = data["date"]
    if "time" in data:
        appointment.time = data["time"]
    if "status" in data:
        appointment.status = data["status"]
    if "reason" in data:
        appointment.reason = data["reason"]

    db.session.commit()
    return jsonify({"msg": "Cita actualizada", "appointment": appointment.serialize()}), 200

@api.route('/appointment/<int:appointment_id>', methods=['DELETE'])
@jwt_required()
def delete_appointment(appointment_id):
    appointment = db.session.get(Appointment, appointment_id)
    if not appointment:
        return jsonify({"msg": "La cita no existe"}), 404

    try:
        db.session.delete(appointment)
        db.session.commit()
        return jsonify({"msg": "Cita eliminada con éxito"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
