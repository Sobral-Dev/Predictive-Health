<template>
  <main>
    <transition name="fade" mode="out-in">
      
      <div>
        <h2 style="padding-bottom: 25px;">Your Patients Predictions History</h2>
        <section class="details-section" v-if="predictions && this.globalData.user_role === 'medico'">
          <table class="predictions-table">
            <thead>
              <tr>
                <th>Patient</th>
                <th>Type</th>
                <th>Risk</th>
                <th>Probability</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="prediction in paginated" :key="prediction._id">
                <td>{{ prediction.patient_id }}</td>
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
        </section>

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
        const response = await axios.get(`http://localhost:5000/doctor/${localStorage.getItem('gd.user_id')}/predictions`, {
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
