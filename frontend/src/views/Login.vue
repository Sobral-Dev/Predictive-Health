<template>
  <main>
    <transition name="fade" mode="out-in">

      <div class="login">
        <h1 class="page-title">Login</h1>

        <section class="login-section">
          <form v-if="!emailSender" @submit.prevent="loginUser">
            <div class="form-group">
              <label for="email">Email</label>
              <input 
                type="email" 
                id="email" 
                v-model="email" 
                required 
                class="form-control"
              />
            </div>

            <div class="form-group">
              <label for="password">Password</label>
              <input 
                type="password" 
                id="password" 
                v-model="password" 
                required 
                class="form-control"
              />
            </div>

            <button type="submit" class="submit-button">Login</button>
          </form>

          <form v-if="emailSender" @submit.prevent="this.requestPasswordReset">
            <div class="form-group">
                <label for="password">Your Email</label>
                <input 
                  type="password" 
                  id="password" 
                  v-model="emailToResetPassword" 
                  required 
                  class="form-control"
                />
              </div>

              <button type="submit" class="submit-button">Submit</button>
              <button class="submit-button" @click="this.emailSender = false; this.emailToResetPassword = '';">Return</button>
          </form>
          
          <button v-if="!emailSender" @click="this.emailSender = true;" class="submit-button">Forgot Password</button>

          <p v-if="message" class="message">{{ message }}</p>
          <p v-if="error" class="error">{{ error }}</p>
        </section>
      </div>
    </transition>
  </main>  
</template>

<script lang="ts">
import { defineComponent, watch, ComponentPublicInstance } from 'vue';
import axios from 'axios';
import { useRouter, RouteLocationNormalized, NavigationGuardNext} from 'vue-router';
import globalData from '../globalData';
import eventBus from '../eventBus';

export default defineComponent({
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      error: '',
      message: '',
      emailToResetPassword: '',
      gd: globalData,
      emailSender: false,
    };
  },

  setup() {
    const router = useRouter();
    return { router };
  },

  created() {
    watch(
      () => globalData.user_consent,
      (newConsent) => {
        this.gd.user_consent = newConsent;
      }
    );
  },

  methods: {
    async loginUser() {
      try {
        const response = await axios.post('http://localhost:5000/login', {
          email: this.email,
          password: this.password,
        });

        // Save the JWT token in local storage
        localStorage.setItem('token', response.data.access_token);

        // Save response data for succeed login in a global variable
        globalData.user_id = response.data.user_id;
        globalData.user_role = response.data.user_role;
        globalData.user_name = response.data.user_name;
        globalData.isAuthenticated = true;
        globalData.user_consent = response.data.consent_status
        globalData.has_patient_history = response.data.has_patient_history

        // Navigate to the appropriate page based on user role
        this.navigateToDashboard(response.data.user_role, response.data.consent_status, response.data.user_id);
      } catch (err) {
        this.error = err.response?.data.error || err;
      }
    },

    navigateToDashboard(role: string, consent_status: string | null, id: number) {

      if (consent_status === null) {
        return this.router.push(`/initial-consent/${id}`);
      } 

      if (role === 'admin') {
        return this.router.push({ name: 'AdminDashboard' });
      } else if (role === 'medico') {
        return this.router.push({ name: 'ShowPatients' });
      } else {
        return this.router.push({ name: 'UserProfile' });
      }
    },
  },

  async requestPasswordReset() {
      try {
        const response = await axios.post('http://localhost:5000/password-reset-request', { email: this.emailToResetPassword });
        this.emailSender = false;
        this.emailToResetPassword = '';
        this.message = response.data.message;
      } catch (error) {
        this.message = error.response?.data.error || 'Error during password reset request';
      }
    },
  
});
</script>

<style scoped>
.login {
  /* Estilos da página de login */
}

.page-title {
  /* Estilos para o título da página */
}

.login-section {
  /* Estilos da seção de login */
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

.error {
  color: red;
  margin-top: 10px;
}
</style>
