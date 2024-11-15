<template>
  <div class="health-prediction">
    <h1 class="page-title">Health Prediction</h1>

    <section class="prediction-section">
      
      <!-- Select para escolher o tipo de predição -->
      <label for="predictionType">Escolha o tipo de predição: </label>
      <select v-model="selectedPrediction" @change="resetForm">
        <option disabled value="">Selecione uma condição...</option>
        <option value="diabetes">Diabetes</option>
        <option value="hypertension">Hipertensão</option>
        <option value="stroke">AVC</option>
      </select>

      <!-- Formulário para predição de Diabetes -->
      <form v-if="selectedPrediction === 'diabetes'" @submit.prevent="predictDiabetes">
        <label>
          Idade: <input v-model="formData.Age" type="number" required />
            <span class="tooltip">i
              <span v-if="!english" class="tooltiptext">Idade do paciente, fator de risco importante para o desenvolvimento de diabetes tipo 2. A idade avançada está associada ao aumento da resistência à insulina.</span>
              <span v-else class="tooltiptext">Patient's age, a significant risk factor for type 2 diabetes. Advanced age is associated with increased insulin resistance.</span>
            </span>
        </label>
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
      <form v-if="selectedPrediction === 'hypertension'" @submit.prevent="predictHypertension">
        <label>
          Idade: <input v-model="formData.age" type="number" required />
            <span class="tooltip">i
              <span v-if="!english" class="tooltiptext">Idade do paciente, associada ao endurecimento arterial e aumento da pressão arterial ao longo dos anos.</span>
              <span v-else class="tooltiptext">Patient's age, associated with arterial stiffening and increased blood pressure over the years.</span>
            </span>
        </label>
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
      <form v-if="selectedPrediction === 'stroke'" @submit.prevent="predictStroke">
        <label>
          Idade: <input v-model="formData.age" type="number" required />
            <span class="tooltip">i
              <span v-if="!english" class="tooltiptext">Idade do paciente. O risco de AVC aumenta com o envelhecimento devido ao endurecimento e obstrução das artérias.</span>
              <span v-else class="tooltiptext">Patient's age. The risk of stroke increases with age due to arterial stiffening and blockages.</span>
            </span>
        </label>
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
          Status de Fumante: <input v-model="formData.smoking_status" type="text" required />
            <span class="tooltip">i
              <span v-if="!english" class="tooltiptext">Indica se o paciente fuma, hábito que aumenta o risco de problemas cardiovasculares e AVC.</span>
              <span v-else class="tooltiptext">Indicates if the patient smokes, a habit that increases cardiovascular issues and stroke risk.</span>
            </span>
        </label>
        <label>
          Já foi Casado(a): <input v-model="formData.ever_married" type="checkbox" />
            <span class="tooltip">i
              <span v-if="!english" class="tooltiptext">Indica se o paciente já foi casado(a). Estudos associam fatores socioeconômicos com a saúde cardiovascular.</span>
              <span v-else class="tooltiptext">Indicates if the patient has ever been married. Socioeconomic factors have been associated with cardiovascular health.</span>
            </span>
        </label>
        <button type="submit" :disabled="!hasConsent">Prever AVC</button>
      </form>

      <!-- Mensagem de consentimento -->
      <p v-if="!hasConsent" style="color: red;">Consentimento necessário para realizar predições.</p>

      <div v-if="predictionResult" class="result-section">
        <h2 class="result-title">Prediction Result</h2>
        <p><strong>Risk:</strong> {{ predictionResult.prediction }}</p>
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
import globalData from '../globalData'

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
      predictionResult: null as { prediction: number; probability: number } | null,
      error: '',
      gd: globalData,
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
        this.predictionResult = response.data;
        this.error = '';
      } catch (err) {
        this.error = err.response?.data.error || `Failed to make prediction: ${err}`;
        this.predictionResult = null;
      }
    },

    async predictHypertension() {
      if (!this.hasConsent) return;
      try {
        const response = await axios.post('http://localhost:5000/predict/hypertension', this.formData, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        });
        this.predictionResult = response.data;
        this.error = '';
      } catch (err) {
         this.error = err.response?.data.error || `Failed to make prediction: ${err}`;
        this.predictionResult = null;
      }
    },
    
    async predictStroke() {
      if (!this.hasConsent) return;
      try {
        const response = await axios.post('http://localhost:5000/predict/stroke', this.formData, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        });
        this.predictionResult = response.data;
        this.error = '';
      } catch (err) {
         this.error = err.response?.data.error || `Failed to make prediction: ${err}`;
        this.predictionResult = null;
      }
    },
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
