from datetime import datetime
import random
import joblib
from repositories.PatientRepository import PatientRepository
from repositories.PredictionDataRepository import PredictionDataRepository
from models.PredictionDataModel import PredictionDataModel
from repositories.UserRepository import UserRepository
from utils.calculate_age_helper import calculate_age
import pandas as pd

# Conexão com MongoDB via Repositories
patient_repo = PatientRepository()
prediction_repo = PredictionDataRepository()
user_repo = UserRepository()

# Carregar os modelos treinados
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

print("🤖 Todos os modelos preditivos foram carregados com sucesso!")

def insert_prediction_data():
    # Buscar todos os pacientes do MongoDB
    patients = patient_repo.find_all()

    count = 0
    # Gerar dados fictícios para cada paciente
    for patient in patients:
        age = calculate_age(patient.birth_date)

        for _ in range(random.randint(3, 7)):  # Criar de 3 a 7 predições por paciente
            prediction_type = random.choice(["diabetes", "hypertension", "stroke"])
            input_data = {}

            if prediction_type == "diabetes":
                input_data = {
                    "Age": age,
                    "BMI": round(random.uniform(18.5, 40.0), 2),
                    "HighChol": random.randint(0, 1),
                    "HighBP": random.randint(0, 1),
                    "PhysActivity": random.randint(0, 1),
                    "GenHlth": random.randint(1, 5),
                    "Smoker": random.randint(0, 1)
                }
                model = diabetes_model
                required_fields = ['Age', 'BMI', 'HighChol', 'HighBP', 'PhysActivity', 'GenHlth', 'Smoker']

            elif prediction_type == "hypertension":
                input_data = {
                    "age": age,
                    "trestbps": random.randint(90, 200),
                    "chol": random.randint(100, 300),
                    "thalach": random.randint(60, 180),
                    "exang": random.randint(0, 1),
                    "oldpeak": round(random.uniform(0.0, 6.0), 2),
                    "cp": random.randint(0, 3)
                }
                model = hypertension_model
                required_fields = ['age', 'trestbps', 'chol', 'thalach', 'exang', 'oldpeak', 'cp']

            elif prediction_type == "stroke":
                input_data = {
                    "age": age,
                    "hypertension": random.randint(0, 1),
                    "heart_disease": random.randint(0, 1),
                    "avg_glucose_level": round(random.uniform(70.0, 200.0), 2),
                    "bmi": round(random.uniform(18.5, 40.0), 2),
                    "smoking_status": random.randint(0, 2),
                    "ever_married": random.randint(0, 1)
                }
                model = stroke_model
                required_fields = ['age', 'hypertension', 'heart_disease', 'avg_glucose_level', 'bmi', 'smoking_status', 'ever_married']

            # Garantir que todos os campos necessários estão presentes
            missing_fields = [field for field in required_fields if field not in input_data]
            if missing_fields:
                print(f"⚠️ Campos ausentes para {prediction_type}: {missing_fields}")

            # Formatar input para predição
            model_input = pd.DataFrame([input_data], columns=required_fields)
            prediction = model.predict(model_input)
            probability = model.predict_proba(model_input)[0][1]

            prediction_result = {
                "risk": int(prediction[0]),
                "probability": round(probability, 2)
            }

            user_id = user_repo.find_one({"cpf_encrypted": patient.cpf_encrypted}).id

            # Criar objeto de predição e salvar no MongoDB
            prediction_register = PredictionDataModel(
                user_id=user_id,  # Associando paciente ao usuário
                patient_id=patient.id,
                prediction_type=prediction_type,
                input_data=input_data,
                prediction_result=prediction_result,
                timestamp=datetime.utcnow()
            )

            prediction_repo.insert_one(prediction_register)

            count += 1

            print(f"• {count} predições fictícias inseridas...")

    print("✅ Dados fictícios de predições inseridos com sucesso!")

if __name__ == "__main__":
    insert_prediction_data()