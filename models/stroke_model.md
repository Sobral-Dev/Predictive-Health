# Documentação do Modelo de Predição de AVC (Acidente Vascular Cerebral)

Este documento detalha as features utilizadas para o treinamento do modelo de predição de AVC, incluindo uma explicação de cada feature, unidade de medida, tipo de dado e seu impacto na probabilidade de ocorrência de um AVC. A inclusão de cada feature é fundamentada na literatura médica e em sua relação conhecida com os fatores de risco para AVC.

---

## 1. Descrição Geral do Modelo

O modelo de predição de AVC é baseado em um classificador de floresta aleatória (Random Forest Classifier) e utiliza múltiplas features relacionadas ao perfil de saúde e histórico do paciente para prever o risco de um AVC.

### Objetivo do Modelo
O objetivo do modelo é calcular o risco e a probabilidade de AVC, ajudando na identificação precoce de indivíduos com maior predisposição a essa condição.

---

## 2. Descrição das Features

| Feature             | Descrição                                                                                     | Unidade         | Tipo de Dado | Impacto na Predição do Modelo |
|---------------------|-----------------------------------------------------------------------------------------------|-----------------|--------------|--------------------------------|
| **age**             | Idade do paciente, um dos principais fatores de risco para AVC.                               | Anos            | Numérico     | Altamente relevante; o risco de AVC aumenta significativamente com a idade, especialmente após os 55 anos. |
| **hypertension**    | Indicador de hipertensão, condição comumente associada a AVC devido ao aumento da pressão arterial. | Booleano (0/1)  | Categórico   | Fundamental; a hipertensão é um dos fatores de risco mais importantes para AVC. |
| **heart_disease**   | Indicador de presença de doença cardíaca, que pode predispor o paciente a um AVC.             | Booleano (0/1)  | Categórico   | Relevante; doenças cardíacas, como fibrilação atrial, aumentam o risco de coágulos, elevando a chance de AVC. |
| **avg_glucose_level** | Nível médio de glicose no sangue, indicador de condições como diabetes, que aumenta o risco de AVC. | mg/dL           | Numérico     | Importante; níveis elevados de glicose estão associados ao risco aumentado de AVC, especialmente em diabéticos. |
| **bmi**             | Índice de Massa Corporal, reflete obesidade, que é fator de risco para diversas condições cardiovasculares. | kg/m²           | Numérico     | Moderadamente relevante; obesidade contribui para hipertensão e diabetes, que aumentam o risco de AVC. |
| **smoking_status**  | Status de fumante, onde o tabagismo é um dos fatores de risco modificáveis para AVC.          | Categórico      | Categórico   | Relevante; o tabagismo aumenta o risco de coágulos sanguíneos e estreitamento das artérias, elevando o risco de AVC. |
| **ever_married**    | Indicador de estado civil, que pode refletir fatores psicológicos e comportamentais relacionados à saúde. | Booleano (0/1)  | Categórico   | Relevância moderada; alguns estudos sugerem que fatores sociais podem influenciar a saúde geral, impactando o risco de AVC. |

---

## 3. Impacto de Cada Feature na Predição de AVC

Abaixo está o impacto esperado de cada feature no modelo de predição de AVC:

1. **age**:
   - **Impacto no Risco**: Com o envelhecimento, as artérias tendem a endurecer e aumentar a pressão, elevando o risco de AVC.
   - **Impacto na Probabilidade**: Um aumento na idade aumenta significativamente a probabilidade de AVC, especialmente após os 55 anos.

2. **hypertension (Hipertensão)**:
   - **Impacto no Risco**: A hipertensão é o principal fator de risco para AVC, pois exerce pressão sobre as artérias, facilitando a ruptura e obstrução dos vasos.
   - **Impacto na Probabilidade**: A presença de hipertensão aumenta substancialmente a probabilidade predita de AVC no modelo.

3. **heart_disease (Doença Cardíaca)**:
   - **Impacto no Risco**: Doenças cardíacas, como arritmias e fibrilação atrial, podem causar a formação de coágulos, que podem se deslocar e causar um AVC.
   - **Impacto na Probabilidade**: A presença de doenças cardíacas eleva a probabilidade de AVC, devido ao risco de embolia cerebral.

4. **avg_glucose_level (Nível Médio de Glicose)**:
   - **Impacto no Risco**: Níveis altos de glicose, indicativos de diabetes, estão associados ao risco de AVC por danos vasculares causados por hiperglicemia.
   - **Impacto na Probabilidade**: Um nível médio elevado de glicose aumenta a probabilidade de AVC, especialmente em indivíduos diabéticos.

5. **bmi (Índice de Massa Corporal)**:
   - **Impacto no Risco**: A obesidade contribui para o desenvolvimento de hipertensão e diabetes, ambos fatores de risco para AVC.
   - **Impacto na Probabilidade**: Um BMI elevado aumenta moderadamente a probabilidade predita de AVC.

6. **smoking_status (Status de Fumante)**:
   - **Impacto no Risco**: O tabagismo causa inflamação e estreitamento dos vasos sanguíneos, além de promover a formação de coágulos.
   - **Impacto na Probabilidade**: Fumantes apresentam uma probabilidade predita mais alta de AVC devido ao impacto do tabagismo na saúde cardiovascular.

7. **ever_married (Estado Civil)**:
   - **Impacto no Risco**: O estado civil pode refletir fatores socioeconômicos e psicológicos, influenciando comportamentos e, indiretamente, o risco de AVC.
   - **Impacto na Probabilidade**: Indivíduos que já foram casados podem apresentar uma leve variação na probabilidade predita, embora esta variável seja de relevância menor.

---

## 4. Justificativa para Inclusão das Features no Modelo de AVC

- **age**, **hypertension** e **heart_disease** são preditores diretos e importantes para AVC, pois contribuem significativamente para o desenvolvimento de condições que levam ao evento cerebrovascular.
- **avg_glucose_level** e **bmi** foram incluídos devido à sua associação com a saúde metabólica, que afeta a saúde vascular e o risco de AVC.
- **smoking_status** é um fator de risco bem documentado para AVC e, portanto, foi incluído para capturar o impacto do tabagismo no risco vascular.
- **ever_married** foi incluído para capturar potenciais impactos indiretos do estado civil e fatores psicossociais na saúde.

Essas features foram selecionadas para capturar tanto os fatores de risco diretos quanto indiretos de AVC, e o modelo foi projetado para fornecer uma predição precisa e confiável da probabilidade de ocorrência de um AVC.