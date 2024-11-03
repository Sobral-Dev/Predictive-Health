<template>
  <div class="health-prediction">
    <h1 class="page-title">Health Prediction</h1>

    <section class="prediction-section">
      <form @submit.prevent="makePrediction">
        <div class="form-group">
          <label for="age">Age</label>
          <input 
            type="number" 
            id="age" 
            v-model="form.age" 
            required 
            class="form-control" 
          />
        </div>

        <div class="form-group">
          <label for="bmi">BMI</label>
          <input 
            type="number" 
            step="0.1" 
            id="bmi" 
            v-model="form.bmi" 
            required 
            class="form-control" 
          />
        </div>

        <div class="form-group">
          <label for="glucose-level">Glucose Level</label>
          <input 
            type="number" 
            id="glucose-level" 
            v-model="form.glucose_level" 
            required 
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label for="prediction-type">Prediction Type</label>
          <select id="prediction-type" v-model="form.prediction_type" class="form-control" required>
            <option value="diabetes">Diabetes</option>
            <option value="hypertension">Hypertension</option>
            <option value="stroke">Stroke</option>
          </select>
        </div>

        <button type="submit" class="submit-button">Make Prediction</button>
      </form>

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
import { defineComponent } from 'vue';
import axios from 'axios';

export default defineComponent({
  name: 'HealthPrediction',
  data() {
    return {
      form: {
        age: null as number | null,
        bmi: null as number | null,
        glucose_level: null as number | null,
        prediction_type: 'diabetes',
      },
      predictionResult: null as { prediction: number; probability: number } | null,
      error: '',
    };
  },
  methods: {
    async makePrediction() {
      try {
        const endpointMap = {
          diabetes: 'http://localhost:5000/predict/diabetes',
          hypertension: 'http://localhost:5000/predict/hypertension',
          stroke: 'http://localhost:5000/predict/stroke',
        };

        const endpoint = endpointMap[this.form.prediction_type];

        const response = await axios.post(
          endpoint,
          {
            age: this.form.age,
            bmi: this.form.bmi,
            glucose_level: this.form.glucose_level,
            consent_status: true, // Supondo que o consentimento foi dado e está validado no backend
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          }
        );

        this.predictionResult = response.data;
        this.error = '';
      } catch (err) {
        this.error = err.response?.data.error || 'Failed to make prediction.';
        this.predictionResult = null;
      }
    },
  },
});
</script>

<style scoped>
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
