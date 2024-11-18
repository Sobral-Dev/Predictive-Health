<template>
  <div class="user-predictions">
    <h2 v-if="this.gd.user_role === 'paciente'">Your Prediction History</h2>
    <table v-if="predictions.length && this.gd.user_role === 'paciente'">
      <thead>
        <tr>
          <th>Type</th>
          <th>Result</th>
          <th>Probability</th>
          <th>Date</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="prediction in predictions" :key="prediction._id">
          <td>{{ prediction.prediction_type }}</td>
          <td>{{ prediction.result }}</td>
          <td>{{ prediction.probability }}</td>
          <td>{{ formatDate(prediction.timestamp) }}</td>
        </tr>
      </tbody>
    </table>

    <p v-if="!predictions.length && this.gd.user_role === 'paciente'">No predictions made by you were found.</p>
    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script lang="ts">
import axios from 'axios';
import globalData from '../globalData';

export default {
  name: 'UserPredictions',
  data() {
    return {
      predictions: [],
      error: '',
      gd: globalData,
    };
  },

  mounted() {
    this.fetchPredictions();
  },

  methods: {

    async fetchPredictions() {

      try {
        const response = await axios.get('http://localhost:5000/user/predictions', {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` },
        });
        this.predictions = response.data;
        this.error = '';

      } catch (err) {
        this.error = `An error occured when trying get your predictions history: ${err}`;
      }
    },

    formatDate(timestamp) {
      const date = new Date(timestamp);
      return date.toLocaleString();
    },
  },
};
</script>

<style scoped>
.user-predictions {
  padding: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th, td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: center;
}

th {
  background-color: #f4f4f4;
}
</style>
