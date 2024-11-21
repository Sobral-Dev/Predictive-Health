<template>
  <main>
    <transition name="fade" mode="out-in">
      <div class="consent-update">
        <h1 class="page-title">Update Consent</h1>

        <section class="consent-section">

          <p v-if="$route.name === 'ConsentUpdate'">Current State: 
            <b :style="this.gd.user_consent ? 'color: blue;' : 'color: red;' ">
            {{ this.gd.user_consent ? 'Given' : 'Revoked' }}
            </b>
          </p>

          <p v-else class="initial-consent">
            We respect your privacy, so we need your consent for your data to be used to make health predictions. <br> 
            <b>Don't worry, you can change your consent status at any time and deleting your account will automatically anonymize your personal information.</b>
          </p> 

          <form @submit.prevent="updateConsent">
            <div class="form-group">
              <label for="consent-status">Switch to:</label>
              <select id="consent-status" v-model="consentStatus" class="form-control" required>
                <option value="null" disabled>Choose one...</option>
                <option value="true">Given</option>
                <option value="false">Revoked</option>
              </select>
            </div>

            <button type="submit" class="submit-button">Update Consent</button>
          </form>

          <p v-if="message" class="message">{{ message }}</p>
          <p v-if="error && error !== 'No Patient'" class="error">{{ error }}</p>
        </section>
      </div>
    </transition>
  </main>  
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
      consentStatus: null,
      message: '',
      error: '',
      gd: globalData,
    };
  },

  created() {
    watch(
      () => globalData.user_consent,
      (newConsent) => {
        this.gd.user_consent = newConsent;
        globalData.user_consent = newConsent;
      }
    );
  },

  setup() {
    const router = useRouter();
    return { router };
  },

  mounted() {
    this.getConsentStatus();
  },

  methods: {
    
    async updateConsent() {

      if (this.$route.name !== 'ConsentUpdate') {
        
        return this.initialConsent();
      
      } else {

        try {
          const response = await axios.post(
            `http://localhost:5000/update-consent`,
            {
              consent_status: this.consentStatus === 'true',
            },
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
              },
            }
          );
          this.gd.user_consent = this.consentStatus === 'true';
          globalData.user_consent = this.consentStatus === 'true';
          this.getConsentStatus();
          this.message = response.data.message || 'Consent updated successfully.';
          this.error = '';
        } catch (err) {
          this.error = err.response?.data.error || 'Failed to update consent.';
          this.message = '';
        }

      };

    },

    async getConsentStatus() {

      if (this.$route.name === 'ConsentUpdate') {
        
        try {
          const response = await axios.get(
            `http://localhost:5000/patients/consent/current`,
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
              },
            }
          );

          this.current_consent = response.data.current_consent;

        } catch (err) {
          this.error = 'No Patient';
        }

      };
    },

    async initialConsent() {
        try {
          const response = await axios.post(
            `http://localhost:5000/consent-initial`,
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
          globalData.user_consent = this.consentStatus === 'true';
          this.router.push(`/consent-update/${globalData.user_id}`)
        } catch (err) {
          this.error = err.response?.data.error || `Failed to update consent: ${err}`;
          this.message = '';
        }
    },

    beforeRouteEnter(
      to: RouteLocationNormalized,
      from: RouteLocationNormalized,
      next: NavigationGuardNext) {
      
        next((vm) => {
          (vm as ComponentPublicInstance & { getConsentStatus: () => void }).getConsentStatus();
        });

    },

  },

});
</script>

<style scoped>
@import '../assets/css/base.css';

.initial-consent {
  color: var(--azul-contraste);
}

.initial-consent b {
  color: var(--azul-vibrante);
}

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
