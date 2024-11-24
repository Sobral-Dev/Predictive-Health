<template>
  <main>
    <transition name="fade" mode="out-in">

      <div class="user-registration">
        <h1 class="page-title">Register New User</h1>

        <section class="form-section">
          <form @submit.prevent="registerUser">
            <div class="form-group">
              <label for="name">Name</label>
              <input 
                type="text" 
                id="name" 
                v-model="form.name" 
                required 
                class="form-control"
              />
            </div>

            <div class="form-group">
              <label for="email">Email</label>
              <input 
                type="email" 
                id="email" 
                v-model="form.email" 
                required 
                class="form-control"
              />
            </div>

            <div class="form-group">
              <label for="password">Password</label>
              <input 
                type="password" 
                id="password" 
                v-model="form.password" 
                required 
                class="form-control"
              />
            </div>

            <div class="form-group">
              <label for="role">Role</label>
              <select id="role" v-model="form.role" class="form-control" required>
                <option value="admin">Admin</option>
                <option value="medico">Medico</option>
                <option value="paciente">Paciente</option>
              </select>
            </div>

            <div class="form-group">
              <label for="cpf">CPF</label>
              <input 
                type="text" 
                id="cpf" 
                v-model="form.cpf" 
                required
                @input="formatCPF"
                placeholder="000.000.000-00" 
                class="form-control"
              />
            </div>

            <button type="submit" class="submit-button">Register User</button>
          </form>

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
import eventBus from '../eventBus';

export default defineComponent({
  name: 'UserRegistration',
  data() {
    return {
      form: {
        name: '',
        email: '',
        password: '',
        role: 'admin',
        cpf: '',
      },
      message: '',
      error: '',
    };
  },

  methods: {
    async registerUser() {
      try {
        const response = await axios.post(
          'http://localhost:5000/register_user',
          {
            name: this.form.name,
            email: this.form.email,
            password: this.form.password,
            role: this.form.role,
            cpf: this.form.cpf.replace(/\D/g, '')
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          }
        );

        this.message = response.data.message || 'User registered successfully.';
        this.error = '';
        this.resetForm();
        eventBus.usersUpdated = true;
      } catch (err) {
        this.error = err.response?.data.error || 'Failed to register user.';
        this.message = '';
      }
    },
    resetForm() {
      this.form.name = '';
      this.form.email = '';
      this.form.password = '';
      this.form.role = 'admin';
      this.form.cpf = '';
    },
  },

    formatCPF() {
      // Remove qualquer caractere que não seja número
      this.form.cpf = this.form.cpf.replace(/\D/g, '');
      
      // Aplica a máscara do CPF manualmente
      if (this.form.cpf.length <= 3) {
        this.form.cpf = this.form.cpf.replace(/(\d{3})/, '$1');
      } else if (this.form.cpf.length <= 6) {
        this.form.cpf = this.form.cpf.replace(/(\d{3})(\d{1,3})/, '$1.$2');
      } else if (this.form.cpf.length <= 9) {
        this.form.cpf = this.form.cpf.replace(/(\d{3})(\d{3})(\d{1,3})/, '$1.$2.$3');
      } else {
        this.form.cpf = this.form.cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{1,2})/, '$1.$2.$3-$4');
      }
    },
  
});
</script>

<style scoped>
.user-registration {
  /* Estilos da página de registro de usuário */
}

.page-title {
  /* Estilos para o título da página */
}

.form-section {
  margin-top: 20px;
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
