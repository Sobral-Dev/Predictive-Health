<template>
  <main>
    <transition name="fade" mode="out-in">
      
      <div>
        <h2>Patients Predictions History</h2>
        <ul v-if="this.globalData.user_role === 'medico'">
          <li v-for="prediction in predictions" :key="prediction._id">
            Patient ID: {{ prediction.user_id }} - Type: {{ prediction.prediction_type }} - Result: {{ prediction.result }} - Probability: {{ prediction.probability }}
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
      predictions: [],
      globalData: {
        user_role: localStorage.getItem('gd.user_role') 
      },
      error: '',
    };
  },
  created() {
    this.fetchPredictions();
  },
  methods: {
    async fetchPredictions() {
      try {
        const response = await axios.get(`http://localhost:5000/doctor/${localStorage.getItem('gd.user_id')}/predictions`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        this.predictions = response.data;
        this.error = '';
      } catch (err) {
        this.error = `An error occured when trying get predictions: ${err}`;
      }
    }
  }
};
</script>
