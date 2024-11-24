<template>
  <main>
    <transition name="fade" mode="out-in">

      <div class="personal-data-export">
        <h1 class="page-title">Export Personal Data</h1>

        <section v-if="this.globalData.user_role === 'paciente'" class="checkbox-section">
          <p>Which information do you want?</p>

          <div class="select-data">
            <input type="radio" id="user" v-model="userData" @value="true" @change="!patientData">
            <label for="user">Your User Data</label><br>
            <input type="radio" id="patient" v-model="patientData" @value="true" @change="!userData">
            <label for="patient">Your Prediction History</label><br>
          </div>
        </section>

        <section class="export-section">
          <p>Select a format to export your data:</p>
          
          <div class="export-options">
            <button 
            v-if="this.globalData.user_role === 'paciente' ? 
            userData !== false || patientData !== false : 
            this.globalData.user_id !== null" 
            @click="exportData('json')" 
            class="export-button">
            Export as JSON
            </button>
            
            <button
            v-if="this.globalData.user_role === 'paciente' ? 
            userData !== false || patientData !== false : 
            this.globalData.user_id !== null"  
            @click="exportData('csv')" 
            class="export-button">
            Export as CSV
            </button>
          </div>
        </section>

        <p v-if="error" class="error">{{ error }}</p>
      </div>
    </transition>
  </main>
</template>

<script lang="ts">
import { defineComponent, watch, ComponentPublicInstance } from 'vue';
import axios from 'axios';

export default defineComponent({
  name: 'PersonalDataExport',
  data() {
    return {
      error: '',
      globalData: {
        user_id: localStorage.getItem('gd.user_id'),
        user_role: localStorage.getItem('gd.user_role')
      },
      userData: true, 
      patientData: false,
    };
  },

  methods: {
    async exportData(format: string) {

      if (this.userData) {

        try {

          const response = await axios.get(`http://localhost:5000/user/export?format=${format}`, {
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

      } else if(this.globalData.user_role === 'paciente' && this.patientData) {
      
        try {

          const response = await axios.get(`http://localhost:5000/patient/export?format=${format}`, {
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
