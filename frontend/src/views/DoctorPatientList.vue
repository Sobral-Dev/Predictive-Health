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
                  <button v-if="patient.request_status === 'accepted'" @click="viewPatientDetails(patient.id)" class="action-button">View</button>
                  <button v-if="patient.request_status === 'pending'" @click="none" class="action-button" style="background-color: rgba(241, 196, 15, 1); cursor: none; border-color: rgba(241, 196, 15, 0.7);">Request Pending</button>
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
import axios from 'axios';
import { useRouter, RouteLocationNormalized, NavigationGuardNext} from 'vue-router';

export default {
  data() {
    return {
      patients: [],
      error: '',
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
  },

  methods: {

    async fetchPatients() {
      try {
        const response = await axios.get(`http://localhost:5000/doctor/${localStorage.getItem('gd.user_id')}/patients`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });

        const patients_accepted = response.data.patients_accepted;
        const patients_pending = response.data.patients_pending;

        this.patients = [
          ...patients_accepted.map((patient: any) => ({ ...patient, request_status: 'accepted' })),
          ...patients_pending.map((patient: any) => ({ ...patient, request_status: 'pending' }))
        ];

      } catch (err) {
        this.error = `An error occured when trying fetch Doctor patients: ${err}`;
      }
    },

    viewPatientDetails(patientId: number) {
      this.router.push({ name: 'PatientDetails', params: { id: patientId } });
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

};
</script>

<style scoped>
@import '../assets/css/base.css';

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