from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
import pandas as pd
import joblib

# Recarregar o dataset de diabetes
diabetes_data = pd.read_csv(r'./health-predictive-dataset/diabetes_data.csv')

# Separação das features (X) e do alvo (y)
X = diabetes_data.drop(columns=['Diabetes'])
y = diabetes_data['Diabetes']

# Divisão em dados de treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinamento do modelo Random Forest com os melhores hiperparâmetros encontrados
best_model_random = RandomForestClassifier(
    n_estimators=50,
    min_samples_split=5,
    min_samples_leaf=1,
    max_features='sqrt',
    max_depth=10,
    random_state=42
)

# Ajuste do modelo com os dados de treino
best_model_random.fit(X_train, y_train)

# Predição nos dados de teste
y_pred_best_random = best_model_random.predict(X_test)

# Avaliação do modelo otimizado
best_accuracy_random = accuracy_score(y_test, y_pred_best_random)
best_conf_matrix_random = confusion_matrix(y_test, y_pred_best_random)

# Resultados
print(f"Acurácia do Melhor Modelo: {best_accuracy_random}")
print(f"Matriz de Confusão do Melhor Modelo:\n{best_conf_matrix_random}")

# Carregar o dataset de hipertensão
hypertension_data = pd.read_csv(r'./health-predictive-dataset/hypertension_data.csv')

# Tratar valores nulos na coluna 'sex' com a moda
hypertension_data['sex'].fillna(hypertension_data['sex'].mode()[0], inplace=True)

# Separação das features (X) e do alvo (y)
X_hyper = hypertension_data.drop(columns=['target'])
y_hyper = hypertension_data['target']

# Divisão em dados de treino e teste
X_train_hyper, X_test_hyper, y_train_hyper, y_test_hyper = train_test_split(X_hyper, y_hyper, test_size=0.2, random_state=42)

# Treinamento do modelo Random Forest com os melhores hiperparâmetros encontrados
best_model_hyper = RandomForestClassifier(
    n_estimators=50,
    min_samples_split=5,
    min_samples_leaf=2,
    max_features='sqrt',
    max_depth=None,
    random_state=42
)

# Ajuste do modelo com os dados de treino
best_model_hyper.fit(X_train_hyper, y_train_hyper)

# Predição nos dados de teste
y_pred_best_hyper = best_model_hyper.predict(X_test_hyper)

# Avaliação do modelo otimizado
best_accuracy_hyper = accuracy_score(y_test_hyper, y_pred_best_hyper)
best_conf_matrix_hyper = confusion_matrix(y_test_hyper, y_pred_best_hyper)

# Resultados
print(f"Acurácia do Melhor Modelo: {best_accuracy_hyper}")
print(f"Matriz de Confusão do Melhor Modelo:\n{best_conf_matrix_hyper}")

# Carregar o dataset de AVC
stroke_data = pd.read_csv(r'./health-predictive-dataset/stroke_data.csv')

# Imputação de valores faltantes usando a média para colunas numéricas
imputer = SimpleImputer(strategy='mean')
X_stroke = stroke_data.drop(columns=['stroke'])  # Ajuste 'stroke' para o nome correto da coluna de alvo em seu dataset
X_stroke = imputer.fit_transform(X_stroke)

# Separação do alvo (y)
y_stroke = stroke_data['stroke']

# Divisão em dados de treino e teste
X_train_stroke, X_test_stroke, y_train_stroke, y_test_stroke = train_test_split(X_stroke, y_stroke, test_size=0.2, random_state=42)

# Treinamento do modelo Random Forest com os melhores hiperparâmetros encontrados
best_model_stroke = RandomForestClassifier(
    n_estimators=100,
    min_samples_split=2,
    min_samples_leaf=1,
    max_features='sqrt',
    max_depth=None,
    random_state=42
)

# Ajuste do modelo com os dados de treino
best_model_stroke.fit(X_train_stroke, y_train_stroke)

# Predição nos dados de teste
y_pred_best_stroke = best_model_stroke.predict(X_test_stroke)

# Avaliação do modelo otimizado
best_accuracy_stroke = accuracy_score(y_test_stroke, y_pred_best_stroke)
best_conf_matrix_stroke = confusion_matrix(y_test_stroke, y_pred_best_stroke)

# Resultados
print(f"Acurácia do Melhor Modelo: {best_accuracy_stroke}")
print(f"Matriz de Confusão do Melhor Modelo:\n{best_conf_matrix_stroke}")

# Caminho para salvar os modelos
model_path_diabetes = r'./models/diabetes_model.pkl'
model_path_hypertension = r'./models/hypertension_model.pkl'
model_path_stroke = r'./models/stroke_model.pkl'

# Salvando o modelo de Diabetes
joblib.dump(best_model_random, model_path_diabetes)
print(f"Modelo de Diabetes salvo em: {model_path_diabetes}")

# Salvando o modelo de Hipertensão
joblib.dump(best_model_hyper, model_path_hypertension)
print(f"Modelo de Hipertensão salvo em: {model_path_hypertension}")

# Salvando o modelo de AVC
joblib.dump(best_model_stroke, model_path_stroke)
print(f"Modelo de AVC salvo em: {model_path_stroke}")