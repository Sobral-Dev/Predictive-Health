<template>
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
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="patient in patients" :key="patient.id">
            <td>{{ patient.id }}</td>
            <td>{{ patient.name }}</td>
            <td>{{ patient.age }}</td>
            <td>{{ patient.medical_conditions }}</td>
            <td>{{ patient.consent_status ? 'Given' : 'Revoked' }}</td>
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
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

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
      }>,
      error: '',
    };
  },
  methods: {
    async fetchPatients() {
      try {
        const response = await axios.get('http://localhost:5000/patients', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        this.patients = response.data;
      } catch (err) {
        this.error = err.response?.data.error || 'Failed to fetch patients list.';
      }
    },
    viewPatientDetails(patientId: number) {
      const router = useRouter();
      router.push({ name: 'PatientDetails', params: { id: patientId } });
    },
    async deletePatient(patientId: number) {
      try {
        await axios.delete(`http://localhost:5000/patients/${patientId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        this.fetchPatients(); // Refresh the patients list after deletion
      } catch (err) {
        this.error = err.response?.data.error || 'Failed to delete patient.';
      }
    },
  },
  mounted() {
    this.fetchPatients();
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
