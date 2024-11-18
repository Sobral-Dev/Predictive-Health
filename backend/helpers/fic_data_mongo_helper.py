from pymongo import MongoClient
from datetime import datetime
import random
import psycopg2
from calculate_age_helper import calculate_age
import joblib

# Conexão com o PostgreSQL para acessar dados dos pacientes
pg_conn = psycopg2.connect(
    host="localhost",
    database="PatientSystem",
    user="postgre",
    password="853211"
)
pg_cursor = pg_conn.cursor()

# Query para obter os dados dos pacientes
pg_cursor.execute("SELECT id, birth_date FROM \"Patient\";")
patients = pg_cursor.fetchall()

# Configuração MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["PredictiveHealth"]
predictions = db["PredictionData"]

# Carregando os modelos
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

print("All predictive models loaded successfully")

# Gerar dados fictícios para cada paciente
for patient_id, birth_date in patients:
    age = calculate_age(birth_date)

    for _ in range(random.randint(3, 7)):  # 3 a 7 predições por paciente
        prediction_type = random.choice(["diabetes", "hypertension", "stroke"])
        input_data = {}

        if prediction_type == "diabetes":

            required_fields = ['Age', 'BMI', 'HighChol', 'HighBP', 'PhysActivity', 'GenHlth', 'Smoker']
            missing_fields = [field for field in required_fields if field not in input_data]

            if missing_fields:
                print(f"Might Required Fields not totally provided: {", ".join(missing_fields)}")

            input_data = {
                "Age": age,
                "BMI": round(random.uniform(18.5, 40.0), 2),  
                "HighChol": random.randint(0, 1),  
                "HighBP": random.randint(0, 1),  
                "PhysActivity": random.randint(0, 1), 
                "GenHlth": random.randint(1, 5),  
                "Smoker": random.randint(0, 1)  
            }
        elif prediction_type == "hypertension":

            required_fields = ['age', 'trestbps', 'chol', 'thalach', 'exang', 'oldpeak', 'cp']
            missing_fields = [field for field in required_fields if field not in input_data]

            if missing_fields:
                print(f"Might Required Fields not totally provided: {", ".join(missing_fields)}")

            input_data = {
                "age": age,
                "trestbps": random.randint(90, 200),  
                "chol": random.randint(100, 300), 
                "thalach": random.randint(60, 180),  
                "exang": random.randint(0, 1), 
                "oldpeak": round(random.uniform(0.0, 6.0), 2), 
                "cp": random.randint(0, 3) 
            }
        elif prediction_type == "stroke":

            required_fields = ['age', 'hypertension', 'heart_disease', 'avg_glucose_level', 'bmi', 'smoking_status', 'ever_married']
            missing_fields = [field for field in required_fields if field not in input_data]

            if missing_fields:
                print(f"Might Required Fields not totally provided: {", ".join(missing_fields)}")

            input_data = {
                "age": age,
                "hypertension": random.randint(0, 1),  
                "heart_disease": random.randint(0, 1),  
                "avg_glucose_level": round(random.uniform(70.0, 200.0), 2), 
                "bmi": round(random.uniform(18.5, 40.0), 2),  
                "smoking_status": random.randint(0, 2),  
                "ever_married": random.randint(0, 1), 
            }

        input_data = [[input_data[field] for field in required_fields]]

        if prediction_type == "diabetes":
            prediction = diabetes_model.predict(input_data)
            probability = diabetes_model.predict_proba(input_data)[0][1]
        elif prediction_type == "hypertension":
            prediction = hypertension_model.predict(input_data)
            probability = hypertension_model.predict_proba(input_data)[0][1]
        elif prediction_type == "stroke":
            prediction = stroke_model.predict(input_data)
            probability = stroke_model.predict_proba(input_data)[0][1]

        prediction_result = {
            "risk": int(prediction[0]),
            "probability": round(probability, 2)
        }

        prediction_register = {
            "user_id": patient_id,
            "prediction_type": prediction_type,
            "input_data": input_data,
            "prediction_result": prediction_result,
            "timestamp": datetime.utcnow()
        }

        predictions.insert_one(prediction_register)

print("Fictitious prediction data inserted successfully.")

# Fechar conexões
pg_cursor.close()
pg_conn.close()
