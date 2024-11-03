<template>
  <div class="consent-update">
    <h1 class="page-title">Update Consent</h1>

    <section class="consent-section">
      <form @submit.prevent="updateConsent">
        <div class="form-group">
          <label for="consent-status">Consent Status</label>
          <select id="consent-status" v-model="consentStatus" class="form-control" required>
            <option value="true">Given</option>
            <option value="false">Revoked</option>
          </select>
        </div>

        <button type="submit" class="submit-button">Update Consent</button>
      </form>

      <p v-if="message" class="message">{{ message }}</p>
      <p v-if="error" class="error">{{ error }}</p>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';

export default defineComponent({
  name: 'ConsentUpdate',
  data() {
    return {
      consentStatus: 'true',
      message: '',
      error: '',
    };
  },
  methods: {
    async updateConsent() {
      try {
        const response = await axios.post(
          `http://localhost:5000/patients/consent/${this.$route.params.id}`,
          {
            consent_status: this.consentStatus === 'true',
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          }
        );
        this.message = response.data.message || 'Consent updated successfully.';
        this.error = '';
      } catch (err) {
        this.error = err.response?.data.error || 'Failed to update consent.';
        this.message = '';
      }
    },
  },
  mounted() {
    // Opção para carregar o estado atual do consentimento (se necessário no futuro)
  },
});
</script>

<style scoped>
.consent-update {
  /* Estilos da página de atualização de consentimento */
}

.page-title {
  /* Estilos para o título da página */
}

.consent-section {
  /* Estilos da seção de formulário */
}

.form-group {
  margin-bottom: 15px;
}

.form-control {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
}

.submit-button {
  margin-top: 20px;
}

.message {
  color: green;
  margin-top: 10px;
}

.error {
  color: red;
  margin-top: 10px;
}
</style>
