<template>
  <div class="personal-data-export">
    <h1 class="page-title">Export Personal Data</h1>

    <section class="export-section">
      <p>Select a format to export your data:</p>
      
      <div class="export-options">
        <button @click="exportData('json')" class="export-button">Export as JSON</button>
        <button @click="exportData('csv')" class="export-button">Export as CSV</button>
      </div>
    </section>

    <p v-if="error" class="error">{{ error }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, watch, ComponentPublicInstance } from 'vue';
import axios from 'axios';
import { useRouter, RouteLocationNormalized, NavigationGuardNext} from 'vue-router';

export default defineComponent({
  name: 'PersonalDataExport',
  data() {
    return {
      error: '',
    };
  },

  methods: {
    async exportData(format: string) {
      try {
        const response = await axios.get(`http://localhost:5000/patients/export/${this.$route.params.id}?format=${format}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
          responseType: 'blob',
        });

        // Create a URL for the downloaded data
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', `patient_data.${format}`);
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);

        this.error = '';
      } catch (err) {
        this.error = err.response?.data.error || 'Failed to export data.';
      }
    },
  },
  
});
</script>

<style scoped>
.personal-data-export {
  /* Estilos da página de exportação de dados pessoais */
}

.page-title {
  /* Estilos para o título da página */
}

.export-section {
  margin-top: 20px;
}

.export-options {
  display: flex;
  gap: 10px;
}

.export-button {
  padding: 10px 20px;
}

.error {
  color: red;
  margin-top: 10px;
}
</style>
