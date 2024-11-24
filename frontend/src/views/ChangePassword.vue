<template>
  <main>
    <transition name="fade" mode="out-in">
      
      <div class="change-password">
        <h1 class="page-title">Change Password</h1>

        <section class="password-section">
          <form @submit.prevent="changePassword">
            <div v-if="!usingResetToken" class="form-group">
              <label for="old-password">Old Password</label>
              <input 
                type="password" 
                id="old-password" 
                v-model="oldPassword" 
                 @required="!usingResetToken ? true : false" 
                class="form-control"
              />
            </div>

            <div v-if="usingResetToken" class="form-group">
              <label for="reset-token">Enter the Reset Token Received</label>
              <input 
                type="password" 
                id="reset-token" 
                v-model="resetToken" 
                @required="usingResetToken ? true : false" 
                class="form-control"
              />
            </div>

            <p v-if="!usingResetToken">Can't you remember? Use your <b>reset token</b> or <a @click.prevent="goToLogin" style="cursor: pointer; opacity: 0.6; color: rgba(52, 152, 219, 1);" :hover="'opacity: 1'"><b>request one here.</b></a></p>
            <button type="button" @click="usingResetToken ? usingResetToken = false : usingResetToken = true">{{ usingResetToken ? 'Back to Old Password' : 'Use your Reset Token' }}</button>

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

            <button type="submit" class="submit-button">Change Password</button>
          </form>

          <p v-if="message" class="message">{{ message }}</p>
          <p v-if="error" class="error">{{ error }}</p>
        </section>
      </div>
    </transition>
  </main>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';

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
      usingResetToken: false,
    };
  },

  methods: {

    async changePassword() {
      if (this.newPassword !== this.confirmPassword) {
        this.error = 'New password and confirm password do not match.';
        return;
      }

      if (this.usingResetToken) {

        try {
          const response = await axios.post(
            'http://localhost:5000/password-reset',
            {
              user_id: localStorage.getItem('gd.user_id'),
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
          this.resetToken = '';
          this.newPassword = '';
          this.oldPassword = '';
          this.confirmPassword = '';
          this.usingResetToken = false;
        } catch (err) {
          this.error = err.response.data.error || 'Failed to change password.';
          this.message = '';
        }

      } else {

        try {

          const response = await axios.put(
            'http://localhost:5000/user/change-password',
            {
              old_password: this.oldPassword,
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
          this.resetToken = '';
          this.newPassword = '';
          this.oldPassword = '';
          this.confirmPassword = '';
          this.usingResetToken = false;
        } catch (err) {
          this.error = err.response.data.error || 'Failed to change password.';
          this.message = '';

        }
      }
    },

    goToLogin() {
      this.$router.push({ 
        name: 'Login', 
        query: { emailSender: true } 
      });
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
