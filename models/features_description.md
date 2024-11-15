# Estrutura do Formulário com Tooltip e Detalhes para os Inputs

## 1. Modelo de Predição de Diabetes

### Campos e Descrições:

#### 1. **Idade (Age)**
   - **Tooltip (Português)**: "Idade do paciente, fator de risco importante para o desenvolvimento de diabetes tipo 2. A idade avançada está associada ao aumento da resistência à insulina."
   - **Tooltip (Inglês)**: "Patient's age, a significant risk factor for type 2 diabetes. Advanced age is associated with increased insulin resistance."
   - **Tipo**: `number`
   - **Unidade**: `anos`

#### 2. **Índice de Massa Corporal (BMI)**
   - **Tooltip (Português)**: "Índice de Massa Corporal, calculado a partir da altura e peso. O sobrepeso e a obesidade são fatores de risco críticos para o diabetes."
   - **Tooltip (Inglês)**: "Body Mass Index, calculated from height and weight. Overweight and obesity are critical risk factors for diabetes."
   - **Tipo**: `number`
   - **Unidade**: `kg/m²`

#### 3. **Colesterol Alto (HighChol)**
   - **Tooltip (Português)**: "Indica se o paciente possui nível elevado de colesterol. Colesterol alto está associado ao risco cardiovascular e ao desenvolvimento de diabetes."
   - **Tooltip (Inglês)**: "Indicates if the patient has high cholesterol levels. High cholesterol is associated with cardiovascular risk and diabetes development."
   - **Tipo**: `checkbox` (0 para “não” e 1 para “sim”)

#### 4. **Pressão Alta (HighBP)**
   - **Tooltip (Português)**: "Indica se o paciente possui hipertensão. A pressão alta contribui para resistência à insulina e é fator de risco para diabetes."
   - **Tooltip (Inglês)**: "Indicates if the patient has hypertension. High blood pressure contributes to insulin resistance and is a risk factor for diabetes."
   - **Tipo**: `checkbox`

#### 5. **Atividade Física (PhysActivity)**
   - **Tooltip (Português)**: "Indica se o paciente realiza atividades físicas regularmente. A atividade física reduz o risco de diabetes ao melhorar a sensibilidade à insulina."
   - **Tooltip (Inglês)**: "Indicates if the patient engages in regular physical activity. Physical activity reduces diabetes risk by improving insulin sensitivity."
   - **Tipo**: `checkbox`

#### 6. **Saúde Geral (GenHlth)**
   - **Tooltip (Português)**: "Avaliação do estado geral de saúde, com base em uma escala de 1 a 5. Um estado de saúde precário aumenta o risco de diabetes."
   - **Tooltip (Inglês)**: "Self-reported general health rating, on a scale from 1 to 5. Poor general health increases diabetes risk."
   - **Tipo**: `number` (1 a 5)

#### 7. **Fumante (Smoker)**
   - **Tooltip (Português)**: "Indica se o paciente fuma. O tabagismo está associado ao aumento da resistência à insulina, elevando o risco de diabetes."
   - **Tooltip (Inglês)**: "Indicates if the patient smokes. Smoking is associated with increased insulin resistance, raising diabetes risk."
   - **Tipo**: `checkbox`

---

## 2. Modelo de Predição de Hipertensão

### Campos e Descrições:

#### 1. **Idade (age)**
   - **Tooltip (Português)**: "Idade do paciente, associada ao endurecimento arterial e aumento da pressão arterial ao longo dos anos."
   - **Tooltip (Inglês)**: "Patient's age, associated with arterial stiffening and increased blood pressure over the years."
   - **Tipo**: `number`
   - **Unidade**: `anos`

#### 2. **Pressão Arterial em Repouso (trestbps)**
   - **Tooltip (Português)**: "Pressão arterial medida em repouso. Indicador direto da presença ou risco de hipertensão."
   - **Tooltip (Inglês)**: "Resting blood pressure, measured while at rest. A direct indicator of hypertension risk."
   - **Tipo**: `number`
   - **Unidade**: `mm Hg`

#### 3. **Colesterol (chol)**
   - **Tooltip (Português)**: "Nível de colesterol no sangue. O colesterol alto pode contribuir para o aumento da pressão arterial e doenças cardiovasculares."
   - **Tooltip (Inglês)**: "Cholesterol level in the blood. High cholesterol can contribute to increased blood pressure and cardiovascular diseases."
   - **Tipo**: `number`
   - **Unidade**: `mg/dL`

#### 4. **Frequência Cardíaca Máxima (thalach)**
   - **Tooltip (Português)**: "Frequência cardíaca máxima atingida, que indica o funcionamento cardiovascular."
   - **Tooltip (Inglês)**: "Maximum heart rate achieved, which indicates cardiovascular functioning."
   - **Tipo**: `number`
   - **Unidade**: `bpm`

#### 5. **Angina Induzida por Exercício (exang)**
   - **Tooltip (Português)**: "Indica se o paciente apresenta dor no peito (angina) ao realizar exercícios físicos."
   - **Tooltip (Inglês)**: "Indicates if the patient experiences chest pain (angina) during physical exertion."
   - **Tipo**: `checkbox`

#### 6. **Depressão ST (oldpeak)**
   - **Tooltip (Português)**: "Medida de depressão do segmento ST, uma anormalidade eletrocardiográfica indicativa de problemas cardíacos."
   - **Tooltip (Inglês)**: "ST depression measurement, an ECG abnormality indicative of heart issues."
   - **Tipo**: `number`
   - **Unidade**: `mm`

#### 7. **Tipo de Dor no Peito (cp)**
   - **Tooltip (Português)**: "Tipo de dor no peito que o paciente sente, de acordo com uma escala de 1 a 4."
   - **Tooltip (Inglês)**: "Type of chest pain experienced by the patient, based on a scale of 1 to 4."
   - **Tipo**: `number` (1 a 4)

---

## 3. Modelo de Predição de AVC

### Campos e Descrições:

#### 1. **Idade (age)**
   - **Tooltip (Português)**: "Idade do paciente. O risco de AVC aumenta com o envelhecimento devido ao endurecimento e obstrução das artérias."
   - **Tooltip (Inglês)**: "Patient's age. The risk of stroke increases with age due to arterial stiffening and blockages."
   - **Tipo**: `number`
   - **Unidade**: `anos`

#### 2. **Hipertensão (hypertension)**
   - **Tooltip (Português)**: "Indica se o paciente possui hipertensão, um dos maiores fatores de risco para AVC."
   - **Tooltip (Inglês)**: "Indicates if the patient has hypertension, one of the major risk factors for stroke."
   - **Tipo**: `checkbox`

#### 3. **Doença Cardíaca (heart_disease)**
   - **Tooltip (Português)**: "Indica se o paciente tem doenças cardíacas, o que aumenta o risco de AVC."
   - **Tooltip (Inglês)**: "Indicates if the patient has heart disease, which increases the risk of stroke."
   - **Tipo**: `checkbox`

#### 4. **Nível Médio de Glicose (avg_glucose_level)**
   - **Tooltip (Português)**: "Nível médio de glicose no sangue. A diabetes aumenta o risco de AVC."
   - **Tooltip (Inglês)**: "Average blood glucose level. Diabetes increases the risk of stroke."
   - **Tipo**: `number`
   - **Unidade**: `mg/dL`

#### 5. **Índice de Massa Corporal (BMI)**
   - **Tooltip (Português)**: "Índice de Massa Corporal. A obesidade é um fator de risco importante para AVC."
   - **Tooltip (Inglês)**: "Body Mass Index. Obesity is an important risk factor for stroke."
   - **Tipo**: `number`
   - **Unidade**: `kg/m²`

#### 6. **Status de Fumante (smoking_status)**
   - **Tooltip (Português)**: "Indica se o paciente fuma, hábito que aumenta o risco de problemas cardiovasculares e AVC."
   - **Tooltip (Inglês)**: "Indicates if the patient sm

okes, a habit that increases cardiovascular issues and stroke risk."
   - **Tipo**: `text` (ou `select`, se houver valores específicos)

#### 7. **Já foi Casado(a) (ever_married)**
   - **Tooltip (Português)**: "Indica se o paciente já foi casado(a). Estudos associam fatores socioeconômicos com a saúde cardiovascular."
   - **Tooltip (Inglês)**: "Indicates if the patient has ever been married. Socioeconomic factors have been associated with cardiovascular health."
   - **Tipo**: `checkbox`