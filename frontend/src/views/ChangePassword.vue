<template>
  <div class="change-password">
    <h1 class="page-title">Change Password</h1>

    <section class="password-section">
      <form @submit.prevent="changePassword">
        <div class="form-group">
          <label for="old-password">Old Password</label>
          <input 
            type="password" 
            id="old-password" 
            v-model="oldPassword" 
            required 
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label for="new-password">New Password</label>
          <input 
            type="password" 
            id="new-password" 
            v-model="newPassword" 
            required 
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label for="confirm-password">Confirm New Password</label>
          <input 
            type="password" 
            id="confirm-password" 
            v-model="confirmPassword" 
            required 
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label for="reset-token">Enter the Reset Token Received</label>
          <input 
            type="text" 
            id="reset-token" 
            v-model="resetToken" 
            required 
            class="form-control"
          />
        </div>

        <button type="submit" class="submit-button">Change Password</button>
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
import globalData from '../globalData';

export default defineComponent({
  name: 'ChangePassword',
  data() {
    return {
      oldPassword: '',
      newPassword: '',
      confirmPassword: '',
      resetToken: '',
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
      }
    );
  },

  methods: {
    async changePassword() {
      if (this.newPassword !== this.confirmPassword) {
        this.error = 'New password and confirm password do not match.';
        return;
      }

      try {
        const response = await axios.put(
          'http://localhost:5000/user/change-password',
          {
            user_id: globalData.user_id,
            reset_token: this.resetToken,
            new_password: this.newPassword,
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          }
        );
        this.message = response.data.message || 'Password changed successfully.';
        this.error = '';
      } catch (err) {
        this.error = err.response.data.error || 'Failed to change password.';
        this.message = '';
      }
    },
  },
  
});
</script>

<style scoped>
.change-password {
  /* Estilos da página de mudança de senha */
}

.page-title {
  /* Estilos para o título da página */
}

.password-section {
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
