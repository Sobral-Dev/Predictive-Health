from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import timedelta
from flask_mail import Mail, Message
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from pymongo import MongoClient
import uuid
import logging
import joblib
from auth import validate_login, role_required, add_audit_log, revoke_token
from config import db
from datetime import datetime
from helpers.calculate_age_helper import calculate_age

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgre:853211@localhost:5432/PatientSystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

# Configuração de email usando Mailtrap
app.config['MAIL_SERVER']= 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'd572e6ff412340'
app.config['MAIL_PASSWORD'] = '73e2c3d1fc80cf'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'predictive-health@noreply.com'

# Inicializando o CORS
CORS(app)

# Conectando ao banco Postgre
db.init_app(app)
migrate = Migrate(app, db)

# Configurando MongoDB
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["PredictiveHealth"]
prediction_collection = mongo_db["PredictionData"]

# Criando índices no MongoDB
def configure_mongo_indexes():
    try:
        prediction_collection.create_index("user_id")
        prediction_collection.create_index("paciente_id")
    except Exception as e:
        print(f"Erro ao configurar índices no MongoDB: {e}")

# Configurando ferramentas de criptografia no app
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Configuração de email
mail = Mail(app)

# Configurando o Logging
logging.basicConfig(filename='app.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

# Carregamento dos modelos de IA na inicialização
diabetes_model = None
hypertension_model = None
stroke_model = None

first_request_executed = False

@app.before_request
def load_models():
    global first_request_executed
    global diabetes_model, hypertension_model, stroke_model
    if not first_request_executed:
        try:
            diabetes_model = joblib.load(r'C:\Users\felip\OneDrive\Documentos\FATEC\Predictive-Health\models\diabetes_model.pkl')
        except Exception as e:
            print(f"Erro ao carregar o modelo de Diabetes: {e}")
        try:
            hypertension_model = joblib.load(r'C:\Users\felip\OneDrive\Documentos\FATEC\Predictive-Health\models\hypertension_model.pkl')
        except Exception as e:
            print(f"Erro ao carregar o modelo de Hipertensão: {e}")
        try:
            stroke_model = joblib.load(r'C:\Users\felip\OneDrive\Documentos\FATEC\Predictive-Health\models\stroke_model.pkl')
        except Exception as e:
            print(f"Erro ao carregar o modelo de AVC: {e}")
        first_request_executed = True
        app.logger.info("All predictive models loaded successfully")

# Callback para verificar se o token está na lista de tokens revogados
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    from models import RevokedToken
    jti = jwt_payload['jti']
    token = RevokedToken.query.filter_by(jti=jti).first()
    return token is not None

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Error: {str(e)}", exc_info=True)
    return jsonify({"error": "An internal error occurred"}), 500

# Rota Raíz
@app.route('/')
def home():
    return "Welcome to the Health Predictive System!"

# Endpoint 1: Registro de Usuário
@app.route('/register_user', methods=['POST'])
def register_user():

    from models import User, Patient

    data = request.get_json()

    new_user = User(
        name=data['name'],
        email=data['email'],
        password=bcrypt.generate_password_hash(data['password']),
        role=data['role'],
        cpf=data['cpf']
    )

    # Verifica se há um paciente com o mesmo CPF
    existing_patient = Patient.query.filter_by(cpf=data['cpf']).first()
    if existing_patient:
        new_user.has_patient_history = True

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User registered successfully"}), 201
    
    except IntegrityError as e:
        db.session.rollback()
        if 'duplicate key value violates unique constraint' in str(e.orig):
            return jsonify({"error": "CPF already registered"}), 409
        
        return jsonify({"error": "Database error"}), 500


# Endpoint 2: Solicitar Consentimento Inicial
@app.route('/consent-initial', methods=['POST'])
@jwt_required()
def consent_initial():
    from models import User, Patient
    from schemas import ConsentSchema

    user_id = get_jwt_identity()
    data = request.get_json()
    consent_schema = ConsentSchema()
    errors = consent_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        user.consent_status = data['consent_status']
        db.session.commit()
        add_audit_log("Consent User updated", user_id)

        try:
            patient = Patient.query.filter_by(cpf=user.cpf).first()
            if not patient:
                pass
            patient.consent_status = data['consent_status']
            db.session.commit()
            add_audit_log("Consent Patient updated", user_id)
        except:
            pass
    
    except Exception as e: 
        return jsonify({"message": f"Error when trying to update consent status: {e}"}), 400

    return jsonify({"message": "Consent updated successfully"}), 200

# Endpoint 3: Login de Usuário
@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()
    user = validate_login(data['email'], data['password'])
    if not user:
        return jsonify({"error": "Invalid email or password"}), 401

    access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
    add_audit_log("User logged in", user.id)

    return jsonify({
        "access_token": access_token,
        "user_name": user.name,
        "user_id": user.id,
        "user_role": user.role,
        "consent_status": user.consent_status,
        "has_patient_history": user.has_patient_history
    }), 200

# Endpoint 4: Logout de Usuário
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    revoke_token(jti)
    user_id = get_jwt_identity()
    add_audit_log("User logged out", user_id)

    return jsonify({"message": "Logged out successfully"}), 200

# Endpoint 5: Visualizar Dados Pessoais
@app.route('/user/me', methods=['GET'])
@jwt_required()
def get_user_data():
    from models import User

    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    user_data = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "consent_status": user.consent_status,
        "has_patient_history": user.has_patient_history,
        "created_at": user.created_at
    }
    return jsonify(user_data), 200

# Endpoint 6: Atualizar Dados Pessoais
@app.route('/user/me', methods=['PUT'])
@jwt_required()
def update_user_data():
    from models import User
    user_id = get_jwt_identity()
    data = request.get_json()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    if "name" in data:
        user.name = data['name']
    if "email" in data:
        user.email = data['email']

    try:
        db.session.commit()
        add_audit_log("User data updated", user_id)

    except IntegrityError as e:
        db.session.rollback() 

        if 'duplicate key value violates unique constraint' in str(e.orig):
            return jsonify({"error": "Email already registered"}), 409
        
        return jsonify({"error": "Database integrity error"}), 500
    
    return jsonify({"message": "User data updated successfully"}), 200

# Endpoint 7: Exportar Dados Pessoais
@app.route('/user/export', methods=['GET'])
@jwt_required()
def export_user_data():
    from models import User

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    export_data = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "consent_status": user.consent_status,
        "created_at": user.created_at
    }
    
    return jsonify(export_data), 200

# Endpoint 8: Solicitar Redefinição de Senha
@app.route('/password-reset-request', methods=['POST'])
def password_reset_request():
    from models import User

    data = request.get_json()
    email = data.get("email")
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({"error": "Email not found"}), 404

    reset_token = str(uuid.uuid4())
    user.reset_token = reset_token
    db.session.commit()

    # Enviar email com o link de redefinição usando Mailtrap
    msg = Message("Password Reset Request", recipients=[user.email])
    msg.body = f"To reset your password, use the following token: {reset_token}"
    mail.send(msg)

    return jsonify({"message": "Password reset email sent"}), 200

# Endpoint 9: Redefinir Senha
@app.route('/password-reset', methods=['POST'])
def password_reset():
    from models import User

    data = request.get_json()

    reset_token = data.get("reset_token")
    new_password = data.get("new_password")

    user_id = data.get("user_id")

    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"error": "Invalid token or email"}), 400
    
    email = user.email

    user = User.query.filter_by(email=email, reset_token=reset_token).first()
    if not user:
        return jsonify({"error": "Invalid token or email"}), 400

    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    user.password = hashed_password
    user.reset_token = None  
    db.session.commit()

    return jsonify({"message": "Password updated successfully"}), 200

# Endpoint 10: Registro de Paciente
@app.route('/register_patient', methods=['POST'])
@jwt_required()
@role_required(['admin', 'medico'])
def register_patient():

    from models import User, Patient

    data = request.get_json()
    new_patient = Patient(
        name=data['name'],
        age=data['age'],
        medical_conditions=data['medical_conditions'],
        consent_status=data['consent_status'],
        cpf=data['cpf'],
        brith_date=data['birth_date']
    )

    # Verifica se há um usuário com o mesmo CPF e define `has_patient_history`
    existing_user = User.query.filter_by(cpf=data['cpf']).first()
    if existing_user:
        existing_user.has_patient_history = True

    try:
        db.session.add(new_patient)
        db.session.commit()

        return jsonify({"message": "Patient registered successfully"}), 201
    
    except IntegrityError as e:
        db.session.rollback()
        if 'duplicate key value violates unique constraint' in str(e.orig):
            return jsonify({"error": "CPF already registered"}), 409
        
        return jsonify({"error": "Database error"}), 500

# Endpoint 11: Obter Dados do Paciente
@app.route('/patients/<int:id>', methods=['GET'])
@jwt_required()
@role_required(['admin', 'medico'])
def get_patient(id):
    from models import Patient
    patient = Patient.query.get(id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    patient_data = {
        "id": patient.id,
        "name": patient.name,
        "age": calculate_age(patient.birth_date),
        "medical_conditions": patient.medical_conditions,
        "consent_status": patient.consent_status,
        "created_at": patient.created_at,
        "has_patient_history": True
    }
    return jsonify(patient_data), 200

# Endpoint 12: Atualizar Dados do Paciente
@app.route('/patients/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin', 'medico'])
def update_patient(id):
    from models import Patient
    data = request.get_json()
    patient = Patient.query.get(id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    if "name" in data:
        patient.name = data['name']
    if "birth_date" in data:
        patient.birth_date = data['birth_date']
    if "medical_conditions" in data:
        patient.medical_conditions = data['medical_conditions']
    if "consent_status" in data:
        patient.consent_status = data['consent_status']

    db.session.commit()
    add_audit_log("Patient data updated", get_jwt_identity())
    return jsonify({"message": "Patient data updated successfully"}), 200

# Endpoint 13: Deletar Paciente
@app.route('/patients/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin'])
def delete_patient(id):
    from models import Patient

    patient = Patient.query.get(id)
    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    # Realiza a exclusão lógica ou a anonimização dos dados, em vez de uma exclusão física
    patient.name = "Anonymous"
    patient.age = None
    patient.medical_conditions = "Removed"
    patient.consent_status = False
    patient.cpf = "Anonymous"
    patient.birth_date = patient.birth_date.replace(month=1, day=1)

    db.session.commit()
    add_audit_log("Patient data anonymized", get_jwt_identity())
    return jsonify({"message": "Patient data anonymized successfully"}), 200

# Endpoint 14: Predição de Diabetes
@app.route('/predict/diabetes', methods=['POST'])
@jwt_required()
@role_required(['paciente'])
def predict_diabetes():

    from models import User, Patient

    data = request.get_json()

    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    patient = Patient.query.filter_by(cpf=user.cpf).first()

    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    
    input_data =  {
        "Age": calculate_age(patient.birth_date),
        "BMI": data.get("BMI"),
        "HighChol": data.get("HighChol"),
        "HighBP": data.get("HighBP"),
        "PhysActivity": data.get("PhysActivity"),
        "GenHlth": data.get("GenHlth"),
        "Smoker": data.get("Smoker")
    }

    # Features essenciais para o modelo de diabetes
    required_fields = ['Age', 'BMI', 'HighChol', 'HighBP', 'PhysActivity', 'GenHlth', 'Smoker']
    missing_fields = [field for field in required_fields if field not in input_data]

    if missing_fields:
        return jsonify({"error": "Might Required Fields not totally provided: " + ", ".join(missing_fields)}), 400

    # Preparar os dados de entrada para o modelo
    input_data = [[input_data[field] for field in required_fields]]
    
    try:
        prediction = diabetes_model.predict(input_data)
        probability = diabetes_model.predict_proba(input_data)[0][1]
        add_audit_log("Diabetes prediction made", get_jwt_identity())
        return jsonify({
            "prediction": int(prediction[0]),
            "probability": round(probability, 2),
            "input_data": input_data
        }), 200
    
    except Exception as e:
        return jsonify({"error": f"An Error occured when trying predict Diabetes: {str(e)}"}), 500

# Endpoint 15: Predição de Hipertensão
@app.route('/predict/hypertension', methods=['POST'])
@jwt_required()
@role_required(['paciente'])
def predict_hypertension():

    from models import User, Patient

    data = request.get_json()

    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    patient = Patient.query.filter_by(cpf=user.cpf).first()

    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    
    input_data =  {
        "age": calculate_age(patient.birth_date),
        "trestbps": data.get("trestbps"),
        "chol": data.get("chol"),
        "thalach": data.get("thalach"),
        "exang": data.get("exang"),
        "oldpeak": data.get("oldpeak"),
        "cp": data.get("cp")
    }

    required_fields = ['age', 'trestbps', 'chol', 'thalach', 'exang', 'oldpeak', 'cp']
    missing_fields = [field for field in required_fields if field not in input_data]

    if missing_fields:
        return jsonify({"error": "Might Required Fields not totally provided: " + ", ".join(missing_fields)}), 400

    input_data = [[input_data[field] for field in required_fields]]

    try:
        prediction = hypertension_model.predict(input_data)
        probability = hypertension_model.predict_proba(input_data)[0][1]
        add_audit_log("Hypertension prediction made", get_jwt_identity())
        return jsonify({
            "prediction": int(prediction[0]), 
            "probability": round(probability, 2),
            "input_data": input_data
            }), 200
    
    except Exception as e:
        return jsonify({"error": f"An Error occured when trying predict Hypertension: {str(e)}"}), 500

# Endpoint 16: Predição de AVC
@app.route('/predict/stroke', methods=['POST'])
@jwt_required()
@role_required(['paciente'])
def predict_stroke():

    from models import User, Patient

    data = request.get_json()

    user_id = get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    patient = Patient.query.filter_by(cpf=user.cpf).first()

    if not patient:
        return jsonify({"error": "Patient not found"}), 404
    
    input_data =  {
        "age": calculate_age(patient.birth_date),
        "hypertension": data.get("hypertension"),
        "heart_disease": data.get("heart_disease"),
        "avg_glucose_level": data.get("avg_glucose_level"),
        "bmi": data.get("bmi"),
        "smoking_status": data.get("smoking_status"),
        "ever_married": data.get("ever_married")
    }

    required_fields = ['age', 'hypertension', 'heart_disease', 'avg_glucose_level', 'bmi', 'smoking_status', 'ever_married']
    missing_fields = [field for field in required_fields if field not in input_data]

    if missing_fields:
        return jsonify({"error": "Might Required Fields not totally provided: " + ", ".join(missing_fields)}), 400

    input_data = [[input_data[field] for field in required_fields]]

    try:
        prediction = stroke_model.predict(input_data)
        probability = stroke_model.predict_proba(input_data)[0][1]
        add_audit_log("Stroke prediction made", get_jwt_identity())
        return jsonify({
            "prediction": int(prediction[0]), 
            "probability": round(probability, 2),
            "input_data": input_data
            }), 200
    
    except Exception as e:
        return jsonify({"error": f"An Error occured when trying predict Stroke: {str(e)}"}), 500
    
# Endpoint 17: Visualizar Logs de Auditoria
@app.route('/audit-log', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def get_audit_log():
    from models import AuditLog
    logs = AuditLog.query.all()
    log_list = []
    for log in logs:
        log_data = {
            "id": log.id,
            "user_id": log.user_id,
            "action": log.action,
            "timestamp": log.timestamp
        }
        log_list.append(log_data)
    return jsonify(log_list), 200

# Endpoint 18: Exportar Dados de um Paciente
@app.route('/patients/export/<int:id>/<string:role>', methods=['GET'])
@jwt_required()
@role_required(['admin', 'medico', 'paciente'])
def export_patient_data(id, role):
    from models import Patient
    from models import User

    if role != 'paciente':
        patient = Patient.query.get(id)

    else:
        user = User.query.get(id)
        patient = Patient.query.filter_by(cpf=user.cpf).first()

    if not patient:
        return jsonify({"error": "Patient not found"}), 404

    # Verifica se o paciente forneceu consentimento para exportação de dados
    if not patient.consent_status:
        return jsonify({"error": "Patient did not provide consent"}), 403

    # Dados do paciente a serem exportados
    export_data = {
        "id": patient.id,
        "name": patient.name,
        "age": calculate_age(patient.birth_date),
        "medical_conditions": patient.medical_conditions,
        "created_at": patient.created_at
    }
    add_audit_log("Patient data exported", get_jwt_identity())

    return jsonify(export_data), 200

# Endpoint 19: Atualizar Consentimento Usuário/Paciente
@app.route('/update-consent', methods=['POST'])
@jwt_required()
def update_consent():

    from models import Patient
    from models import User
    
    user_id = get_jwt_identity()
    data = request.get_json()

    if 'consent_status' not in data:
        return jsonify({"error": "Consent status is required"}), 400

    user_consent = None
    try:
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({"error": "User not found"}), 404
        
        user.consent_status = data['consent_status']
        db.session.commit()
        add_audit_log("User consent status updated", get_jwt_identity())

        user_consent = 'User Consent update successfully'

    except Exception as e:
        return jsonify({"error": f"An error ocurred when trying update User consent status: {e}"}), 400
    
    patient_consent = None
    try:
        patient = Patient.query.filter_by(cpf=user.cpf).first()
    
        if not patient:
            add_audit_log("User without Patient history", get_jwt_identity())
        
        patient.consent_status = data['consent_status']
        db.session.commit()
        add_audit_log("Patient consent status updated", get_jwt_identity())

        patient_consent = 'Patient Consent update successfully'

    except Exception as e:
        patient_consent = f"An error ocurred when trying update Patient consent status: {e}"    

    return jsonify({"message": "Consent status updated successfully", 
                    "user_consent": user_consent, "patient_consent": patient_consent}), 200

# Endpoint 20: Obter Todos os Pacientes
@app.route('/patients', methods=['GET'])
@jwt_required()
@role_required(['admin', 'medico'])
def get_all_patients():
    from models import Patient
    patients = Patient.query.filter(
        (Patient.medical_conditions != "Removed") &
        (Patient.name != "Anonymous") &
        (Patient.age.isnot(None))
    ).all()
    patient_list = []
    for patient in patients:
        patient_data = {
            "id": patient.id,
            "name": patient.name,
            "age": calculate_age(patient.birth_date),
            "medical_conditions": patient.medical_conditions,
            "consent_status": patient.consent_status,
            "has_patient_history": True,  
            "created_at": patient.created_at
        }
        patient_list.append(patient_data)
    return jsonify(patient_list), 200

# Endpoint 21: Obter Todos os Usuários
@app.route('/users', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def get_all_users():
    from models import User
    users = User.query.filter(User.role != 'Deleted User').all()
    users_list = []
    for user in users:
        user_data = {
            "id": user.id,
            "name": user.name,
            "role": user.role,
            "email": user.email,
            "has_patient_history": user.has_patient_history,
            "consent_status": user.consent_status,
            "created_at": user.created_at,
        }
        users_list.append(user_data)
    return jsonify(users_list), 200

# Endpoint 22: Deletar Usuário
@app.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin'])
def delete_user(id):
    from models import User

    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Exclusão lógica: Anonimizar o usuário
    user.id = id
    user.name = "Deleted User"
    user.email = "Deleted User"
    user.password = "Deleted User"
    user.role = "Deleted User"
    user.cpf = "Deleted User"
    db.session.commit()
    
    add_audit_log("User anonymized", get_jwt_identity())
    return jsonify({"message": "User anonymized successfully"}), 200

# Endpoint 23: Trocar Senha do Usuário Autenticado
@app.route('/user/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    from models import User

    user_id = get_jwt_identity()
    data = request.get_json()

    old_password = data.get("old_password")
    new_password = data.get("new_password")

    if not old_password or not new_password:
        return jsonify({"error": "Old password and new password are required"}), 400

    user = User.query.get(user_id)
    if not user or not bcrypt.check_password_hash(user.password, old_password):
        return jsonify({"error": "Old password is incorrect"}), 401

    hashed_new_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    user.password = hashed_new_password
    db.session.commit()

    add_audit_log("User password changed", user_id)
    return jsonify({"message": "Password changed successfully"}), 200

# Endpoint 24: Atualizar Informações de Usuário
@app.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
@role_required(['admin'])
def update_user(id):
    from models import User
    data = request.get_json()

    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    if "name" in data:
        user.name = data['name']
    if "email" in data:
        user.email = data['email']
    if "role" in data:
        user.role = data['role']

    db.session.commit()
    add_audit_log("User data updated", get_jwt_identity())
    return jsonify({"message": "User updated successfully"}), 200

# Endpoint 25: Obter o estado atual de Consentimento do Usuário Logado
@app.route('/patients/consent/current', methods=['GET'])
@jwt_required()
def get_current_consent():

    from models import Patient
    from models import User

    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if user.role != 'paciente':
        patient = Patient.query.filter_by(cpf=user.cpf).first()

    else:
        patient = Patient.query.filter_by(cpf=user.cpf).first()
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

    add_audit_log("Current patient consent status obtained", get_jwt_identity())
    return jsonify({"consent_status": patient.consent_status}), 200     

# Endpoint 26: Listar Pacientes de um Médico
@app.route('/doctor/<int:doctor_id>/patients', methods=['GET'])
@jwt_required()
@role_required(['admin', 'medico'])
def findAll_doctor_patients(doctor_id):
    
    from models import DoctorPatient, Patient
    
    patients = db.session.query(Patient).join(DoctorPatient).filter(DoctorPatient.doctor_id == doctor_id).all()
    
    return jsonify([patients.to_dict() for patient in patients])

# Endpoint 27: Listar Médicos de um Paciente
@app.route('/patient/<int:patient_id>/doctors', methods=['GET'])
@jwt_required()
@role_required(['admin', 'medico'])
def listar_medicos_paciente(patient_id):

    from models import DoctorPatient, User

    doctors = db.session.query(User).join(DoctorPatient).filter(DoctorPatient.patient_id == patient_id).all()
    
    return jsonify([doctors.to_dict() for doctor in doctors])

# Endpoint 28: Salvar Predição
@app.route('/save-prediction', methods=['POST'])
@jwt_required()
def save_prediction():

    from models import Patient
    from mongo_models import PredictionData

    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        prediction_type = data.get("prediction_type")
        input_data = data.get("input_data")
        prediction_result = data.get("prediction_result")

        patient = Patient.query.filter_by(id=user_id).first()

        # Armazena a predição no MongoDB
        new_prediction = {
            "user_id": user_id,
            "patient_id": patient.id,
            "prediction_type": prediction_type,
            "input_data": input_data,
            "prediction_result": prediction_result,
            "timestamp": datetime.utcnow()
        }

        validated_data = PredictionData(new_prediction)
        prediction_collection.insert_one(validated_data.dict())

    except Exception as e:
        return jsonify({f"Error occured when trying save prediction: {str(e)}"}), 400

    return jsonify({"message": "Prediction successfully saved"}), 201

# Endpoint 29: Ver predições feitas pelo próprio usuário paciente autenticado
@app.route('/user/predictions', methods=['GET'])
@jwt_required()
@role_required(['paciente'])
def get_user_predictions():

    try:
        user_id = get_jwt_identity()
        
        # Buscar predições no MongoDB
        predictions = list(prediction_collection.find({"user_id": user_id}))
        for prediction in predictions:
            prediction["_id"] = str(prediction["_id"])  
 
    except Exception as e:
        return jsonify({ "message": f"An error occured when trying get your predictions history: {e}" }), 400
    
    return jsonify(predictions), 200

# Endpoint 30: Associar um médico a um paciente
@app.route('/doctor-patient', methods=['POST'])
@jwt_required()
@role_required(['medico'])
def associate_doctor_patient():

    from models import DoctorPatient

    data = request.get_json()
    doctor_id = get_jwt_identity()
    patient_id = data.get("patient_id")
    
    # Verificar se já existe associação
    existing_association = DoctorPatient.query.filter_by(doctor_id=doctor_id, patient_id=patient_id).first()
    if existing_association:
        return jsonify({"message": "It has an association with this patient already."}), 400

    try:
        # Criar nova associação
        new_association = DoctorPatient(doctor_id=doctor_id, patient_id=patient_id)
        db.session.add(new_association)
        db.session.commit()

    except Exception as e:
        return jsonify({"message": f"An error occured when trying create association: {e}"})

    return jsonify({"message": "Created association successfully."}), 201

# Endpoint 31: Listar Pacientes Associados a um Médico
@app.route('/doctor/<int:doctor_id>/patients', methods=['GET'])
@jwt_required()
@role_required(['medico'])
def list_doctor_patients(doctor_id):

    from models import DoctorPatient, Patient

    associations = DoctorPatient.query.filter_by(doctor_id=doctor_id).all()
    patients = [Patient.query.get(assoc.patient_id).to_dict() for assoc in associations]

    return jsonify(patients), 200

# Endpoint 32: Listar Médicos Associados a um Paciente
@app.route('/patient/<int:patient_id>/doctors', methods=['GET'])
@jwt_required()
@role_required(['paciente'])
def list_patient_doctors(patient_id):

    from models import DoctorPatient, User

    associations = DoctorPatient.query.filter_by(patient_id=patient_id).all()
    doctors = [User.query.get(assoc.doctor_id).to_dict() for assoc in associations]

    return jsonify(doctors), 200

# Endpoint 33: Ver predições de um paciente associado a um médico
@app.route('/doctor/<int:doctor_id>/patient/<int:patient_id>/predictions', methods=['GET'])
@jwt_required()
@role_required(['medico'])
def get_patient_predictions(doctor_id, patient_id):

    from models import DoctorPatient

    try:

        # Verificar associação entre médico e paciente
        association = DoctorPatient.query.filter_by(doctor_id=doctor_id, patient_id=patient_id).first()
        if not association:
            return jsonify({"error": "You are not associate to this patient. Access refused."}), 403

        # Buscar predições no MongoDB
        predictions = list(prediction_collection.find({"user_id": patient_id}))
        for prediction in predictions:
            prediction["_id"] = str(prediction["_id"])  
    
    except Exception as e:
        return jsonify({ "message": f"An error occured when trying get patient predictions history: {e}" }), 400

    return jsonify(predictions), 200

# Endpoint 34: Ver predições de todos os pacientes associado a um médico
@app.route('/doctor/<int:doctor_id>/predictions', methods=['GET'])
@jwt_required()
@role_required(['medico'])
def get_doctor_patient_predictions(doctor_id):
    
    from models import DoctorPatient

    try:
        # Verificar associação e consentimento
        associations = DoctorPatient.query.filter_by(doctor_id=doctor_id).all()
        patient_ids = [assoc.patient_id for assoc in associations]

        predictions = list(prediction_collection.find({"user_id": {"$in": patient_ids}}))
        for prediction in predictions:
            prediction["_id"] = str(prediction["_id"])
    
    except Exception as e:
        return jsonify({ "message": f"An error occured when trying get patients predictions history: {e}" }), 400

    return jsonify(predictions), 200

# Endpoint 35: Ver predições de todos os pacientes de maneira anonimizada (para admins)
@app.route('/admin/predictions', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def get_all_predictions():

    try:
        predictions = list(prediction_collection.find({}, {"user_id": 1, "prediction_type": 1, "result": 1, "probability": 1, "timestamp": 1}))
        for prediction in predictions:
            prediction["_id"] = str(prediction["_id"])

    except Exception as e:
        return jsonify({ "message": f"An error occured when trying get patients predictions history: {e}" }), 400

    return jsonify(predictions), 200

if __name__ == '__main__':
    configure_mongo_indexes()
    app.run(debug=True, port=5001)
