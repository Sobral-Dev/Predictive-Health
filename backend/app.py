from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import timedelta
from flask_mail import Mail, Message
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
import uuid
import logging
import joblib
from auth import validate_login, role_required, add_audit_log, revoke_token
from config import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgre:853211@localhost:5432/PatientSystem'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super-secret-key'

# Inicializando o CORS
CORS(app)

# Conectando ao banco Postgre
db.init_app(app)
migrate = Migrate(app, db)

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
@app.route('/register', methods=['POST'])
@jwt_required()
@role_required(['admin'])
def register():
    from models import User
    from schemas import UserSchema

    data = request.get_json()
    user_schema = UserSchema()
    errors = user_schema.validate(data)

    if errors:
        return jsonify(errors), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    try:
        new_user = User(
            name=data['name'],
            email=data['email'],
            password=hashed_password,
            role=data['role'],
            cpf=data['cpf']
        )
        db.session.add(new_user)
        db.session.commit()
        add_audit_log("User registered", new_user.id)

    except IntegrityError as e:
        db.session.rollback() 
        
        if 'duplicate key value violates unique constraint' in str(e.orig):
            return jsonify({"error": "CPF already registered"}), 409
        
        return jsonify({"error": "Database integrity error"}), 500
    
    return jsonify({"message": "User registered successfully", "user_id": new_user.id}), 201

# Endpoint 2: Solicitar Consentimento Inicial
@app.route('/consent-initial', methods=['POST'])
@jwt_required()
def consent_initial():
    from models import User
    from models import Patient
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

    return jsonify({"access_token": access_token, "user_name": user.name, "user_id": user.id, "user_role": user.role, "consent_status": user.consent_status}), 200

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
        "consent_status": user.consent_status
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

    # Enviar email com o link de redefinição
    msg = Message("Password Reset Request", sender="no-reply@example.com", recipients=[user.email])
    msg.body = f"To reset your password, use the following token: {reset_token}"
    mail.send(msg)

    return jsonify({"message": "Password reset email sent"}), 200

# Endpoint 9: Redefinir Senha
@app.route('/password-reset', methods=['POST'])
def password_reset():
    from models import User
    data = request.get_json()
    email = data.get("email")
    reset_token = data.get("reset_token")
    new_password = data.get("new_password")

    user = User.query.filter_by(email=email, reset_token=reset_token).first()
    if not user:
        return jsonify({"error": "Invalid token or email"}), 400

    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    user.password = hashed_password
    user.reset_token = None  
    db.session.commit()

    return jsonify({"message": "Password updated successfully"}), 200

# Endpoint 10: Criar Paciente
@app.route('/patients', methods=['POST'])
@jwt_required()
@role_required(['admin', 'medico'])
def create_patient():
    from models import Patient
    
    data = request.get_json()
    
    if not data.get("name") or not data.get("age") or not data.get("medical_conditions") or not data.get("cpf"):
        return jsonify({"error": "Missing required fields"}), 400

    consent_status = data.get("consent_status")
    if consent_status is None:
        return jsonify({"error": "Consent status is required"}), 400

    try:
        new_patient = Patient(
            name=data['name'],
            age=data['age'],
            medical_conditions=data['medical_conditions'],
            consent_status=consent_status,
            cpf=data['cpf']
        )
        db.session.add(new_patient)
        db.session.commit()
        add_audit_log("Patient created", get_jwt_identity())
    
    except IntegrityError as e:
        db.session.rollback()  
   
        if 'duplicate key value violates unique constraint' in str(e.orig):
            return jsonify({"error": "CPF already registered"}), 409
    
        return jsonify({"error": "Database integrity error"}), 500

    return jsonify({"message": "Patient created successfully", "patient_id": new_patient.id}), 201

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
        "age": patient.age,
        "medical_conditions": patient.medical_conditions,
        "consent_status": patient.consent_status
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
    if "age" in data:
        patient.age = data['age']
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

    db.session.commit()
    add_audit_log("Patient data anonymized", get_jwt_identity())
    return jsonify({"message": "Patient data anonymized successfully"}), 200

# Endpoint 14: Predição de Diabetes
@app.route('/predict/diabetes', methods=['POST'])
@jwt_required()
@role_required(['admin', 'medico', 'paciente'])
def predict_diabetes():
    data = request.get_json()

    # Verificar se todos os campos necessários estão presentes
    required_fields = ['age', 'bmi', 'glucose_level']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    if not data.get("consent_status"):
        return jsonify({"error": "User consent is required for prediction"}), 403

    # Preparar os dados para a predição
    input_data = [[data['age'], data['bmi'], data['glucose_level']]]
    prediction = diabetes_model.predict(input_data)
    probability = diabetes_model.predict_proba(input_data)[0][1]

    add_audit_log("Diabetes prediction made", get_jwt_identity())
    return jsonify({
        "prediction": int(prediction[0]),
        "probability": round(probability, 2)
    }), 200

# Endpoint 15: Predição de Hipertensão
@app.route('/predict/hypertension', methods=['POST'])
@jwt_required()
@role_required(['admin', 'medico', 'paciente'])
def predict_hypertension():
    data = request.get_json()

    # Verificar se todos os campos necessários estão presentes
    required_fields = ['age', 'blood_pressure', 'cholesterol']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    if not data.get("consent_status"):
        return jsonify({"error": "User consent is required for prediction"}), 403

    # Preparar os dados para a predição
    input_data = [[data['age'], data['blood_pressure'], data['cholesterol']]]
    prediction = hypertension_model.predict(input_data)
    probability = hypertension_model.predict_proba(input_data)[0][1]

    add_audit_log("Hypertension prediction made", get_jwt_identity())
    return jsonify({
        "prediction": int(prediction[0]),
        "probability": round(probability, 2)
    }), 200

# Endpoint 16: Predição de AVC
@app.route('/predict/stroke', methods=['POST'])
@jwt_required()
@role_required(['admin', 'medico', 'paciente'])
def predict_stroke():
    data = request.get_json()

    # Verificar se todos os campos necessários estão presentes
    required_fields = ['age', 'smoking_status', 'bmi']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    if not data.get("consent_status"):
        return jsonify({"error": "User consent is required for prediction"}), 403

    # Preparar os dados para a predição
    input_data = [[data['age'], data['smoking_status'], data['bmi']]]
    prediction = stroke_model.predict(input_data)
    probability = stroke_model.predict_proba(input_data)[0][1]

    add_audit_log("Stroke prediction made", get_jwt_identity())
    return jsonify({
        "prediction": int(prediction[0]),
        "probability": round(probability, 2)
    }), 200

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
        "age": patient.age,
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
            "age": patient.age,
            "medical_conditions": patient.medical_conditions,
            "consent_status": patient.consent_status,
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
            "email": user.email
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

        add_audit_log("Current patient consent status obtained", get_jwt_identity())
        return jsonify({"consent_status": patient.consent_status}), 200

    else:
        patient = Patient.query.filter_by(cpf=user.cpf).first()
        if not patient:
            return jsonify({"error": "Patient not found"}), 404     


if __name__ == '__main__':
    app.run(debug=True)
