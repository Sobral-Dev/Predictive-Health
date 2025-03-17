<template>
  <main>
    <transition name="fade" mode="out-in">
      <section class="predictions-section">
        <h2>Patients Predictions History (Anonymized)</h2> <br>
        <table v-if="user_role === 'admin'" class="predictions-table">
          <thead>
            <tr>
              <th>Type</th>
              <th>Risk</th>
              <th>Probability</th>
              <th>Timestamp</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="prediction in paginated" :key="prediction._id" :title="`id: ${prediction._id}`">
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
      user_role: localStorage.getItem('gd.user_role'),
      currentPage: 1, 
      perPage: 10,
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