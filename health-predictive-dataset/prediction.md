# Documentação Completa da Funcionalidade de Predição de Saúde

## Objetivo
O objetivo desta funcionalidade é proporcionar uma análise preditiva que possa identificar riscos de saúde, como diabetes, hipertensão e AVC, utilizando modelos de inteligência artificial. A ideia é fornecer suporte adicional aos profissionais de saúde, ajudando-os a tomar decisões informadas e prevenir condições críticas de saúde nos pacientes.

---

## Justificativa
A previsão de doenças como diabetes, hipertensão e AVC é essencial na prevenção e na gestão da saúde dos pacientes. Utilizar modelos de IA treinados oferece uma abordagem baseada em dados, que considera múltiplos fatores de risco e suas interações complexas. A funcionalidade é particularmente útil para:
- **Prevenção Proativa:** Identificar precocemente os riscos de saúde.
- **Gerenciamento de Casos:** Focar em pacientes com maior risco.
- **Tomada de Decisões Baseada em Dados:** Ajudar profissionais de saúde a priorizar cuidados.

---

## Plano de Ação e Modelos de IA

### 1. **Modelo de Predição de Diabetes**
- **Modelo Utilizado:** RandomForest Classifier
- **Atributos Importantes:** Níveis de glicose, pressão arterial, IMC, idade, e histórico médico.
- **Arquivo:** `diabetes_model.pkl`
- **Endpoint Backend:** `POST /predict/diabetes`
- **Lógica de Backend:**
  - Os dados do paciente são recebidos via requisição POST.
  - A entrada é processada e passada ao modelo de IA.
  - O modelo retorna a predição e a probabilidade de risco.
- **Relacionamento com o Banco de Dados:**
  - **Tabela:** `patients` – Dados demográficos e médicos.
  - **Tabela:** `predictions` – Registra o tipo de predição, o risco, e a data.

### 2. **Modelo de Predição de Hipertensão**
- **Modelo Utilizado:** RandomForest Classifier
- **Atributos Importantes:** Idade, histórico de saúde, IMC, atividade física.
- **Arquivo:** `hypertension_model.pkl`
- **Endpoint Backend:** `POST /predict/hypertension`
- **Lógica de Backend:**
  - Recebe dados do paciente e valida a entrada.
  - O modelo analisa os dados e retorna a decisão e o score de risco.
- **Relacionamento com o Banco de Dados:**
  - **Tabela:** `patients` – Contém os atributos necessários.
  - **Tabela:** `predictions` – Armazena o resultado e detalhes da predição.

### 3. **Modelo de Predição de AVC**
- **Modelo Utilizado:** RandomForest Classifier
- **Atributos Importantes:** Idade, histórico de tabagismo, níveis de colesterol, entre outros.
- **Arquivo:** `stroke_model.pkl`
- **Endpoint Backend:** `POST /predict/stroke`
- **Lógica de Backend:**
  - Valida e processa os dados do paciente.
  - Passa os dados ao modelo, que retorna a probabilidade de risco.
- **Relacionamento com o Banco de Dados:**
  - **Tabela:** `patients` – Dados necessários para a análise.
  - **Tabela:** `predictions` – Registra os detalhes da análise.

---

## Configuração no Backend (Flask)

### Arquitetura e Lógica
1. **Carregamento dos Modelos:**
   - Os modelos de IA são carregados a partir de arquivos `.pkl` usando a biblioteca `pickle`.
   - Exemplos:
     ```python
     import pickle
     from flask import Flask, request, jsonify

     # Carregando o modelo de diabetes
     with open('diabetes_model.pkl', 'rb') as file:
         diabetes_model = pickle.load(file)
     ```

2. **Endpoints de Predição:**
   - Cada condição de saúde possui um endpoint separado, que processa os dados e retorna a predição.
   - Exemplo para Diabetes:
     ```python
     @app.route('/predict/diabetes', methods=['POST'])
     def predict_diabetes():
         data = request.get_json()
         # Processamento dos dados...
         prediction = diabetes_model.predict([data['features']])
         response = {
             'risk_score': prediction[0],
             'details': 'Probabilidade de risco de diabetes'
         }
         return jsonify(response)
     ```

3. **Segurança e Validação:**
   - Todas as requisições são autenticadas via JWT.
   - Validações são realizadas para garantir a integridade dos dados antes de serem passados ao modelo.

---

## Implementação no Frontend (Vue.js)

### Páginas Principais e Métodos
1. **HealthPrediction.vue**
   - **Função Principal:** Enviar dados para os endpoints do backend e exibir o resultado.
   - **Método Exemplo:**
     ```javascript
     async makePrediction() {
       try {
         const response = await axios.post('http://localhost:5000/predict/diabetes', this.patientData);
         this.predictionResult = response.data;
       } catch (error) {
         console.error('Erro na predição:', error);
       }
     }
     ```

2. **PatientDetails.vue**
   - **Função Principal:** Exibir detalhes do paciente, incluindo as predições.
   - A página mostra um histórico das predições associadas ao paciente.

3. **UserProfile.vue**
   - **Função Principal:** Permitir que o usuário visualize suas informações, incluindo riscos de saúde baseados em predições.

---

## Tabelas do Banco de Dados PostgreSQL

### 1. **Tabela `patients`**
- **Colunas Relevantes:**
  - `id`: Identificador único do paciente.
  - `age`: Idade do paciente.
  - `bmi`: Índice de Massa Corporal.
  - `smoking_status`: Status de tabagismo.
  - **Atributos Utilizados nas Predições:** Todas as informações demográficas e de saúde relevantes.

### 2. **Tabela `predictions`**
- **Colunas Relevantes:**
  - `id`: Identificador único da predição.
  - `patient_id`: Chave estrangeira para a tabela `patients`.
  - `prediction_type`: Tipo de predição (diabetes, hipertensão, AVC).
  - `risk_score`: Score de risco retornado pelo modelo.
  - `created_at`: Data e hora da predição.
- **Associação:** `patient_id` relaciona-se diretamente com a tabela `patients`.

### 3. **Tabela `audit_logs`**
- **Propósito:** Registrar atividades relacionadas às predições para garantir conformidade com a LGPD.
- **Colunas Relevantes:**
  - `id`: Identificador único do log.
  - `action`: Descrição da ação realizada.
  - `timestamp`: Data e hora do evento.
  - `user_id`: Identificador do usuário que realizou a ação.

---

## Considerações Finais
Esta documentação fornece uma visão abrangente da funcionalidade de predição na aplicação, desde a configuração no backend até o acesso no frontend e como os dados são organizados no banco de dados PostgreSQL. A abordagem utilizada combina IA, segurança de dados, e boas práticas de engenharia de software, garantindo uma experiência robusta e eficaz para usuários e profissionais de saúde.