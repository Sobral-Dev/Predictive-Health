from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity, get_jwt
from datetime import timedelta
from flask_mail import Mail, Message
from flask_cors import CORS
import uuid
from utils.serialize_helper import serialize_document
from utils.logging_config import log_request_response
import joblib
from utils.auth import role_required, add_audit_log, revoke_token
from utils.calculate_age_helper import calculate_age
from werkzeug.serving import WSGIRequestHandler
from cryptography.fernet import Fernet
import time
from datetime import datetime
from redis import Redis
from utils.jwt_keys import get_active_jwt_key, store_jwt_key
from repositories.AuditLogRepository import AuditLogRepository
from repositories.ConsentTermRepository import ConsentTermRepository
from repositories.DoctorPatientRepository import DoctorPatientRepository
from repositories.JWTKeyRepository import JWTKeyRepository
from repositories.PatientRepository import PatientRepository
from repositories.PredictionDataRepository import PredictionDataRepository
from repositories.RevokedTokenRepository import RevokedTokenRepository
from repositories.UserConsentRepository import UserConsentRepository
from repositories.UserRepository import UserRepository
from models.DoctorPatientModel import DoctorPatientModel
from models.PatientModel import PatientModel
from models.PredictionDataModel import PredictionDataModel
from models.UserModel import UserModel
from utils.consents_helper import get_terms
from utils.mongodb_indexes import create_indexes, drop_indexes
import os
from bson import ObjectId

app = Flask(__name__)
app = log_request_response(app)
WSGIRequestHandler.protocol_version = "HTTP/1.1"

# Configuração de email usando Mailtrap
app.config['MAIL_SERVER']= 'sandbox.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 2525
app.config['MAIL_USERNAME'] = 'd572e6ff412340'
app.config['MAIL_PASSWORD'] = '73e2c3d1fc80cf'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = 'predictive-health@noreply.com'
mail = Mail(app)

# Configurando Fernet Cryptography
if os.path.exists("encryption_key.key"):
    with open("encryption_key.key", "rb") as key_file:
        encryption_key = key_file.read()
else:
    encryption_key = Fernet.generate_key()
    with open("encryption_key.key", "wb") as key_file:
        key_file.write(encryption_key)

cipher_suite = Fernet(encryption_key)

# Configurando chave JWT
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_HEADER_NAME'] = 'Authorization'
app.config['JWT_HEADER_TYPE'] = 'Bearer'

active_key = get_active_jwt_key()

if active_key:
    app.config["JWT_SECRET_KEY"] = active_key
else:
    new_key = Fernet.generate_key().decode("utf-8")
    store_jwt_key(new_key)  
    app.config["JWT_SECRET_KEY"] = new_key

# Variáveis para bloqueio temporário e limitar solicitações
login_attempts = {}
reset_requests = {}

# Inicializando o CORS
CORS(app, resources={r"/*": {"origins": "*"}})

# Inicializando conexão com o Redis
redis_client = Redis(host='localhost', port=6379, decode_responses=True)

# Configurando ferramentas de criptografia no app
bcrypt = Bcrypt(app)
jwt = JWTManager(app)

# Criando instâncias dos Repositories
UserRepository = UserRepository()
PatientRepository = PatientRepository()
DoctorPatientRepository = DoctorPatientRepository()
ConsentTermRepository = ConsentTermRepository()
UserConsentRepository = UserConsentRepository()
RevokedTokenRepository = RevokedTokenRepository()
JWTKeyRepository = JWTKeyRepository()
AuditLogRepository = AuditLogRepository()
PredictionDataRepository = PredictionDataRepository()

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
            diabetes_model = joblib.load(r'C:\Users\felip\OneDrive\Downloads\Predictive-Health\models\diabetes_model.pkl')
        except Exception as e:
            print(f"Erro ao carregar o modelo de Diabetes: {e}")
        try:
            hypertension_model = joblib.load(r'C:\Users\felip\OneDrive\Downloads\Predictive-Health\models\hypertension_model.pkl')
        except Exception as e:
            print(f"Erro ao carregar o modelo de Hipertensão: {e}")
        try:
            stroke_model = joblib.load(r'C:\Users\felip\OneDrive\Downloads\Predictive-Health\models\stroke_model.pkl')
        except Exception as e:
            print(f"Erro ao carregar o modelo de AVC: {e}")
        first_request_executed = True
        app.logger.info("All predictive models loaded successfully")

@app.before_request
def check_revoked_token():
    if request.endpoint in ['/login', '/password-reset-request']:
        return
    if request.headers.get("Authorization"):  
        try:

            token_identity = get_jwt_identity()

            if token_identity:  # Verifica se o JWT é válido antes de continuar
                jti = get_jwt()['jti']
                token_revoked = RevokedTokenRepository.find_one({"jti": jti}) 

                if token_revoked:
                    # Registro da tentativa de uso de token revogado
                    add_audit_log(
                        action="Attempted use of revoked token",
                        user_id=ObjectId(token_identity),
                        details={
                            "jti": jti,
                            "ip_address": request.remote_addr,
                            "user_agent": request.headers.get('User-Agent', 'Unknown')
                        }
                    )
                    return jsonify({'error': 'Token has been revoked'}), 401

        except Exception:
            pass

# Usando a chave ativa dinâmica no JWTManager
@jwt.decode_key_loader
def custom_decode_key(jwt_header, jwt_payload):
    return app.config["JWT_SECRET_KEY"]

# Callback para verificar se o token está na lista de tokens revogados
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    token = RevokedTokenRepository.find_one({"jti": jti}) 
    return token is not None

@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f"Error: {str(e)}", exc_info=True)
    print(e)
    return jsonify({"error": f"An internal error occurred: {str(e)}"}), 500

@app.before_request
def log_request_data():
    if request.method in ['POST', 'PUT', 'PATCH']:
        app.logger.debug(f"Headers: {request.headers}")
        app.logger.debug(f"Body: {request.get_data()}")

@app.before_request
def log_mime_type():
    app.logger.debug(f"Content-Type: {request.content_type}")

# Rota Raíz
@app.route('/')
def home():
    return "Welcome to the Health Predictive System!"

# Endpoint 1: Registro de Usuário
@app.route('/register_user', methods=['POST'])
@role_required(['admin'])
def register_user():

    from email_validator import validate_email, EmailNotValidError

    data = request.get_json()

    # Criptografar o CPF
    encrypted_cpf = cipher_suite.encrypt(data['cpf'].encode('utf-8'))

    # Verificar se o CPF já existe
    if UserRepository.find_one({"cpf_encrypted": encrypted_cpf}):
        return jsonify({'error': 'CPF already exists'}), 400

    # Verificar se o email já existe
    if UserRepository.find_one({"email": data['email']}):
        return jsonify({'error': 'Email already exists'}), 400
    
    # Validação do email
    try:
        validate_email(data['email'])
    except EmailNotValidError:
        return jsonify({"error": "Invalid email format"}), 400

    # Criar o novo usuário
    new_user = UserModel(
        name=data['name'],
        email=data['email'],
        password=bcrypt.generate_password_hash(data['password']).decode('utf-8'),
        role=data['role'],
        cpf_encrypted=encrypted_cpf,
    )

    try:
        # Adicionar o novo usuário ao banco de dados
        UserRepository.insert_one(new_user)

        # Registrar log de auditoria
        add_audit_log(
            user_id=ObjectId(new_user.id),
            action="User registration",
            details={
                "created_by": get_jwt_identity(),
                "new_user_id": str(new_user.id),
                "encrypted_cpf": encrypted_cpf.decode('utf-8'),
                "admin_ip": request.remote_addr,
                "endpoint": "/register_user"
            }
        )

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": f'Unexpected error: {e}'}), 500

# Endpoint 3: Login de Usuário
@app.route('/login', methods=['POST'])
def login():

    data = request.get_json()
    email = data.get('email')
    password_or_token = data.get('password')
    client_ip = request.remote_addr

    if not email or not password_or_token:
        return jsonify({'error': 'Email and password/reset token are required'}), 400

    # Limite de tentativas por IP
    block_key = f"login_block:{client_ip}"
    if redis_client.exists(block_key):
        remaining_time = redis_client.ttl(block_key)
        return jsonify({'error': f'Too many failed attempts. Try again in {remaining_time} seconds.'}), 429

    # Verificar tentativas falhas
    attempts_key = f"login_attempts:{client_ip}"
    attempts = redis_client.get(attempts_key) or 0

    user = UserRepository.find_one({"email": email})
   
    # Validação de credenciais
    if not user or not bcrypt.check_password_hash(user.password, password_or_token):

        attempts = int(attempts) + 1
        redis_client.set(attempts_key, attempts, ex=300)  # Expira em 5 minutos
        if attempts >= 5:
            redis_client.set(block_key, "blocked", ex=300)  # Bloqueio por 5 minutos

        # Log para auditoria em caso de tentativa falha
        add_audit_log(
            action="Failed login attempt",
            user_id=None,  # Usuário não identificado
            details={
                "ip_address": client_ip,
                "attempted_email": email,
                "attempt_method": "Password" if bcrypt.check_password_hash(user.password, password_or_token) else "Reset Token",
                "endpoint": "/login"
            }
        )

        return jsonify({'error': 'Invalid credentials'}), 401

    # Autenticação com senha
    if bcrypt.check_password_hash(user.password, password_or_token):
        try:

            # Criar token de acesso
            access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))

            consents_response = get_terms(str(user.id))

            # Log de auditoria
            add_audit_log(
                action="User login",
                user_id=user.id,
                details={
                    "ip_address": client_ip,
                    "login_way": 'Password',
                    "consent_status": consents_response,
                    "endpoint": "/login"
                }
            )

            # Resetar tentativas após login bem-sucedido
            redis_client.delete(attempts_key)

            return jsonify({
                "access_token": access_token,
                "user_name": user.name,
                "user_id": str(user.id),
                "user_role": user.role,
                "consent_status": consents_response
            }), 200

        except Exception as e:
            return jsonify({'error': 'Database error', 'details': {e}}), 500

    # Autenticação com token de redefinição de senha
    if user.reset_token == password_or_token:
        try:
            # Invalidar token de redefinição
            update_result = UserRepository.update_one({"_id": user.id}, {"reset_token": None})

            if update_result:
                print("Reset Token atualizado com sucesso!")
            else:
                print("Reset Token não encontrado ou nenhum dado foi modificado.")

            # Criar token de acesso
            access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=1))

            consents_response = get_terms(str(user.id))

            # Log de auditoria
            add_audit_log(
                action="User login",
                user_id=user.id,
                details={
                    "ip_address": client_ip,
                    "login_way": 'Reset Token',
                    "consent_status": consents_response,
                    "endpoint": "/login"
                }
            )

            # Resetar tentativas após login bem-sucedido
            redis_client.delete(attempts_key)

            return jsonify({
                "access_token": access_token,
                "user_name": user.name,
                "user_id": str(user.id),
                "user_role": user.role,
                "consent_status": consents_response
            }), 200

        except Exception as e:
            return jsonify({'error': 'Database error', 'details': str(e)}), 500

    return jsonify({"error": "Invalid email or password/reset token"}), 401

# Endpoint 4: Logout de Usuário
@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    try:
        # Obter informações do token
        token_data = get_jwt()
        jti = token_data['jti']
        user_id = get_jwt_identity()

        # Revogar o token
        revoke_token(jti)

        # Registrar o logout nos logs de auditoria
        add_audit_log(
            action="Logout",
            user_id=ObjectId(user_id),
            details={
                "ip_address": request.remote_addr,
                "jti": jti,
                "user_agent": request.headers.get('User-Agent', 'Unknown'),
                "endpoint": "/logout"
            }
        )

    except KeyError as e:
        # Caso falte algum dado esperado no JWT
        return jsonify({
            'error': 'Token data missing or invalid',
            'details': str(e)
        }), 400

    except Exception as e:
        # Erros gerais
        return jsonify({
            'error': 'An unexpected error occurred during logout',
            'details': str(e)
        }), 500

    return jsonify({"message": "Logged out successfully"}), 200

# Endpoint 5: Visualizar Dados Pessoais
@app.route('/user/me', methods=['GET'])
@jwt_required()
def get_user_data():

    try:
        # Obter o ID do usuário a partir do token JWT
        user_id = get_jwt_identity()

        # Consultar o banco de dados pelo usuário
        user = UserRepository.find_one({"_id": ObjectId(user_id)})
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Registrar acesso nos logs de auditoria
        add_audit_log(
            action="Access user profile",
            user_id=ObjectId(user_id),
            details={
                "ip_address": request.remote_addr,
                "user_role": str(user.role),
                "endpoint": "/user/me"
            }
        )

        # Construir os dados do usuário para a resposta
        user_data = {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else None
        }

        return jsonify(user_data), 200

    except Exception as e:
        app.logger.error(f"Unexpected error during user data retrieval: {str(e)}")
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

# Endpoint 6: Atualizar Dados Pessoais
@app.route('/user/me', methods=['PUT'])
@jwt_required()
def update_user_data():

    try:
        # Obter o ID do usuário a partir do token JWT
        user_id = get_jwt_identity()
        user = UserRepository.get_by_id(ObjectId(user_id))

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Obter os dados enviados na requisição
        data = request.get_json()
        audit_details = {
            "changes": {},
            "ip_address": request.remote_addr,
            "endpoint": "/user/me"
        }

        update_fields = {}

        # Atualizar o e-mail se fornecido e válido
        if 'email' in data:
            existing_email_user = UserRepository.find_one({"email": data['email']})
            if existing_email_user and existing_email_user.id != user.id:
                return jsonify({'error': 'Email already exists'}), 400
            audit_details['changes']['email'] = {"old": user.email, "new": data['email']}
            update_fields['email'] = data['email']

        # Atualizar o nome se fornecido
        if 'name' in data:
            audit_details['changes']['name'] = {"old": user.name, "new": data['name']}
            update_fields['name'] = data['name']
            
        if update_fields:
            update_result = UserRepository.update_many({"_id": ObjectId(user_id)}, update_fields)

            if update_result:
                print("Usuário atualizado com sucesso!")
            else:
                print("Usuário não encontrado ou não foi modificado.")

        # Registrar logs de auditoria
        add_audit_log(
            action="Update user info",
            user_id=ObjectId(user_id),
            details=audit_details,
        )

        return jsonify({
            "message": "User updated successfully"
        }), 200

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": e}), 500

# Endpoint 7: Exportar Dados Pessoais
@app.route('/user/export', methods=['GET'])
@jwt_required()
def export_user_data():

    try:
        # Identificar o usuário a partir do token JWT
        user_id = get_jwt_identity()
        user = UserRepository.get_by_id(ObjectId(user_id))

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Preparar os dados para exportação
        export_data = {
            "id": str(user.id),
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.isoformat()
        }

        # Registro de auditoria para exportação de dados
        add_audit_log(
            action="Export user data",
            user_id=ObjectId(user_id),
            details={
                "ip_address": request.remote_addr,
                "fields_exported": list(export_data.keys()),
                "endpoint": "/user/export"
            }
        )

        return jsonify(export_data), 200

    except Exception as e:
        return jsonify({"error": "An error occurred", "details": str(e)}), 500

# Endpoint 8: Solicitar Redefinição de Senha
@app.route('/password-reset-request', methods=['POST'])
def password_reset_request():

    try:
        data = request.get_json()
        email = data.get("email")

        if not email:
            return jsonify({'error': 'Email is required'}), 400

        client_ip = request.remote_addr

        # Lógica para limitar solicitações por IP
        if client_ip in reset_requests and reset_requests[client_ip]['count'] >= 5:
            block_time = reset_requests[client_ip]['time']
            if time.time() - block_time < 600:  # Bloqueio de 10 minutos
                return jsonify({'error': 'Too many reset requests. Try again later.'}), 429
            else:
                del reset_requests[client_ip]  # Remove o registro após o bloqueio expirar

        user = UserRepository.find_one({"email": email})

        if not user:
            # Resposta genérica para evitar expor informações de existência do email
            add_audit_log(
                action="Password reset request - non-existent user",
                user_id=None,
                details={
                    "ip_address": client_ip,
                    "email_attempted": email,
                    "endpoint": "/password-reset-request"
                }
            )
            return jsonify({"message": "If the email exists, a reset link will be sent."}), 200

        # Geração de token de redefinição
        reset_token = str(uuid.uuid4())
        
        update_result = UserRepository.update_one({"_id": user.id}, {"reset_token": reset_token})

        if update_result:
            print("Reset Token do Usuário atualizado com sucesso!")
        else:
            print("Usuário não encontrado ou o Reset Token não foi modificado.")

        # Envio de email com o link de redefinição (simulado com Mailtrap)
        msg = Message("Password Reset Request", recipients=[user.email])
        msg.body = f"To reset your password, use the following token: {reset_token}"
        mail.send(msg)

        # Registro de auditoria para a solicitação de redefinição
        add_audit_log(
            action="Password reset request",
            user_id=user.id,
            details={
                "ip_address": client_ip,
                "email_sent_to": user.email,
                "endpoint": "/password-reset-request"
            }
        )

        # Registro de tentativas por IP
        if client_ip not in reset_requests:
            reset_requests[client_ip] = {'count': 1, 'time': time.time()}
        else:
            reset_requests[client_ip]['count'] += 1

        return jsonify({"message": "If the email exists, a reset link will be sent."}), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred', 'details': str(e)}), 500

# Endpoint 9: Redefinir Senha
@app.route('/password-reset', methods=['POST'])
def password_reset():

    try:
        data = request.get_json()

        reset_token = data.get("reset_token")
        new_password = data.get("new_password")
        user_id = data.get("user_id")

        # Validação dos dados de entrada
        if not user_id or not reset_token or not new_password:
            return jsonify({'error': 'User ID, reset token, and new password are required'}), 400

        user = UserRepository.find_one({"_id": ObjectId(user_id)})
        if not user:
            add_audit_log(
                action="Password reset attempt - invalid user",
                user_id=None,
                details={
                    "user_id_attempted": user_id,
                    "ip_address": request.remote_addr,
                    "endpoint": "/password-reset"
                }
            )
            return jsonify({"error": "Invalid user ID or token"}), 400

        if user.reset_token != reset_token:
            add_audit_log(
                action="Password reset attempt - invalid token",
                user_id=ObjectId(user_id),
                details={
                    "ip_address": request.remote_addr,
                    "endpoint": "/password-reset"
                }
            )
            return jsonify({'error': 'Invalid reset token'}), 400

        # Atualização da senha
        hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        user.password = hashed_password
        
        update_result = UserRepository.update_one({"_id": ObjectId(user_id)}, {"reset_token": None})

        if update_result:
            print("Reset Token do Usuário atualizado com sucesso!")
        else:
            print("Usuário não encontrado ou o Reset Token não foi modificado.")

        # Registro de auditoria
        add_audit_log(
            action="Password reset",
            user_id=ObjectId(user_id),
            details={
                "ip_address": request.remote_addr,
                "endpoint": "/password-reset"
            }
        )

        return jsonify({"message": "Password updated successfully"}), 200

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

# Endpoint 10: Registro de Paciente
@app.route('/register_patient', methods=['POST'])
@jwt_required()
@role_required(['admin', 'medico'])
def register_patient():

    data = request.get_json()

    if not data.get('cpf') or not data.get('name') or not data.get('birth_date'):
        return jsonify({'error': 'Name, CPF, and birth date are required'}), 400

    encrypted_cpf = cipher_suite.encrypt(data['cpf'].encode('utf-8'))

    # Verificar se o CPF já existe
    if PatientRepository.find_one({"cpf_encrypted": encrypted_cpf}):
        return jsonify({'error': 'CPF already exists'}), 400

    new_patient = PatientModel(
        name=data['name'],
        birth_date=data['birth_date'],
        medical_conditions=data.get('medical_conditions'),
        cpf_encrypted=encrypted_cpf
    )

    try:
        # Registrar paciente
        PatientRepository.insert_one(new_patient)

        # Registrar no log de auditoria
        add_audit_log(
            action="Register patient",
            user_id=ObjectId(get_jwt_identity()),
            details={
                "patient_id": new_patient.id,
                "encrypted_cpf": encrypted_cpf.decode('utf-8'),
                "endpoint": "/register_patient"
            }
        )

        # Verificar se o registro foi feito por um médico e criar associação
        user_id = get_jwt_identity()
        user = UserRepository.get_by_id(ObjectId(user_id))

        if user.role == 'medico':
            new_association = DoctorPatientModel(
                doctor_id=ObjectId(user_id),
                patient_id=ObjectId(new_patient.id),
                consent_status='pending'
            )
            DoctorPatientRepository.insert_one(new_association)

            # Registrar associação no log de auditoria
            add_audit_log(
                action="Create doctor-patient association",
                user_id=ObjectId(user_id),
                details={
                    "patient_id": str(new_patient.id),
                    "doctor_id": user_id,
                    "endpoint": "/register_patient"
                }
            )

        return jsonify({"message": "Patient registered successfully"}), 201

    except Exception as e:
        return jsonify({"error": "Unexpected error occurred", "details": str(e)}), 500

# Endpoint 11: Obter Dados do Paciente
@app.route('/patients/<string:id>/<string:role>', methods=['GET'])
@jwt_required()
@role_required(['admin', 'medico', 'paciente'])
def get_patient(id, role):

    try:
        user_id = get_jwt_identity()

        # Identificar o paciente com base no papel do usuário
        if role == 'paciente':
            user = UserRepository.get_by_id(ObjectId(user_id))
            if not user:
                return jsonify({"error": "User not found"}), 404

            patient = PatientRepository.find_one({"cpf_encrypted": user.cpf_encrypted})

        elif role in ['admin', 'medico']:
            patient = PatientRepository.get_by_id(ObjectId(id))

        else:
            return jsonify({"error": "Invalid role"}), 400

        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        # Verificar associação e consentimento para médicos
        if role == 'medico':
            associations = DoctorPatientRepository.find_all({
                "patient_id": ObjectId(id), "doctor_id": ObjectId(user_id), "consent_status": "accepted"
            })

            if not associations:
                return jsonify({"error": "You are not authorized to access this patient's data."}), 401

        # Registrar log de auditoria
        add_audit_log(
            action="Access patient data",
            user_id=ObjectId(user_id),
            details={
                "patient_id": str(patient.id),
                "role": role,
                "ip_address": request.remote_addr,
                "endpoint": "/patients/<id>/<role>"
            }
        )

        # Preparar dados do paciente
        patient_data = {
            "id": str(patient.id),
            "name": patient.name,
            "age": calculate_age(patient.birth_date),
            "birth_date": patient.birth_date.isoformat(),
            "medical_conditions": patient.medical_conditions,
            "created_at": patient.created_at.isoformat()
        }

        return jsonify(patient_data), 200

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

# Endpoint 12: Atualizar Dados do Paciente
@app.route('/patients/<string:id>', methods=['PUT'])
@jwt_required()
@role_required(['medico'])
def update_patient(id):

    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        patient = PatientRepository.get_by_id(ObjectId(id))

        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        # Verificar associação com consentimento aceito
        associations = DoctorPatientRepository.find_all({
            "patient_id": ObjectId(id), "doctor_id": ObjectId(user_id), "consent_status": 'accepted'
        })

        if not associations:
            return jsonify({"error": "You are not authorized to update this patient's data"}), 401

        # Campos atualizados
        updated_fields = {}
        if 'name' in data and data['name'] != patient.name:
            updated_fields['name'] = {'old': patient.name, 'new': data['name']}

            update_result = PatientRepository.update_one({"_id": patient.id}, {"name": data['name']})

            if update_result:
                print("Nome do Paciente atualizado com sucesso!")
            else:
                print("Paciente não encontrado ou o Nome não foi modificado.")

        if 'birth_date' in data and datetime.strptime(data['birth_date'], "%Y-%m-%d").isoformat() != patient.birth_date.isoformat():
            updated_fields['birth_date'] = {'old': patient.birth_date.isoformat(), 'new': datetime.strptime(data['birth_date'], "%Y-%m-%d").isoformat()}

            update_result = PatientRepository.update_one({"_id": patient.id}, {"birth_date": datetime.strptime(data['birth_date'], "%Y-%m-%d")})

            if update_result:
                print("Data de Nascimento do Paciente atualizado com sucesso!")
            else:
                print("Paciente não encontrado ou a Data de Nascimento não foi modificada.")

        if 'medical_conditions' in data:
            if isinstance(data['medical_conditions'], list):
                medical_conditions = data['medical_conditions']
            else:
                medical_conditions = data['medical_conditions'].split(", ")

        if medical_conditions and str(medical_conditions) != str(patient.medical_conditions):
            updated_fields['medical_conditions'] = {
                'old': patient.medical_conditions,
                'new': medical_conditions
            }

            update_result = PatientRepository.update_one({"_id": patient.id}, {"medical_conditions": medical_conditions})

            if update_result:
                print("Condições Médicas do Paciente atualizadas com sucesso!")
            else:
                print("Paciente não encontrado ou Condições Médicas não foram modificadas.")

        # Registrar log de auditoria
        add_audit_log(
            action="Update patient data",
            user_id=ObjectId(user_id),
            details={
                "patient_id": str(patient.id),
                "updated_fields": updated_fields,
                "ip_address": request.remote_addr,
                "endpoint": "/patients/<id>"
            }
        )

        return jsonify({
            "message": "Patient data updated successfully",
            "updated_fields": updated_fields
        }), 200

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

# Endpoint 13: Deletar Paciente
@app.route('/patients/<string:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin'])
def delete_patient(id):

    try:
        patient = PatientRepository.get_by_id(ObjectId(id))
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        # Realiza a anonimização dos dados do paciente
        anonymized_name = "Anonymous"
        anonymized_cpf = cipher_suite.encrypt("Anonymous".encode('utf-8'))

        audit_details = {
            "patient_id": str(patient.id),
            "changes": {
                "name": {"old": patient.name, "new": anonymized_name},
                "medical_conditions": {"old": patient.medical_conditions, "new": None},
                "cpf_encrypted": {"old": patient.cpf_encrypted, "new": anonymized_cpf.decode('utf-8')},
                "birth_date": {"old": patient.birth_date.isoformat(), "new": patient.birth_date.replace(month=1, day=1).isoformat()}
            },
            "ip_address": request.remote_addr,
            "endpoint": "/patients/<id>"
        }

        # Atualiza os campos para anonimizar o paciente
        PatientRepository.update_many({"_id": patient.id}, 
                                    
                                    {
                                        "name": anonymized_name, 
                                        "medical_conditions": None,
                                        "cpf_encrypted": anonymized_cpf,
                                        "birth_date": patient.birth_date.replace(month=1, day=1) 
                                    
                                    }
                                
                                )

        # Registrar log de auditoria
        add_audit_log(
            action="Anonymize patient data",
            user_id=ObjectId(get_jwt_identity()),
            details=audit_details
        )

        return jsonify({"message": "Patient data anonymized successfully"}), 200

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

# Endpoint 14: Predição de Diabetes
@app.route('/predict/diabetes', methods=['POST'])
@jwt_required()
@role_required(['paciente'])
def predict_diabetes():

    try:
        data = request.get_json()

        user_id = get_jwt_identity()
        user = UserRepository.get_by_id(ObjectId(user_id))
        if not user:
            return jsonify({"error": "User not found"}), 404

        patient = PatientRepository.find_one({"cpf_encrypted": user.cpf_encrypted})
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        # Validar dados de entrada
        input_data = {
            "Age": calculate_age(patient.birth_date),
            "BMI": data.get("BMI"),
            "HighChol": data.get("HighChol") if data.get("HighChol") != "" else False,
            "HighBP": data.get("HighBP") if data.get("HighBP") != "" else False,
            "PhysActivity": data.get("PhysActivity") if data.get("PhysActivity") != "" else False,
            "GenHlth": data.get("GenHlth"),
            "Smoker": data.get("Smoker") if data.get("Smoker") != "" else False
        }
        required_fields = ['Age', 'BMI', 'HighChol', 'HighBP', 'PhysActivity', 'GenHlth', 'Smoker']
        missing_fields = [field for field in required_fields if input_data.get(field) is None]

        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        # Preparar dados para o modelo
        input_features = [[input_data[field] for field in required_fields]]

        try:
            # Predição e probabilidade
            prediction = diabetes_model.predict(input_features)
            probability = diabetes_model.predict_proba(input_features)[0][1]

            # Registrar log detalhado
            add_audit_log(
                action="Diabetes prediction",
                user_id=ObjectId(user_id),
                details={
                    "patient_id": str(patient.id),
                    "parameters_used": input_data,
                    "prediction": int(prediction[0]),
                    "probability": round(probability, 2),
                    "endpoint": "/predict/diabetes"
                }
            )

            return jsonify({
                "prediction": int(prediction[0]),
                "probability": round(probability, 2),
                "input_data": input_data
            }), 200

        except Exception as e:
            return jsonify({"error": f"An error occurred during prediction: {str(e)}"}), 500

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

# Endpoint 15: Predição de Hipertensão
@app.route('/predict/hypertension', methods=['POST'])
@jwt_required()
@role_required(['paciente'])
def predict_hypertension():

    try:
        data = request.get_json()

        # Obter usuário autenticado
        user_id = get_jwt_identity()
        user = UserRepository.get_by_id(ObjectId(user_id))
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Obter paciente associado ao usuário
        patient = PatientRepository.find_one({"cpf_encrypted": user.cpf_encrypted})
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        # Dados de entrada e validação
        input_data = {
            "age": calculate_age(patient.birth_date),
            "trestbps": data.get("trestbps"),
            "chol": data.get("chol"),
            "thalach": data.get("thalach"),
            "exang": data.get("exang") if data.get("exang") != "" else False,
            "oldpeak": data.get("oldpeak"),
            "cp": data.get("cp")
        }

        required_fields = ['age', 'trestbps', 'chol', 'thalach', 'exang', 'oldpeak', 'cp']
        missing_fields = [field for field in required_fields if input_data.get(field) is None]

        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        # Preparar dados para predição
        input_features = [[input_data[field] for field in required_fields]]

        try:
            # Fazer predição
            prediction = hypertension_model.predict(input_features)
            probability = hypertension_model.predict_proba(input_features)[0][1]

            # Registrar log de auditoria
            add_audit_log(
                action="Hypertension prediction",
                user_id=ObjectId(user_id),
                details={
                    "patient_id": str(patient.id),
                    "parameters_used": input_data,
                    "prediction": int(prediction[0]),
                    "probability": round(probability, 2),
                    "endpoint": "/predict/hypertension"
                }
            )

            return jsonify({
                "prediction": int(prediction[0]),
                "probability": round(probability, 2),
                "input_data": input_data
            }), 200

        except Exception as e:
            return jsonify({"error": f"An error occurred during prediction: {str(e)}"}), 500

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

# Endpoint 16: Predição de AVC
@app.route('/predict/stroke', methods=['POST'])
@jwt_required()
@role_required(['paciente'])
def predict_stroke():

    try:
        # Obter dados da requisição
        data = request.get_json()

        # Identificar usuário autenticado
        user_id = get_jwt_identity()
        user = UserRepository.get_by_id(ObjectId(user_id))
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Obter paciente associado
        patient = PatientRepository.find_one({"cpf_encrypted": user.cpf_encrypted})
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        # Preparar dados de entrada
        input_data = {
            "age": calculate_age(patient.birth_date),
            "hypertension": data.get("hypertension") if data.get("hypertension") != "" else False,
            "heart_disease": data.get("heart_disease") if data.get("heart_disease") != "" else False,
            "avg_glucose_level": data.get("avg_glucose_level"),
            "bmi": data.get("bmi"),
            "smoking_status": data.get("smoking_status"),
            "ever_married": data.get("ever_married")
        }

        # Verificar campos obrigatórios
        required_fields = ['age', 'hypertension', 'heart_disease', 'avg_glucose_level', 'bmi', 'smoking_status', 'ever_married']
        missing_fields = [field for field in required_fields if input_data.get(field) is None]

        if missing_fields:
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        # Formatando dados para predição
        input_features = [[input_data[field] for field in required_fields]]

        try:
            # Fazer predição
            prediction = stroke_model.predict(input_features)
            probability = stroke_model.predict_proba(input_features)[0][1]

            # Registrar log de auditoria
            add_audit_log(
                action="Stroke prediction",
                user_id=ObjectId(user_id),
                details={
                    "patient_id": str(patient.id),
                    "parameters_used": input_data,
                    "prediction": int(prediction[0]),
                    "probability": round(probability, 2),
                    "endpoint": "/predict/stroke"
                }
            )

            return jsonify({
                "prediction": int(prediction[0]),
                "probability": round(probability, 2),
                "input_data": input_data
            }), 200

        except Exception as e:
            return jsonify({"error": f"An error occurred during prediction: {str(e)}"}), 500

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500
    
# Endpoint 17: Visualizar Logs de Auditoria
@app.route('/audit-log', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def get_audit_log():

    try:

        # Construir query base com filtro de ordem
        logs = AuditLogRepository.find_all({}, sort_field="timestamp", sort_order=-1)

        # Converter os logs para um formato serializável
        serialized_logs = [serialize_document(log.__dict__) for log in logs]

        # Retorno dos logs
        return jsonify({
            "logs": serialized_logs
        }), 200

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

# Endpoint 18: Exportar Dados de um Paciente
@app.route('/patient/export', methods=['GET'])
@jwt_required()
@role_required(['paciente'])
def export_patient_data():

    try:
        # Identidade do usuário autenticado
        user_id = get_jwt_identity()
        client_ip = request.remote_addr

        user = UserRepository.get_by_id(ObjectId(user_id))
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Buscar o paciente associado ao CPF criptografado do usuário
        patient = PatientRepository.find_one({"cpf_encrypted": user.cpf_encrypted})
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        # Preparar os dados de exportação
        export_data = {
            "id": str(patient.id),
            "name": patient.name,
            "age": calculate_age(patient.birth_date),
            "medical_conditions": patient.medical_conditions,
            "created_at": patient.created_at.isoformat(),
            "cpf": "REDACTED",  # Dado sensível
        }

        # Registrar a exportação nos logs de auditoria
        add_audit_log(
            action="Export patient data",
            user_id=ObjectId(user_id),
            details={
                "fields_exported": list(export_data.keys()),
                "patient_id": str(patient.id),
                "ip_address": client_ip,
                "endpoint": "/patient/export"
            }
        )

        # Retornar os dados exportados
        response = jsonify(export_data)
        response.headers['Content-Disposition'] = f'attachment; filename=patient_{str(patient.id)}_data.json'
        response.headers['Content-Type'] = 'application/json'

        return response, 200

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

# Endpoint 19: Atualizar Consentimento Usuário/Paciente
@app.route('/update-consent', methods=['POST'])
@jwt_required()
def update_consent():

    try:
        # Identidade do usuário autenticado
        user_id = get_jwt_identity()
        client_ip = request.remote_addr

        # Recuperar o usuário
        user = UserRepository.get_by_id(ObjectId(user_id))
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Recuperar os dados da requisição
        data = request.get_json()
    
        for term in data['consents']:
            # Verifica se o termo existe na collection de termos de consentimento
            if not ConsentTermRepository.get_term_by_id(term['term_id']):
                return jsonify({'error': 'Invalid term_id'}), 400

            if term['consent_status'] is not None:

                # Atualizar ou inserir o consentimento do usuário
                UserConsentRepository.update_or_insert_user_consent(user_id, term['term_id'], 
                                                                    term['consent_status'], term['version'])

                # Registrar log de auditoria
                add_audit_log(
                    action="Update Consent",
                    user_id=ObjectId(user_id),
                    details={
                        "term_id": term['term_id'],
                        "new_status": term['consent_status'],
                        "ip_address": client_ip,
                        "endpoint": "/update-consent"
                    }
                )

        return jsonify({
            "message": "Consent status updated successfully"
        }), 200

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

# Endpoint 20: Obter Todos os Pacientes
@app.route('/patients', methods=['GET'])
@jwt_required()
@role_required(['admin', 'medico'])
def get_all_patients():
    
    try:
        # Identidade do usuário autenticado
        user_id = get_jwt_identity()
        client_ip = request.remote_addr

        # Filtrar pacientes anonimizados por exclusão
        patients = PatientRepository.find_all({
            "medical_conditions": {"$exists": True, "$ne": None},  
            "name": {"$ne": "Anonymous"}  
        })

        # Preparar a resposta com dados necessários
        patient_list = []
        for patient in patients:
            patient_list.append({
                "id": str(patient.id),
                "name": patient.name,
                "age": calculate_age(patient.birth_date),
                "medical_conditions": patient.medical_conditions,
                "created_at": patient.created_at.isoformat()
            })

        # Log de auditoria
        add_audit_log(
            action="Access patient list",
            user_id=ObjectId(user_id),
            details={
                "ip_address": client_ip,
                "total_patients_accessed": len(patient_list),
                "endpoint": "/patients"
            }
        )

        return jsonify({
            "patients": patient_list
        }), 200

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

# Endpoint 21: Obter Todos os Usuários
@app.route('/users', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def get_all_users():

    try:
        # Identidade do usuário autenticado
        user_id = get_jwt_identity()
        client_ip = request.remote_addr

        # Exclui usuários deletados
        users = UserRepository.find_all({"role": {"$ne": "deleted"}})

        # Preparar resposta com dados necessários
        users_list = [
            {
                "id": str(user.id),
                "name": user.name,
                "role": user.role,
                "email": user.email,
                "created_at": user.created_at.isoformat()
            }
            for user in users
        ]

        # Registrar log de auditoria
        add_audit_log(
            action="Access user list",
            user_id=ObjectId(user_id),
            details={
                "ip_address": client_ip,
                "total_users_accessed": len(users_list),
                "endpoint": "/users"
            }
        )

        return jsonify({
            "users": users_list
        }), 200

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

# Endpoint 22: Deletar Usuário
@app.route('/users/<string:id>', methods=['DELETE'])
@jwt_required()
@role_required(['admin'])
def delete_user(id):

    try:
        user_id = get_jwt_identity()
        client_ip = request.remote_addr

        user = UserRepository.get_by_id(ObjectId(id))
        if not user:
            return jsonify({"error": "User not found"}), 404

        if user.role == 'admin':
            return jsonify({"error": "Cannot delete an admin user"}), 403

        # Exclusão lógica: Anonimizar o usuário
        anonymized_name = f"Deleted_{user.id}"[:50]
        anonymized_email = f"deleted_{user.id}@anon.com"[:120]
        anonymized_cpf = cipher_suite.encrypt(f"deleted{user.id}".encode('utf-8'))

        UserRepository.update_many({"_id": ObjectId(id)}, {
            "name": anonymized_name,
            "email": anonymized_email,
            "password": "DeletedPassword",
            "role": "deleted",
            "cpf_encrypted": anonymized_cpf,
            "reset_token": None,
        })

        # Registro no log de auditoria
        add_audit_log(
            action="Anonymize user",
            user_id=ObjectId(user_id),
            details={
                "anonymized_user_id": id,
                "anonymized_name": anonymized_name,
                "ip_address": client_ip,
                "reason": "Operational Need",
                "endpoint": "/users"
            }
        )

        return jsonify({"message": "User anonymized successfully"}), 200

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

# Endpoint 23: Trocar Senha do Usuário Autenticado
@app.route('/user/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    import time

    try:
        user_id = get_jwt_identity()
        client_ip = request.remote_addr
        data = request.get_json()

        old_password = data.get("old_password")
        new_password = data.get("new_password")

        if not old_password or not new_password:
            return jsonify({"error": "Old password and new password are required"}), 400

        if len(new_password) < 8:
            return jsonify({"error": "New password must be at least 8 characters long"}), 400

        user = UserRepository.get_by_id(ObjectId(user_id))
        if not user:
            return jsonify({'error': 'User not found'}), 404

        if client_ip in login_attempts and login_attempts[client_ip]['count'] >= 5:
            block_time = login_attempts[client_ip]['time']
            if time.time() - block_time < 300:  
                return jsonify({'error': 'Too many failed attempts. Try again later.'}), 429
            else:
                del login_attempts[client_ip]

        if not bcrypt.check_password_hash(user.password, old_password):
            if client_ip not in login_attempts:
                login_attempts[client_ip] = {'count': 1, 'time': time.time()}
            else:
                login_attempts[client_ip]['count'] += 1

            return jsonify({"error": "Old password is incorrect"}), 401

        hashed_new_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
        
        update_result = UserRepository.update_one({"_id": ObjectId(user_id)}, {"password": hashed_new_password})

        if update_result:
            print("Senha do Usuário atualizada com sucesso!")
        else:
            print("Usuário não encontrado ou a senha não foi modificada.")

        if client_ip in login_attempts:
            del login_attempts[client_ip]

        add_audit_log(
            action="Change password",
            user_id=ObjectId(user_id),
            details={
                "ip_address": client_ip,
                "password_strength": "validated",
                "endpoint": "/user/change-password"
            }
        )

        return jsonify({"message": "Password changed successfully"}), 200

    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

# Endpoint 24: Obter Consentimentos do Usuário com Detalhes dos Termos
@app.route('/patients/consent/current', methods=['GET'])
@jwt_required()
def get_current_consent():
    try:

        user_id = get_jwt_identity()
        user = UserRepository.get_by_id(ObjectId(user_id))

        if not user:
            return jsonify({"error": "User not found"}), 404

        consents_response = get_terms(user_id)

        # Registrar no log de auditoria
        add_audit_log(
            action="Access consent status",
            user_id=ObjectId(user_id),
            details={
                "ip_address": request.remote_addr,
                "endpoint": "/patients/consent/current"
            }
        )

        return jsonify({
            "user_id": user_id,
            "consents": consents_response
        }), 200

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

# Endpoint 25: Salvar Predição
@app.route('/save-prediction', methods=['POST'])
@jwt_required()
def save_prediction():

    try:
        data = request.get_json()
        user_id = get_jwt_identity()
        prediction_type = data.get("prediction_type")
        input_data = data.get("input_data")
        prediction_result = data.get("prediction_result")

        if not prediction_type or not input_data or not prediction_result:
            return jsonify({"error": "Prediction type, input data, and result are required"}), 400

        user = UserRepository.get_by_id(ObjectId(user_id))
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Buscar paciente correspondente
        patient = PatientRepository.find_one({"cpf_encrypted": user.cpf_encrypted})
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        # Preparar a predição para armazenamento no MongoDB
        new_prediction = PredictionDataModel(
            user_id= user.id,
            patient_id= patient.id,
            prediction_type= prediction_type,
            input_data= list(input_data) if isinstance(input_data, set) else input_data,
            prediction_result= prediction_result,
            timestamp= datetime.utcnow().isoformat()
        )

        # Inserir a predição no MongoDB
        PredictionDataRepository.insert_one(new_prediction)

        # Registrar ação no log de auditoria
        add_audit_log(
            action="Save prediction",
            user_id=ObjectId(user_id),
            details={
                "prediction_type": prediction_type,
                "patient_id": str(patient.id),
                "input_data_size": len(input_data) if input_data else 0,
                "ip_address": request.remote_addr,
                "endpoint": "/save-prediction"
            }
        )

        return jsonify({"message": "Prediction successfully saved"}), 201

    except Exception as e:
        return jsonify({"error": f"Error occurred when trying to save prediction: {str(e)}"}), 400

# Endpoint 26: Ver predições feitas pelo próprio usuário/paciente autenticado
@app.route('/user/predictions', methods=['GET'])
@jwt_required()
@role_required(['paciente'])
def get_user_predictions():

    try:
        user_id = get_jwt_identity()
        user = UserRepository.get_by_id(ObjectId(user_id))

        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Buscar predições no MongoDB
        predictions = PredictionDataRepository.find_all({"user_id": ObjectId(user_id)})
        predictions = [prediction.to_dict() for prediction in predictions]

        # Registrar no log de auditoria
        add_audit_log(
            action="Access user predictions",
            user_id=ObjectId(user_id),
            details={
                "total_predictions": len(predictions),
                "ip_address": request.remote_addr,
                "endpoint": "/user/predictions"
            }
        )

        # Minimizar dados retornados
        filtered_predictions = [
            {
                "prediction_type": prediction.prediction_type,
                "timestamp": prediction.timestamp,
                "prediction_result": prediction.prediction_result,
            }
            for prediction in predictions
        ]

        return jsonify(filtered_predictions), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred while fetching predictions: {str(e)}"}), 400

# Endpoint 27: Associar um médico a um paciente
@app.route('/doctor-patient', methods=['POST'])
@jwt_required()
@role_required(['medico'])
def associate_doctor_patient():

    try:
        data = request.get_json()
        doctor_id = get_jwt_identity()
        patient_id = data.get("patient_id")

        if not patient_id:
            return jsonify({'error': 'Patient ID is required'}), 400

        patient = PatientRepository.get_by_id(ObjectId(patient_id))
        if not patient:
            return jsonify({'error': 'Patient not found'}), 404

        # Verificar associação existente
        existing_association = DoctorPatientRepository.find_one({"doctor_id": ObjectId(doctor_id), "patient_id": ObjectId(patient_id)})
        if existing_association:
            return jsonify({"message": "Association already exists"}), 400

        # Criar nova associação
        new_association = DoctorPatientModel(
            doctor_id=ObjectId(doctor_id),
            patient_id=ObjectId(patient_id),
            consent_status='pending'
        )
        DoctorPatientRepository.insert_one(new_association)

        add_audit_log(
            action="Create doctor-patient association",
            user_id=ObjectId(doctor_id),
            details={
                "patient_id": patient_id,
                "consent_status": "pending",
                "ip_address": request.remote_addr,
                "endpoint": "/doctor-patient"
            }
        )

        return jsonify({"message": "Association created successfully", "status": "pending"}), 201

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Endpoint 28: Listar Pacientes Associados a um Médico
@app.route('/doctor/<string:doctor_id>/patients', methods=['GET'])
@jwt_required()
@role_required(['medico'])
def list_doctor_patients(doctor_id):

    try:
        user_id = get_jwt_identity()

        # Verificar se o médico autenticado é o mesmo solicitado
        if user_id != doctor_id:
            return jsonify({'error': 'Unauthorized access to other doctor\'s data'}), 403

        # Filtrar associações por médico
        associations = DoctorPatientRepository.find_all({"doctor_id": ObjectId(doctor_id)})

        # Separar pacientes aceitos e pendentes
        patients_accepted = []
        patients_pending = []
        
        for assoc in associations:
            patient = PatientRepository.find_one({"_id": assoc.patient_id})

            if assoc.consent_status == 'accepted':
                
                patient_assoc = {
                        "id": str(patient.id),
                        "name": patient.name,
                        "age": calculate_age(patient.birth_date),
                        "medical_conditions": patient.medical_conditions,
                        "created_at": patient.created_at.isoformat()
                    }
                patients_accepted.append(patient_assoc)
             
            elif assoc.consent_status == 'pending':           

                patient_assoc = {
                        "id": str(patient.id),
                        "name": patient.name,
                        "age": calculate_age(patient.birth_date),
                        "medical_conditions": patient.medical_conditions,
                        "created_at": patient.created_at.isoformat()
                    }
                patients_pending.append(patient_assoc)


        add_audit_log(
            action="Access doctor-patient associations",
            user_id=ObjectId(user_id),
            details={
                "doctor_id": doctor_id,
                "total_patients": len(patients_accepted) + len(patients_pending),
                "ip_address": request.remote_addr,
                "endpoint": f"/doctor/{doctor_id}/patients"
            }
        )

        return jsonify({"patients_accepted": patients_accepted, "patients_pending": patients_pending}), 200

    except Exception as e:
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

# Endpoint 29: Listar Médicos Associados a um Paciente
@app.route('/patient/doctors', methods=['GET'])
@jwt_required()
@role_required(['paciente'])
def list_patient_doctors():

    try:
        user_id = get_jwt_identity()

        # Verificar se o paciente existe
        user = UserRepository.get_by_id(ObjectId(user_id))
        if not user:
            return jsonify({"error": "User not found"}), 404

        patient = PatientRepository.find_one({"cpf_encrypted": user.cpf_encrypted})
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        # Listar associações aceitas
        associations = DoctorPatientRepository.find_all({"patient_id": patient.id})

        doctors = []
        for assoc in associations:
            if assoc.consent_status == 'accepted':
                doctor = UserRepository.find_one({"_id": assoc.doctor_id})
                doctor = {
                    "id": str(doctor.id),
                    "name": doctor.name,
                    "email": doctor.email,
                    "role": doctor.role,
                    "created_at": doctor.created_at.isoformat()
                }

                doctors.append(doctor)

        add_audit_log(
            action="List associated doctors",
            user_id=ObjectId(user_id),
            details={
                "total_doctors": len(doctors),
                "ip_address": request.remote_addr,
                "endpoint": "/patient/doctors"
            }
        )

        return jsonify(doctors), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Endpoint 30: Ver predições de um paciente associado a um médico
@app.route('/doctor/<string:doctor_id>/patient/<string:patient_id>/predictions', methods=['GET'])
@jwt_required()
@role_required(['medico'])
def get_patient_predictions(doctor_id, patient_id):

    try:
        user_id = get_jwt_identity()

        # Validar associação entre o médico e o paciente
        association = DoctorPatientRepository.find_one({"doctor_id": ObjectId(doctor_id), "patient_id": ObjectId(patient_id)})
        if not association or association.consent_status != 'accepted':
            return jsonify({"error": "Access denied due to missing association or consent"}), 403

        # Buscar predições no MongoDB para o paciente
        predictions = PredictionDataRepository.find_all({"patient_id": ObjectId(patient_id)})

        add_audit_log(
            action="Access patient predictions",
            user_id=ObjectId(user_id),
            details={
                "doctor_id": doctor_id,
                "patient_id": patient_id,
                "total_predictions": len(predictions),
                "ip_address": request.remote_addr,
                "endpoint": f"/doctor/{doctor_id}/patient/{patient_id}/predictions"
            }
        )

        return jsonify([prediction.to_dict() for prediction in predictions]), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Endpoint 31: Ver predições de todos os pacientes associados a um médico
@app.route('/doctor/<string:doctor_id>/predictions', methods=['GET'])
@jwt_required()
@role_required(['medico'])
def get_doctor_patient_predictions(doctor_id):

    try:
        user_id = get_jwt_identity()

        # Recuperar associações com consentimento aceito
        associations = DoctorPatientRepository.find_all({"doctor_id": ObjectId(doctor_id)})
        patient_ids = [assoc.patient_id for assoc in associations if assoc.consent_status == 'accepted']

        if not patient_ids:
            return jsonify({"message": "No predictions available for associated patients."}), 404

        # Buscar predições no MongoDB para os pacientes associados
        predictions = PredictionDataRepository.find_all({"patient_id": {"$in": patient_ids}})
        patients = PatientRepository.find_all({"_id": {"$in": patient_ids}})

        patient_map = {str(patient.id): patient.name for patient in patients}
        for prediction in predictions:
            prediction.patient_id = patient_map.get(str(prediction.patient_id), "Unknown")

        add_audit_log(
            action="Access all patient predictions",
            user_id=ObjectId(user_id),
            details={
                "doctor_id": doctor_id,
                "total_predictions": len(predictions),
                "total_patients": len(patient_ids),
                "ip_address": request.remote_addr,
                "endpoint": f"/doctor/{doctor_id}/predictions"
            }
        )

        return jsonify([prediction.to_dict() for prediction in predictions]), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Endpoint 32: Ver predições de todos os pacientes de maneira anonimizada (para admins)
@app.route('/admin/predictions', methods=['GET'])
@jwt_required()
@role_required(['admin'])
def get_all_predictions():
    try:

        # Buscar predições no MongoDB com campos anonimizados
        predictions = PredictionDataRepository.find_all(projection={"prediction_type": 1, "prediction_result": 1, "timestamp": 1})

        for prediction in predictions:
            prediction["_id"] = str(prediction["_id"])
            prediction["timestamp"] = prediction["timestamp"].isoformat()

        add_audit_log(
            action="Access anonymized predictions",
            user_id=ObjectId(get_jwt_identity()),
            details={
                "total_predictions": len(predictions),
                "ip_address": request.remote_addr,
                "endpoint": "/admin/predictions"
            }
        )

        return jsonify(predictions), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred while retrieving anonymized predictions: {str(e)}"}), 500

# Endpoint 33: Verificar se está autenticado
@app.route('/isAuthenticated', methods=['GET'])
@jwt_required()
@role_required(['admin', 'medico', 'paciente'])
def is_authenticated():
    try:
        user_id = get_jwt_identity()
        user_ip = request.remote_addr
        current_time = datetime.utcnow().isoformat()

        return jsonify({
            'authenticated': True,
            'user_id': user_id,
            'user_ip': user_ip,
            'timestamp': current_time
        }), 200

    except Exception as e:
        user_ip = request.remote_addr
        current_time = datetime.utcnow().isoformat()

        return jsonify({
            'authenticated': False,
            'error': str(e),
            "timestamp": current_time,
            "ip_address": user_ip
        }), 401

# Endpoint 34: Consentimento do paciente em uma requisição de associação feita por um médico
@app.route('/doctor-patient/consent', methods=['POST'])
@jwt_required()
@role_required(['paciente'])
def consent_doctor_patient():

    try:
        user_id = get_jwt_identity()
        data = request.get_json()

        doctor_patient_id = data.get('doctor_patient_id')
        consent_status = data.get('consent_status')

        user = UserRepository.get_by_id(ObjectId(user_id))

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Obter informações do paciente a partir do CPF criptografado
        patient = PatientRepository.find_one({"cpf_encrypted": user.cpf_encrypted})
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        if consent_status not in ['accepted', 'rejected']:
            return jsonify({"error": "Invalid consent status"}), 400

        doctor_patient = DoctorPatientRepository.find_one({"_id": ObjectId(doctor_patient_id)})

        if not doctor_patient:
            return jsonify({"error": "Association not found"}), 404

        # Verificar se o paciente está autorizado a alterar o consentimento
        if doctor_patient.patient_id != patient.id:
            return jsonify({"error": "You are not authorized to update this association"}), 403

        # Atualizar o consentimento ou remover associação
        if consent_status == 'rejected':
            delete_result = DoctorPatientRepository.delete_one({"_id": ObjectId(doctor_patient_id)})

            if delete_result:
                print("Consentimento removido com sucesso!")
            else:
                print("Nenhuma correspondência encontrada para remoção.")

            add_audit_log(
                action="Reject doctor-patient association",
                user_id=ObjectId(user_id),
                details={
                    "doctor_id": str(doctor_patient.doctor_id),
                    "patient_id": str(doctor_patient.patient_id),
                    "association_id": str(doctor_patient.id),
                    "consent_status": consent_status,
                    "ip_address": request.remote_addr,
                    "endpoint": "/doctor-patient/consent"
                }
            )
            return jsonify({"message": "Association rejected and deleted"}), 200

        # Atualizar o consentimento para aceito
        update_result = DoctorPatientRepository.update_one({"_id": doctor_patient.id}, {"consent_status": consent_status})

        if update_result:
            print("Consentimento atualizado com sucesso!")
        else:
            print("Associação não encontrada ou nenhum dado de consentimento foi modificado.")

        add_audit_log(
            action="Update consent",
            user_id=ObjectId(user_id),
            details={
                "doctor_id": str(doctor_patient.doctor_id),
                "patient_id": str(doctor_patient.patient_id),
                "association_id": str(doctor_patient.id),
                "consent_status": consent_status,
                "ip_address": request.remote_addr,
                "endpoint": "/doctor-patient/consent"
            }
        )

        return jsonify({"message": f"Consent status updated to {consent_status}"}), 200

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

# Endpoint 35: Listar Todas as Requisições de Associação por um médico em relação a um determinado paciente
@app.route('/doctor-patient/requests', methods=['GET'])
@jwt_required()
@role_required(['paciente'])
def list_doctor_requests():

    try:
        user_id = get_jwt_identity()
        user = UserRepository.get_by_id(ObjectId(user_id))

        if not user:
            return jsonify({"error": "User not found"}), 404

        # Obter informações do paciente a partir do CPF criptografado
        patient = PatientRepository.find_one({"cpf_encrypted": user.cpf_encrypted})
        if not patient:
            return jsonify({"error": "Patient not found"}), 404

        # Buscar todas as associações com o paciente autenticado
        associations = DoctorPatientRepository.find_all({"patient_id": patient.id})
        
        consent_requests = []
        for assoc in associations:
            doctor = UserRepository.find_one({"_id": assoc.doctor_id})
            association = {
                'id': str(assoc.id),
                'doctor_name': doctor.name if assoc.doctor_id else "Unknown",
                'doctor_id': str(assoc.doctor_id),
                'consent_status': assoc.consent_status,
                'created_at': assoc.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }

            consent_requests.append(association)

        add_audit_log(
            action="List doctor-patient requests",
            user_id=ObjectId(user_id),
            details={
                "patient_id": str(patient.id),
                "total_requests": len(consent_requests),
                "ip_address": request.remote_addr,
                "endpoint": "/doctor-patient/requests"
            }
        )

        return jsonify(consent_requests), 200

    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

if __name__ == '__main__':
    create_indexes()
    app.run(debug=True, port=5000)
