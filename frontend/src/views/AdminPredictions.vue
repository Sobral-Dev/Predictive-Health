<template>
  <div>
    <h2>Patients Predictions History (Anonymized)</h2>
    <ul v-if="this.gd.user_role === 'admin'">
      <li v-for="prediction in predictions" :key="prediction._id">
        User ID: {{ prediction.user_id }} - Type: {{ prediction.prediction_type }} - Result: {{ prediction.result }} - Probability: {{ prediction.probability }}
      </li>
    </ul>
  </div>

  <p v-if="error" class="error">{{ error }}</p>
</template>

<script>
import axios from 'axios';
import globalData from '../globalData';

export default {
  data() {
    return {
      predictions: [],
      error: '',
      gd: globalData,
    };
  },
  created() {
    this.fetchPredictions();
  },
  methods: {
    async fetchPredictions() {
      try {
        const response = await axios.get('http://localhost:5000/admin/predictions', {
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
