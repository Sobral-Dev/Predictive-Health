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
        
        <div class="form-group">
          <label for="cpf">CPF</label>
          <input 
            type="text" 
            id="cpf" 
            v-model="form.cpf" 
            required
            @input="formatCPF"
            placeholder="000.000.000-00" 
            class="form-control"
          />
        </div>

        <button type="submit" class="submit-button">Register Patient</button>
      </form>

      <p v-if="message" class="message">{{ message }}</p>
      <p v-if="error" class="error">{{ error }}</p>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent, watch, ComponentPublicInstance } from 'vue';
import axios from 'axios';
import { useRouter, RouteLocationNormalized, NavigationGuardNext} from 'vue-router';
import eventBus from '../eventBus'
import globalData from '../globalData';

export default defineComponent({
  name: 'RegisterPatient',
  data() {
    return {
      form: {
        name: '',
        age: null as number | null,
        medical_conditions: '',
        consent_status: null,
        cpf: '',
      },
      message: '',
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
    async registerPatient() {
      try {
        const response = await axios.post(
          'http://localhost:5000/register_patient',
          {
            name: this.form.name,
            age: this.form.age,
            medical_conditions: this.form.medical_conditions,
            consent_status: this.form.consent_status === 'true',
            cpf: this.form.cpf.replace(/\D/g, '')
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
        eventBus.patientsUpdated = true;
      } catch (err) {
        this.error = err.response?.data.error || 'Failed to register patient.';
        this.message = '';
      }
    },
    resetForm() {
      this.form.name = '';
      this.form.age = null;
      this.form.medical_conditions = '';
      this.form.consent_status = null;
      this.form.cpf = '';
    },
  },

    formatCPF() {
      // Remove qualquer caractere que não seja número
      this.form.cpf = this.form.cpf.replace(/\D/g, '');
      
      // Aplica a máscara do CPF manualmente
      if (this.form.cpf.length <= 3) {
        this.form.cpf = this.form.cpf.replace(/(\d{3})/, '$1');
      } else if (this.form.cpf.length <= 6) {
        this.form.cpf = this.form.cpf.replace(/(\d{3})(\d{1,3})/, '$1.$2');
      } else if (this.form.cpf.length <= 9) {
        this.form.cpf = this.form.cpf.replace(/(\d{3})(\d{3})(\d{1,3})/, '$1.$2.$3');
      } else {
        this.form.cpf = this.form.cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{1,2})/, '$1.$2.$3-$4');
      }
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
