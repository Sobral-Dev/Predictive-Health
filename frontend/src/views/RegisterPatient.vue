<template>
  <div class="register-patient">
    <h1 class="page-title">Register New Patient</h1>

    <section class="form-section">
      <form @submit.prevent="registerPatient">
        <div class="form-group">
          <label for="name">Name</label>
          <input 
            type="text" 
            id="name" 
            v-model="form.name" 
            required 
            class="form-control"
          />
        </div>

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
          <label for="medical-conditions">Medical Conditions</label>
          <textarea 
            id="medical-conditions" 
            v-model="form.medical_conditions" 
            required 
            class="form-control"
          ></textarea>
        </div>

        <div class="form-group">
          <label for="consent-status">Consent Status</label>
          <select id="consent-status" v-model="form.consent_status" class="form-control" required>
            <option value="true">Given</option>
            <option value="false">Revoked</option>
          </select>
        </div>

        <button type="submit" class="submit-button">Register Patient</button>
      </form>

      <p v-if="message" class="message">{{ message }}</p>
      <p v-if="error" class="error">{{ error }}</p>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';

export default defineComponent({
  name: 'RegisterPatient',
  data() {
    return {
      form: {
        name: '',
        age: null as number | null,
        medical_conditions: '',
        consent_status: 'true',
      },
      message: '',
      error: '',
    };
  },
  methods: {
    async registerPatient() {
      try {
        const response = await axios.post(
          'http://localhost:5000/patients',
          {
            name: this.form.name,
            age: this.form.age,
            medical_conditions: this.form.medical_conditions,
            consent_status: this.form.consent_status === 'true',
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          }
        );

        this.message = response.data.message || 'Patient registered successfully.';
        this.error = '';
        this.resetForm();
      } catch (err) {
        this.error = err.response?.data.error || 'Failed to register patient.';
        this.message = '';
      }
    },
    resetForm() {
      this.form.name = '';
      this.form.age = null;
      this.form.medical_conditions = '';
      this.form.consent_status = 'true';
    },
  },
});
</script>

<style scoped>
.register-patient {
  /* Estilos da página de registro de paciente */
}

.page-title {
  /* Estilos para o título da página */
}

.form-section {
  margin-top: 20px;
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

.message {
  color: green;
  margin-top: 10px;
}

.error {
  color: red;
  margin-top: 10px;
}
</style>
