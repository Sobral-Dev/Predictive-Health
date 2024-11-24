<template>
  <main>
    <transition name="fade" mode="out-in">
      <section class="predictions-section">
        <h2>Patients Predictions History (Anonymized)</h2> <br>
        <table v-if="localStorage.getItem('gd.user_role') === 'admin'" class="predictions-table">
          <thead>
            <tr>
              <th>Patient ID</th>
              <th>Type</th>
              <th>Risk</th>
              <th>Probability</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="prediction in predictions" :key="prediction._id">
              <td>{{ prediction.user_id }}</td>
              <td>{{ prediction.prediction_type }}</td>
              <td>{{ prediction.prediction_result.risk === 0 ? 'Moderate' : 'High' }}</td>
              <td>{{ prediction.prediction_result.probability }}</td>
              <td>{{ prediction.timestamp }}</td>
            </tr>
          </tbody>
        </table>
        <p v-if="error" class="error">{{ error }}</p>
      </section>
    </transition>
  </main>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      predictions: [],
      error: '',
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

<style>
@import '../assets/css/base.css';

.predictions-section {
  margin-top: 20px;
}

.predictions-table {
  width: 100%;
  border-collapse: collapse;
}

.predictions-table th,
.predictions-table td {
  padding: 12px;
  border: 1px solid #ccc;
}

.predictions-table th {
  background-color: #f4f4f4;
  font-weight: bold;
}

.predictions-table tr:nth-child(even) {
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