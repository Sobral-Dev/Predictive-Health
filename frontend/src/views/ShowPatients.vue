<template>
  <main>
    <transition name="fade" mode="out-in">

      <div class="show-patients">
        <h1 class="page-title">Patients List</h1>

        <section class="patients-section">
          <table class="patients-table">
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Age</th>
                <th>Medical Conditions</th>
                <th>Consent Status</th>
                <th>Created At</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="patient in patients" :key="patient.id">
                <td>{{ patient.id }}</td>
                <td>{{ patient.name }}</td>
                <td>{{ patient.birth_date }}</td>
                <td>{{ patient.medical_conditions }}</td>
                <td>{{ patient.consent_status ? 'Given' : 'Revoked' }}</td>
                <td>{{ patient.created_at }}</td>
                <td>
                  <button @click="viewPatientDetails(patient.id)" class="action-button">View</button>
                  <button @click="deletePatient(patient.id)" class="action-button">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
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
        birth_date: number;
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

        if (this.globalData.user_role === 'admin') {
          const response = await axios.get('http://localhost:5000/patients', {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          });
          this.patients = response.data;
        } else if (this.globalData.user_role === 'medico') {
          const response = await axios.get(`http://localhost:5000/doctor/${this.globalData.user_id}/patients`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          });
          this.patients = response.data;
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
      } catch (err) {
        this.error = err.response?.data.error || 'Failed to delete patient.';
      }
    },
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
