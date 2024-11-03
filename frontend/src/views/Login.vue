<template>
  <div class="login">
    <h1 class="page-title">Login</h1>

    <section class="login-section">
      <form @submit.prevent="loginUser">
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

      <p v-if="error" class="error">{{ error }}</p>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';

export default defineComponent({
  name: 'Login',
  data() {
    return {
      email: '',
      password: '',
      error: '',
    };
  },

  setup() {
    const router = useRouter();
    return { router };
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

        // Navigate to the appropriate page based on user role
        this.navigateToDashboard(response.data.user_role);
      } catch (err) {
        this.error = err.response?.data.error || err;
      }
    },
    navigateToDashboard(role: string) {
      if (role === 'admin') {
        this.router.push({ name: 'AdminDashboard' });
      } else if (role === 'medico') {
        this.router.push({ name: 'ShowPatients' });
      } else {
        this.router.push({ name: 'UserProfile' });
      }
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
