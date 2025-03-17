<template>
  <main>
    <transition name="fade" mode="out-in">

      <div class="show-patients">
        <h1 class="page-title">Patients List</h1>
  
        <section class="patients-section">
          <table class="patients-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Age</th>
                <th>Medical Conditions</th>
                <th>Created At</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="patient in paginated" :key="patient.id">
                <td>{{ patient.name }}</td>
                <td>{{ patient.age }}</td>
                <td><span v-for="(medical_condition, index) in patient.medical_conditions">{{ medical_condition }}{{ index < patient.medical_conditions.length - 1 ? ', ' : '' }}</span></td>
                <td>{{ new Date(patient.created_at).toLocaleString("pt-BR") }}</td>
                <td>
                  <button v-if="this.globalData.user_role === 'admin' || isInDoctorPatients(patient)" @click="viewPatientDetails(patient.id)" class="action-button">View</button>
                  <button v-if="this.globalData.user_role === 'admin'" @click="deletePatient(patient.id)" class="action-button">Delete</button>
                  <button v-if="this.globalData.user_role === 'medico'" 
                  @click="isInDoctorPatients(patient) || isInDoctorPatientsPending(patient) ? null : requestAssociation(patient.id)" 
                  :style="isInDoctorPatients(patient) ? 'background-color: rgba(52, 152, 219, 1); cursor: none; border-color: rgba(41, 128, 185, 1);' : (isInDoctorPatientsPending(patient) ? 'background-color: rgba(241, 196, 15, 1); cursor: none; border-color: rgba(241, 196, 15, 0.7);' : '')"
                  >
                    {{ isInDoctorPatients(patient) ? 'Already your Patient' : (isInDoctorPatientsPending(patient) ? 'Already Requested' : 'Request Association') }}
                  </button>
                </td>
              </tr>
            </tbody>
          </table>

        <div class="pagination">
            <button @click="prevPage" :disabled="currentPage === 1">Anterior</button>
            <span>Página {{ currentPage }} de {{ totalPages }}</span>
            <button @click="nextPage" :disabled="currentPage === totalPages">Próxima</button>
        </div>
        </section>

        <p v-if="error" class="error">{{ error }}</p>
      </div>
    </transition>
  </main>
</template>

<script lang="ts">
import { defineComponent, watch, ComponentPublicInstance } from 'vue';
import axios from 'axios';
import { useRouter, RouteLocationNormalized, NavigationGuardNext} from 'vue-router';
import eventBus from '../eventBus';

export default defineComponent({
  name: 'ShowPatients',
  data() {
    return {
      patients: [] as Array<{
        id: number;
        name: string;
        age: number;
        medical_conditions: string;
        consent_status: boolean;
        has_patient_history: boolean;
        created_at: Date;
      }>,
      error: '',
      globalData: {
        user_id: localStorage.getItem('gd.user_id'),
        user_role: localStorage.getItem('gd.user_role')
      },
      doctor_patients: [],
      doctor_patients_pending: [],
      currentPage: 1, 
      perPage: 10,
    };
  },

  setup() {
      const router = useRouter();
      return { router };
  },

  mounted() {
    this.fetchPatients();

    watch(
      () => eventBus.patientsUpdated, 
      (newValue) => {
        if (newValue) {
          this.fetchPatients();
          eventBus.patientsUpdated = false;
        }
      }
    );
  },

  methods: {
    async fetchPatients() {
      try {

          const response = await axios.get('http://localhost:5000/patients', {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          });
          this.patients = response.data.patients;
        
        if (this.globalData.user_role === 'medico') {
          const response = await axios.get(`http://localhost:5000/doctor/${this.globalData.user_id}/patients`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          });
          this.doctor_patients = response.data.patients_accepted;
          this.doctor_patients_pending = response.data.patients_pending;
        }
      } catch (err) {
        this.error = err.response?.data.error || 'Failed to fetch patients list.';
      }
    },
    viewPatientDetails(patientId: number) {
      this.router.push({ name: 'PatientDetails', params: { id: patientId } });
    },
    async deletePatient(patientId: number) {
      try {
        await axios.delete(`http://localhost:5000/patients/${patientId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        eventBus.patientsUpdated = true;
        this.fetchPatients();
      } catch (err) {
        this.error = err.response?.data.error || 'Failed to delete patient.';
      }
    },

    isInDoctorPatients(patient) {
      return this.doctor_patients.some(dp => dp.id === patient.id);
    },

    isInDoctorPatientsPending(patient) {
      return this.doctor_patients_pending.some(dp => dp.id === patient.id);
    },

    async requestAssociation(patientId: number) {
      try {
        await axios.post('http://localhost:5000/doctor-patient', { patient_id: patientId }, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
         localStorage.setItem(`requested_${patientId}`, `${patientId}`);
        this.fetchPatients();
        this.message = 'Request sent successfully.';
      } catch (err) {
        this.error = `Error when trying send request: ${err}`;
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
      return this.patients.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.patients.length / this.perPage);
    }
  },

  beforeRouteEnter(
    to: RouteLocationNormalized,
    from: RouteLocationNormalized,
    next: NavigationGuardNext) {
    
      next((vm) => {
        (vm as ComponentPublicInstance & { fetchPatients: () => void }).fetchPatients();
      });
  },

});
</script>

<style scoped>
.show-patients {
  /* Estilos da página de lista de pacientes */
}

.page-title {
  /* Estilos para o título da página */
}

.patients-section {
  margin-top: 20px;
}

.patients-table {
  width: 100%;
  border-collapse: collapse;
}

.patients-table th,
.patients-table td {
  padding: 12px;
  border: 1px solid #ccc;
}

.patients-table th {
  background-color: #f4f4f4;
  font-weight: bold;
}

.patients-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.action-button {
  margin: 0 5px;
}

.error {
  color: red;
  margin-top: 10px;
}
</style>
