<template>
  <main>
    <transition name="fade" mode="out-in">
      
      <div>
        <h2>Pacientes Associados</h2>
        <ul>
          <li v-for="patient in patients" :key="patient.id" @click.prevent="this.$router.push(`/patients/${patient.id}`)" style="cursor: pointer;">
            {{ patient.name }} - {{ patient.birth_date }}
          </li>
        </ul>

        <p v-if="error" class="error">{{ error }}</p>
      </div>
    </transition>
  </main>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      patients: [],
      error: '',
    };
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
        this.patients = response.data;
      } catch (err) {
        this.error = `An error occured when trying fetch Doctor patients: ${err}`;
      }
    },
    
  },

};
</script>
