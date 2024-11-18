<template>
  <div class="health-prediction">
    <h1 class="page-title">Health Prediction</h1>

    <section class="prediction-section">

      <button class="choose-language" @click.prevent="english = !english"><i class="fa-solid fa-language">{{ !english ? 'PT-Br' : 'EN' }}</i></button>
      
      <!-- Select para escolher o tipo de predição -->
      <label for="predictionType">Escolha o tipo de predição: </label>
      <select v-model="selectedPrediction" @change="resetForm">
        <option disabled value="">Selecione uma condição...</option>
        <option value="diabetes">Diabetes</option>
        <option value="hypertension">Hipertensão</option>
        <option value="stroke">AVC</option>
      </select>

      <!-- Formulário para predição de Diabetes -->
      <form v-if="selectedPrediction === 'diabetes' && this.gd.user_role === 'paciente'" @submit.prevent="predictDiabetes">
        <label>
          Índice de Massa Corporal (IMC): <input v-model="formData.BMI" type="number" required />
            <span class="tooltip">i
              <span v-if="!english" class="tooltiptext">Índice de Massa Corporal, calculado a partir da altura e peso. O sobrepeso e a obesidade são fatores de risco críticos para o diabetes.</span>
              <span v-else class="tooltiptext">Body Mass Index, calculated from height and weight. Overweight and obesity are critical risk factors for diabetes.</span>
            </span>
        </label>
        <label>
          Colesterol Alto: <input v-model="formData.HighChol" type="checkbox" />
            <span class="tooltip">i
              <span v-if="!english" class="tooltiptext">Indica se o paciente possui nível elevado de colesterol. Colesterol alto está associado ao risco cardiovascular e ao desenvolvimento de diabetes.</span>
              <span v-else class="tooltiptext">Indicates if the patient has high cholesterol levels. High cholesterol is associated with cardiovascular risk and diabetes development.</span>
            </span>
          </label>
        <label>
          Pressão Alta: <input v-model="formData.HighBP" type="checkbox" />
            <span class="tooltip">i
              <span v-if="!english" class="tooltiptext">Indica se o paciente possui hipertensão. A pressão alta contribui para resistência à insulina e é fator de risco para diabetes.</span>
              <span v-else class="tooltiptext">Indicates if the patient has hypertension. High blood pressure contributes to insulin resistance and is a risk factor for diabetes.</span>
            </span>
        </label>
        <label>
          Atividade Física: <input v-model="formData.PhysActivity" type="checkbox" />
            <span class="tooltip">i
              <span v-if="!english" class="tooltiptext">Indica se o paciente realiza atividades físicas regularmente. A atividade física reduz o risco de diabetes ao melhorar a sensibilidade à insulina.</span>
              <span v-else class="tooltiptext">Indicates if the patient engages in regular physical activity. Physical activity reduces diabetes risk by improving insulin sensitivity.</span>
            </span>
        </label>
        <label>
          Saúde Geral: <input v-model="formData.GenHlth" type="number" min="1" max="5" required />
            <span class="tooltip">i
              <span v-if="!english" class="tooltiptext">Avaliação do estado geral de saúde, com base em uma escala de 1 a 5. Um estado de saúde precário aumenta o risco de diabetes.</span>
              <span v-else class="tooltiptext">Self-reported general health rating, on a scale from 1 to 5. Poor general health increases diabetes risk.</span>
            </span>
          </label>
        <label>
          Fumante: <input v-model="formData.Smoker" type="checkbox" />
            <span class="tooltip">i
              <span v-if="!english" class="tooltiptext">Indica se o paciente fuma. O tabagismo está associado ao aumento da resistência à insulina, elevando o risco de diabetes.</span>
              <span v-else class="tooltiptext">Indicates if the patient smokes. Smoking is associated with increased insulin resistance, raising diabetes risk.</span>
            </span>
          </label>
        <button type="submit" :disabled="!hasConsent">Prever Diabetes</button>
      </form>

      <!-- Formulário para predição de Hipertensão -->
      <form v-if="selectedPrediction === 'hypertension' && this.gd.user_role === 'paciente'" @submit.prevent="predictHypertension">
        <label>
          Pressão Arterial em Repouso (trestbps): <input v-model="formData.trestbps" type="number" required />
            <span class="tooltip">i
              <span v-if="!english" class="tooltiptext">Pressão arterial medida em repouso. Indicador direto da presença ou risco de hipertensão.</span>
              <span v-else class="tooltiptext">Resting blood pressure, measured while at rest. A direct indicator of hypertension risk.</span>
            </span>
        </label>
        <label>
          Colesterol (chol): <input v-model="formData.chol" type="number" required />
            <span class="tooltip">i
              <span v-if="!english" class="tooltiptext">Nível de colesterol no sangue. O colesterol alto pode contribuir para o aumento da pressão arterial e doenças cardiovasculares.</span>
              <span v-else class="tooltiptext">Cholesterol level in the blood. High cholesterol can contribute to increased blood pressure and cardiovascular diseases.</span>
            </span>
        </label>
        <label>
          Frequência Cardíaca Máxima (thalach): <input v-model="formData.thalach" type="number" required />
            <span class="tooltip">i
              <span v-if="!english" class="tooltiptext">Frequência cardíaca máxima atingida, que indica o funcionamento cardiovascular.</span>
              <span v-else class="tooltiptext">Maximum heart rate achieved, which indicates cardiovascular functioning.</span>
            </span>
        </label>
        <label>
          Angina Induzida por Exercício (exang): <input v-model="formData.exang" type="checkbox" />
            <span class="tooltip">i
              <span v-if="!english" class="tooltiptext">Indica se o paciente apresenta dor no peito (angina) ao realizar exercícios físicos.</span>
              <span v-else class="tooltiptext">Indicates if the patient experiences chest pain (angina) during physical exertion.</span>
            </span>
        </label>
        <label>
          Depressão ST (oldpeak): <input v-model="formData.oldpeak" type="number" step="0.1" required />
            <span class="tooltip">i
              <span v-if="!english" class="tooltiptext">Medida de depressão do segmento ST, uma anormalidade eletrocardiográfica indicativa de problemas cardíacos.</span>
              <span v-else class="tooltiptext">ST depression measurement, an ECG abnormality indicative of heart issues.</span>
            </span>
        </label>
        <label>
          Tipo de Dor no Peito (cp): <input v-model="formData.cp" type="number" min="1" max="4" required />
            <span class="tooltip">i
              <span v-if="!english" class="tooltiptext">Tipo de dor no peito que o paciente sente, de acordo com uma escala de 1 a 4.</span>
              <span v-else class="tooltiptext">Type of chest pain experienced by the patient, based on a scale of 1 to 4.</span>
            </span>
        </label>
        <button type="submit" :disabled="!hasConsent">Prever Hipertensão</button>
      </form>

      <!-- Formulário para predição de AVC -->
      <form v-if="selectedPrediction === 'stroke' && this.gd.user_role === 'paciente'" @submit.prevent="predictStroke">
        <label>
          Hipertensão: <input v-model="formData.hypertension" type="checkbox" />
            <span class="tooltip">i
              <span v-if="!english" class="tooltiptext">Indica se o paciente possui hipertensão, um dos maiores fatores de risco para AVC.</span>
              <span v-else class="tooltiptext">Indicates if the patient has hypertension, one of the major risk factors for stroke.</span>
            </span>
        </label>
        <label>
          Doença Cardíaca: <input v-model="formData.heart_disease" type="checkbox" />
            <span class="tooltip">i
              <span v-if="!english" class="tooltiptext">Indica se o paciente tem doenças cardíacas, o que aumenta o risco de AVC.</span>
              <span v-else class="tooltiptext">Indicates if the patient has heart disease, which increases the risk of stroke.</span>
            </span>
        </label>
        <label>
          Nível Médio de Glicose: <input v-model="formData.avg_glucose_level" type="number" step="0.1" required />
            <span class="tooltip">i
              <span v-if="!english" class="tooltiptext">Nível médio de glicose no sangue. A diabetes aumenta o risco de AVC.</span>
              <span v-else class="tooltiptext">Average blood glucose level. Diabetes increases the risk of stroke.</span>
            </span>
        </label>
        <label>
          Índice de Massa Corporal (IMC): <input v-model="formData.bmi" type="number" required />
            <span class="tooltip">i
              <span v-if="!english" class="tooltiptext">Índice de Massa Corporal. A obesidade é um fator de risco importante para AVC.</span>
              <span v-else class="tooltiptext">Body Mass Index. Obesity is an important risk factor for stroke.</span>
            </span>
        </label>
        <label>
          {{ !english ? 'Status de Fumante: ' : 'Smoking Status: ' }}
          <select v-model="formData.smoking_status" required>
            <option value="" disabled>{{ !english ? 'Selecione...' : 'Select one...' }}</option>
            <option value="0">{{ !english ? 'Nunca Fumou' : 'Never Smoked' }}</option>
            <option value="1">{{ !english ? 'Fumou anteriormente' : 'Formerly Smoked' }}</option>
            <option value="2">{{ !english ? 'Atualmente fuma' : 'Currently Smokes' }}</option>
          </select>
          <span class="tooltip">i
            <span v-if="!english" class="tooltiptext">Indica o status de tabagismo do paciente: Nunca fumou, Fumou anteriormente ou Atualmente fuma.</span>
            <span v-else class="tooltiptext">Indicates the smoking status of the patient: Never smoked, Formerly smoked, or Currently smokes.</span>
          </span>
        </label>
        <label>
            {{ !english ? 'Já foi Casado(a): ' : 'Have your ever married: ' }}
          <select v-model="formData.ever_married" required>
            <option value="" disabled>{{ !english ? 'Selecione...' : 'Select one...' }}</option>
            <option value="0">{{ !english ? 'Não' : 'Not' }}</option>
            <option value="1">{{ !english ? 'Sim' : 'Yes' }}</option>
          </select>
          <span class="tooltip">i
            <span v-if="!english" class="tooltiptext">Indica se o paciente já foi casado(a). Estudos associam fatores socioeconômicos com a saúde cardiovascular.</span>
            <span v-else class="tooltiptext">Indicates if the patient has ever been married. Socioeconomic factors have been associated with cardiovascular health.</span>
          </span>
        </label>
        <button type="submit" :disabled="!hasConsent">{{ !english ? 'Prever AVC' : 'Predict Stroke' }}</button>
      </form>

      <!-- Mensagem de consentimento -->
      <p v-if="!hasConsent" style="color: red;">Consentimento necessário para realizar predições.</p>

      <div v-if="predictionResult && this.gd.user_role === 'paciente'" class="result-section">
        <h2 class="result-title">Prediction Result</h2>
        <p><strong>Risk:</strong> {{ predictionResult.risk }}</p>
        <p><strong>Probability:</strong> {{ predictionResult.probability }}</p>
      </div>

      <p v-if="error" class="error">{{ error }}</p>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent, watch, ComponentPublicInstance } from 'vue';
import axios from 'axios';
import { useRouter, RouteLocationNormalized, NavigationGuardNext} from 'vue-router';
import globalData from '../globalData';
import eventBus from '../eventBus';

export default defineComponent({
  name: 'HealthPrediction',
  data() {
    return {
      selectedPrediction: '', 
      hasConsent: globalData.user_consent, 
      formData: { 
        Age: '', BMI: '', HighChol: '', HighBP: '', PhysActivity: '', GenHlth: '', Smoker: '', // Diabetes
        age: '', trestbps: '', chol: '', thalach: '', exang: '', oldpeak: '', cp: '',         // Hipertensão
        hypertension: '', heart_disease: '', avg_glucose_level: '', bmi: '', smoking_status: '', ever_married: '' // AVC
      },
      predictionResult: null as { risk: number; probability: number } | null,
      last_input_data: '',
      error: '',
      gd: globalData,
      english: false,
    };
  },

  created() {
    watch(
      () => globalData.user_consent,
      (newConsent) => {
        this.gd.user_consent = newConsent;
      }
    );
  },

  methods: {

    resetForm() {
      this.formData = { 
        Age: '', BMI: '', HighChol: '', HighBP: '', PhysActivity: '', GenHlth: '', Smoker: '',
        age: '', trestbps: '', chol: '', thalach: '', exang: '', oldpeak: '', cp: '',
        hypertension: '', heart_disease: '', avg_glucose_level: '', bmi: '', smoking_status: '', ever_married: ''
      };
      this.predictionResult = null;
    },
    
    async predictDiabetes() {
      if (!this.hasConsent) return;
      try {
        const response = await axios.post('http://localhost:5000/predict/diabetes', this.formData, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        });
        this.predictionResult.risk = response.data.prediction;
        this.predictionResult.probability = response.data.probability;
        this.last_input_data = response.data.input_data;
        this.error = '';
        this.submitPrediction(this.predictionResult, this.last_input_data, this.selectedPrediction);
      } catch (err) {
        this.error = err.response?.data.error || `Failed to make prediction: ${err}`;
        this.predictionResult = null;
        this.last_input_data = null;
      }
    },

    async predictHypertension() {
      if (!this.hasConsent) return;
      try {
        const response = await axios.post('http://localhost:5000/predict/hypertension', this.formData, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        });
        this.predictionResult.risk = response.data.prediction;
        this.predictionResult.probability = response.data.probability;
        this.last_input_data = response.data.input_data;
        this.error = '';
        this.submitPrediction(this.predictionResult, this.last_input_data, this.selectedPrediction);
      } catch (err) {
        this.error = err.response?.data.error || `Failed to make prediction: ${err}`;
        this.predictionResult = null;
        this.last_input_data = null;
      }
    },
    
    async predictStroke() {
      if (!this.hasConsent) return;
      try {
        const response = await axios.post('http://localhost:5000/predict/stroke', this.formData, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        });
        this.predictionResult.risk = response.data.prediction;
        this.predictionResult.probability = response.data.probability;
        this.last_input_data = response.data.input_data;
        this.error = '';
        this.submitPrediction(this.predictionResult, this.last_input_data, this.selectedPrediction);
      } catch (err) {
        this.error = err.response?.data.error || `Failed to make prediction: ${err}`;
        this.predictionResult = null;
        this.last_input_data = null;
      }
    },
  },

  async submitPrediction(predict: any, input_data: any, selectedPrediction: string) {
    const predictionData = {
      prediction_type: selectedPrediction,
      input_data: input_data,
      prediction_result: { risk: predict.risk, probability: predict.probability }
    };

    try {

      await axios.post('http://localhost:5000/save-prediction', predictionData, {
        headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
      });

      eventBus.predictionSaved = true;
      this.last_input_data = null;

    } catch (err) {
      this.error = err.response?.data.error || `Error occured when trying save prediction: ${err}`;
    }
  },
  
});
</script>

<style scoped>
.tooltip {
  position: relative;
  display: inline-block;
  cursor: pointer;
}

.tooltiptext {
  visibility: hidden;
  width: 200px;
  background-color: black;
  color: #fff;
  text-align: center;
  border-radius: 5px;
  padding: 5px;
  position: absolute;
  z-index: 1;
  bottom: 125%; 
  left: 50%;
  margin-left: -100px;
  opacity: 0;
  transition: opacity 0.3s;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
  opacity: 1;
}

.health-prediction {
  /* Estilos da página de predição de saúde */
}

.page-title {
  /* Estilos para o título da página */
}

.prediction-section {
  /* Estilos da seção de formulário */
}

.form-group {
  margin-bottom: 15px;
}

.form-control {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
}

.submit-button {
  margin-top: 20px;
}

.result-section {
  margin-top: 20px;
}

.result-title {
  font-weight: bold;
  margin-bottom: 10px;
}

.error {
  color: red;
  margin-top: 10px;
}
</style>
