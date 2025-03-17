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
            <input v-else type="date" v-model="updateValues.birth_date">
          </div>

          <div class="detail-item">
            <label>Medical Conditions: </label>
            <span v-if="!editPatient" v-for="(medical_condition, index) in patient.medical_conditions">
              {{ medical_condition }}{{ index < patient.medical_conditions.length - 1 ? ', ' : '' }}</span>
            <input v-else type="text" :placeholder="patient.medical_conditions" v-model="updateValues.medical_conditions">
          </div>

          <div class="detail-item">
            <label>Created At: </label>
            <span>
              {{ new Date(patient.created_at).toLocaleString("pt-BR") }}
            </span>
          </div>       

          <button v-if="this.globalData.user_role === 'medico' && !editPatient" @click="editPatient = true">Update Information of <b>{{ patient.name }}</b></button>

          <button v-if="this.globalData.user_role === 'medico' && editPatient && updateValues" @click="updatePatient(this.$route.params.id)">Update</button>

          <button @click="goBack" class="back-button">Back to Patients List</button>
        </section>

        <section class="details-section" v-if="predictions && this.globalData.user_role === 'medico'">
          <h3 style="margin: 10px; padding-left: 1vw;">User Predictions History</h3>
          <table class="predictions-table">
            <thead>
              <tr>
                <th>Type</th>
                <th>Risk</th>
                <th>Probability</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="prediction in paginated" :key="prediction._id">
                <td>{{ prediction.prediction_type }}</td>
                <td><i style="font-style: normal;" :style="prediction.prediction_result.risk === 1 ? 'color: rgba(231, 76, 60, 1);' : 'color: rgba(241, 196, 15, 1);'">{{ prediction.prediction_result.risk === 1 ? 'High' : 'Moderate'  }}</i></td>
                <td>{{ (prediction.prediction_result.probability * 100).toFixed(0) }}%</td>
                <td>{{ new Date(prediction.timestamp).toLocaleString("pt-BR") }}</td>
              </tr>
            </tbody>
          </table>

          <div class="pagination">
              <button @click="prevPage" :disabled="currentPage === 1">Anterior</button>
              <span>Página {{ currentPage }} de {{ totalPages }}</span>
              <button @click="nextPage" :disabled="currentPage === totalPages">Próxima</button>
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
        birth_date: string;
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
      predictions: [],
      currentPage: 1, 
      perPage: 10,
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
      this.$router.back();
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
        this.fetchPatientDetails();
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

    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },

    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },

  },

  computed: {
    paginated() {
      const start = (this.currentPage - 1) * this.perPage;
      const end = start + this.perPage;
      return this.predictions.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.predictions.length / this.perPage);
    }
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
