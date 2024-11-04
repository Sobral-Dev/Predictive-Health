<template>
  <div class="consent-update">
    <h1 class="page-title">Update Consent</h1>

    <section class="consent-section">
      <p>Current State: <p>{{ current_consent }}</p></p> 
      <form @submit.prevent="updateConsent">
        <div class="form-group">
          <label for="consent-status">Switch to:</label>
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
import { defineComponent, watch, ComponentPublicInstance } from 'vue';
import axios from 'axios';
import { useRouter, RouteLocationNormalized, NavigationGuardNext} from 'vue-router';
import globalData from '../globalData'

export default defineComponent({
  name: 'ConsentUpdate',
  data() {
    return {
      consentStatus: 'true',
      message: '',
      error: '',
      current_consent: '',
    };
  },

  mounted() {
    this.getConsentStatus();
  },

  methods: {
    async updateConsent() {
      try {
        const response = await axios.post(
          `http://localhost:5000/patients/consent/${globalData.user_id}`,
          {
            consent_status: this.consentStatus === 'true',
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          }
        );
        this.getConsentStatus();
        this.message = response.data.message || 'Consent updated successfully.';
        this.error = '';
      } catch (err) {
        this.error = err.response?.data.error || 'Failed to update consent.';
        this.message = '';
      }
    },

    async getConsentStatus() {
      try {
        const response = await axios.get(
          `http://localhost:5000/patients/consent/current/${globalData.user_id}`,
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          }
        );

        this.current_consent = response.data.current_consent;

      } catch (err) {
        this.error = err.response?.data.error || 'Failed to get current state of consent.';
        this.message = '';
      }
    },
  },

  beforeRouteEnter(
    to: RouteLocationNormalized,
    from: RouteLocationNormalized,
    next: NavigationGuardNext) {
    
      next((vm) => {
        (vm as ComponentPublicInstance & { getConsentStatus: () => void }).getConsentStatus();
      });
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
