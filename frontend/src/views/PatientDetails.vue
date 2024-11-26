<template>
  <transition name="fade" mode="out-in">
    <main>
      <div class="patient-details">
        <h1 class="page-title">Patient Details</h1>

        <section class="details-section" v-if="patient">
          <div class="detail-item">
            <label>Name: </label>
            <span v-if="!editPatient">{{ patient.name }}</span>
            <input v-else type="text" :placeholder="patient.name" v-model="updateValues.name">
          </div>

          <div class="detail-item">
            <label>Age: </label>
            <span v-if="!editPatient">{{ patient.age }} anos</span>
            <input v-else type="date" :placeholder="patient.age" v-model="updateValues.birth_date">
          </div>

          <div class="detail-item">
            <label>Medical Conditions: </label>
            <span v-if="!editPatient">{{ patient.medical_conditions }}</span>
            <input v-else type="text" :placeholder="patient.medical_conditions" v-model="updateValues.medical_conditions">
          </div>

          <div class="detail-item">
            <label>Consent Status: </label>
            <span>{{ patient.consent_status ? 'Given' : 'Revoked' }}</span>
          </div>

          <div class="detail-item">
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

          <div class="detail-item">
            <label>Created At: </label>
            <span>
              {{ patient.created_at }}
            </span>
          </div>       

          <button v-if="this.globalData.user_role === 'medico'" @click="requestAssociation(this.$route.params.id)">Request association with <b>{{ patient.name }}</b></button>
          <button v-if="this.globalData.user_role === 'medico' && !editPatient" @click="editPatient = true">Update Information of <b>{{ patient.name }}</b></button>

          <button v-if="this.globalData.user_role === 'medico' && editPatient && updateValues" @click="updatePatient(this.$route.params.id)">Update</button>

          <button @click="goBack" class="back-button">Back to Patients List</button>
        </section>

        <section class="details-section" v-if="predictions && this.globalData.user_role === 'medico'">
          <div class="detail-item" v-for="prediction in predictions" :key="prediction._id">
            <p>{{ prediction }}</p>
          </div>
        </section>
        
        <p v-if="message" class="message">{{ message }}</p>
        <p v-if="error" class="error">{{ error }}</p>
      </div>
    </main>
  </transition>
</template>

<script lang="ts">
import { defineComponent, watch, ComponentPublicInstance } from 'vue';
import axios from 'axios';
import { useRouter, RouteLocationNormalized, NavigationGuardNext} from 'vue-router';
import eventBus from '../eventBus';

export default defineComponent({
  name: 'PatientDetails',
  data() {
    return {
      patient: null as {
        age: number;
        consent_status: boolean;
        created_at: Date;
        has_patient_history: boolean;
        id: number;
        medical_conditions: string;
        name: string;
        
      } | null,
      error: '',
      message: '',
      globalData: {
        user_id: localStorage.getItem('gd.user_id'),
        user_role: localStorage.getItem('gd.user_role')
      },
      editPatient: false,
      updateValues: {
        name: null,
        birth_date: null,
        medical_conditions: null
      },
      predictions: {},
    };
  },

    setup() {
      const router = useRouter();
      return { router };
  },

  mounted() {
    this.fetchPatientDetails();
    this.fetchPredictionsHistory();

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
        const response = await axios.get(`http://localhost:5000/patients/${this.$route.params.id}/${this.globalData.user_role}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        this.patient = response.data;
        this.updateValues = response.data;
      } catch (err) {
        this.error = err.response?.data.error || 'Failed to fetch patient details.';
      }
    },
    goBack() {
      this.router.push({ name: 'ShowPatients' });
    },

    async requestAssociation(patientId: number) {
      try {
        await axios.post('http://localhost:5000/doctor-patient', { patient_id: patientId }, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        this.message = 'Request sent successfully.';
      } catch (err) {
        this.error = `Error when trying send request: ${err}`;
      }
    },

    async updatePatient(patientId: number) {

      try {
        await axios.put(`http://localhost:5000/patients/${patientId}`, {
          name: this.updateValues.name,
          birth_date: this.updateValues.birth_date,
          medical_conditions: this.updateValues.medical_conditions
        }, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        this.editPatient = false;
        this.updateValues = {};
        this.message = 'Update made successfully.';
      } catch (err) {
        this.error = `Error when trying update Patient Information: ${err}`;
      }

    },

    async fetchPredictionsHistory() {

      if (this.globalData.user_role !== 'medico') {
        return this.predictions = {};
      }

      try {
        const response = await axios.get(`http://localhost:5000/doctor/${this.globalData.user_id}/patient/${this.$route.params.id}/predictions`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        this.predictions = response.data;
      } catch (err) {
        this.error = err.response?.data.error || 'Failed to fetch predictions history.';
        this.predictions = {};
      }
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
