<template>
  <div class="patient-details">
    <h1 class="page-title">Patient Details</h1>

    <section class="details-section" v-if="patient">
      <div class="detail-item">
        <label>Name: </label>
        <span>{{ patient.name }}</span>
      </div>

      <div class="detail-item">
        <label>Age: </label>
        <span>{{ patient.age }}</span>
      </div>

      <div class="detail-item">
        <label>Medical Conditions: </label>
        <span>{{ patient.medical_conditions }}</span>
      </div>

      <div class="detail-item">
        <label>Consent Status: </label>
        <span>{{ patient.consent_status ? 'Given' : 'Revoked' }}</span>
      </div>

      <div class="profile-item">
        <label>With Patient History: </label>
        <span>
          {{
            patient.has_patient_history === true
              ? 'Yes'
              : patient.has_patient_history === false
              ? 'No'
              : "Hasn't got a patient history yet"
          }}
        </span>
      </div>

      <div class="profile-item">
        <label>Created At: </label>
        <span>
          {{ patient.created_at }}
        </span>
      </div>       

      <button @click="goBack" class="back-button">Back to Patients List</button>
    </section>
    
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, watch, ComponentPublicInstance } from 'vue';
import axios from 'axios';
import { useRouter, RouteLocationNormalized, NavigationGuardNext} from 'vue-router';
import eventBus from '../eventBus';
import globalData from '../globalData';

export default defineComponent({
  name: 'PatientDetails',
  data() {
    return {
      patient: null as {
        name: string;
        age: number;
        medical_conditions: string;
        consent_status: boolean;
        has_patient_history: boolean;
        created_at: Date;
      } | null,
      error: '',
      gd: globalData,
    };
  },

    setup() {
      const router = useRouter();
      return { router };
  },

  created() {
    watch(
      () => globalData.user_consent,
      (newConsent) => {
        this.gd.user_consent = newConsent;
      }
    );
  },

  mounted() {
    this.fetchPatientDetails();

     watch(
      () => eventBus.patientsUpdated, 
      (newValue) => {
        if (newValue) {
          this.fetchPatientDetails();
          eventBus.patientsUpdated = false;
        }
      }
    );
  },

  methods: {
    async fetchPatientDetails() {
      try {
        const response = await axios.get(`http://localhost:5000/patients/${this.$route.params.id}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        this.patient = response.data;
      } catch (err) {
        this.error = err.response?.data.error || 'Failed to fetch patient details.';
      }
    },
    goBack() {
      this.router.push({ name: 'ShowPatients' });
    },
  },

    beforeRouteEnter(
    to: RouteLocationNormalized,
    from: RouteLocationNormalized,
    next: NavigationGuardNext) {
    
      next((vm) => {
        (vm as ComponentPublicInstance & { fetchPatientDetails: () => void }).fetchPatientDetails();
      });
  },

});
</script>

<style scoped>
.patient-details {
  /* Estilos da página de detalhes do paciente */
}

.page-title {
  /* Estilos para o título da página */
}

.details-section {
  margin-top: 20px;
}

.detail-item {
  margin-bottom: 15px;
}

.detail-item label {
  font-weight: bold;
}

.back-button {
  margin-top: 20px;
}

.error {
  color: red;
  margin-top: 10px;
}
</style>
