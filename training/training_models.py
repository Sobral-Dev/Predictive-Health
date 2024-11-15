from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib

# --- Modelo de Diabetes ---
# Carregar o dataset de diabetes
diabetes_data = pd.read_csv('../health-predictive-dataset/diabetes_data.csv')

# Seleção das features e do alvo para diabetes
X_diabetes = diabetes_data[['Age', 'BMI', 'HighChol', 'HighBP', 'PhysActivity', 'GenHlth', 'Smoker']]
y_diabetes = diabetes_data['Diabetes']

# Divisão em treino e teste
X_train_d, X_test_d, y_train_d, y_test_d = train_test_split(X_diabetes, y_diabetes, test_size=0.2, random_state=42)

# Treinamento
model_diabetes = RandomForestClassifier(n_estimators=50, min_samples_split=5, min_samples_leaf=1, max_features='sqrt', max_depth=10, random_state=42)
model_diabetes.fit(X_train_d, y_train_d)

# Avaliação
y_pred_d = model_diabetes.predict(X_test_d)
print("Acurácia Diabetes:", accuracy_score(y_test_d, y_pred_d))
print("Matriz de Confusão Diabetes:\n", confusion_matrix(y_test_d, y_pred_d))

# --- Modelo de Hipertensão ---
hypertension_data = pd.read_csv('../health-predictive-dataset/hypertension_data.csv')
X_hypertension = hypertension_data[['age', 'trestbps', 'chol', 'thalach', 'exang', 'oldpeak', 'cp']]
y_hypertension = hypertension_data['target']

X_train_h, X_test_h, y_train_h, y_test_h = train_test_split(X_hypertension, y_hypertension, test_size=0.2, random_state=42)

model_hypertension = RandomForestClassifier(n_estimators=50, min_samples_split=5, min_samples_leaf=2, max_features='sqrt', max_depth=None, random_state=42)
model_hypertension.fit(X_train_h, y_train_h)

y_pred_h = model_hypertension.predict(X_test_h)
print("Acurácia Hipertensão:", accuracy_score(y_test_h, y_pred_h))
print("Matriz de Confusão Hipertensão:\n", confusion_matrix(y_test_h, y_pred_h))

# --- Modelo de AVC ---
stroke_data = pd.read_csv('../health-predictive-dataset/stroke_data.csv')
X_stroke = stroke_data[['age', 'hypertension', 'heart_disease', 'avg_glucose_level', 'bmi', 'smoking_status', 'ever_married']]
y_stroke = stroke_data['stroke']

X_train_s, X_test_s, y_train_s, y_test_s = train_test_split(X_stroke, y_stroke, test_size=0.2, random_state=42)

model_stroke = RandomForestClassifier(n_estimators=100, min_samples_split=2, min_samples_leaf=1, max_features='sqrt', max_depth=None, random_state=42)
model_stroke.fit(X_train_s, y_train_s)

y_pred_s = model_stroke.predict(X_test_s)
print("Acurácia AVC:", accuracy_score(y_test_s, y_pred_s))
print("Matriz de Confusão AVC:\n", confusion_matrix(y_test_s, y_pred_s))

# Salvando os modelos treinados
joblib.dump(model_diabetes, '../models/diabetes_model.pkl')
joblib.dump(model_hypertension, '../models/hypertension_model.pkl')
joblib.dump(model_stroke, '../models/stroke_model.pkl')
