<template>
  <main>
    <transition name="fade" mode="out-in">

      <div class="login">
        <h1 class="page-title">{{ emailSender || this.$route.query.emailSender === 'true' ? 'Send Reset Token' : 'Login' }}</h1>

        <section class="login-section">
          <form v-if="!emailSender && this.$route.query.emailSender !== 'true'" @submit.prevent="loginUser">
            <div class="form-group">
              <label for="email">Email</label>
              <input 
                type="email" 
                id="email" 
                v-model="email" 
                required 
                placeholder="Type your email..."
                class="form-control"
              />
            </div>

            <div class="form-group">
              <select v-model="authWay" 
              style="color: rgba(39, 174, 96, 1); 
                    font-optical-sizing: auto;
                    font-weight: 400;
                    font-style: normal;
                    font-size: 21px;
                    background-color: transparent;
                    line-height: 1;
                    text-rendering: optimizeLegibility;
                    text-align: initial;
                    vertical-align: super;"
                    >
                <option value="password" style="color: rgba(39, 174, 96, 1);">Password</option>
                <option value="reset_token" style="color: rgba(39, 174, 96, 1);">Reset Token</option>
              </select>
              <input 
                type="password" 
                :id="authWay === 'password' ? 'password' : 'reset_token'" 
                v-model="password" 
                :placeholder="authWay === 'password' ? 'Type your password...' : 'Type your reset token...'" 
                required 
                class="form-control"
              />
            </div>

            <button type="submit" class="submit-button">Login</button>
          </form>

          <form v-if="emailSender || this.$route.query.emailSender === 'true'" @submit.prevent="requestPasswordReset">
            <div class="form-group">
                <label for="emailReset">Your Email</label>
                <input 
                  type="email" 
                  id="emailReset" 
                  v-model="emailToResetPassword" 
                  required 
                  class="form-control"
                />
              </div>

              <button type="submit" class="submit-button">Submit</button>
              <button type="button" class="submit-button" @click.prevent="resetForm">Return</button>
          </form>
          
          <button type="button" v-if="!emailSender && this.$route.query.emailSender !== 'true'" @click.prevent="this.emailSender = true;" class="submit-button">Forgot Password</button>

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
import { useRouter } from 'vue-router';
import globalData from '../globalData';

export default defineComponent({
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      error: '',
      message: '',
      emailToResetPassword: '',
      globalData: globalData,
      emailSender: false,
      authWay: 'password',
    };
  },

  setup() {
    const router = useRouter();
    return { router };
  },

  created() {
    watch(
      () => this.globalData.user_consent,
      (newConsent) => {
        this.globalData.user_consent = newConsent;
        localStorage.setItem('gd.user_consent', this.globalData.user_consent)
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
        this.globalData.user_id = response.data.user_id;
        this.globalData.user_role = response.data.user_role;
        this.globalData.user_name = response.data.user_name;
        this.globalData.isAuthenticated = true;
        this.globalData.user_consent = response.data.consent_status
        this.globalData.has_patient_history = response.data.has_patient_history

        localStorage.setItem('gd.user_id', this.globalData.user_id);
        localStorage.setItem('gd.user_role', this.globalData.user_role);
        localStorage.setItem('gd.user_name', this.globalData.user_name);
        localStorage.setItem('gd.isAuthenticated', this.globalData.isAuthenticated);
        localStorage.setItem('gd.user_consent', this.globalData.user_consent);
        localStorage.setItem('gd.has_patient_history', this.globalData.has_patient_history);

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

    async requestPasswordReset() {
      try {
        const response = await axios.post('http://localhost:5000/password-reset-request', { email: this.emailToResetPassword });
        this.emailToResetPassword = '';
        this.message = response.data.message;
      } catch (error) {
        this.message = error.response?.data.error || 'Error during password reset request';
      }
    },

    resetForm() {
      this.emailSender = false;
      this.emailToResetPassword = '';
      this.message = '';
      this.error = '';
      if (this.$route.query.emailSender === 'true') {
        this.$router.push('/change-password');
      } else {
        this.$router.push('/');
      };
    },

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
