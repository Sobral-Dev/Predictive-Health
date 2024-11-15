<template>
  <div class="users-management">
    <h1 class="page-title">Users Management</h1>

    <section class="users-section">
      <table class="users-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Email</th>
            <th>Role</th>
            <th>Consent Status</th>
            <th>Created At</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id">
            <td>{{ user.id }}</td>
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
            <td>{{ user.role }}</td>
            <td>
              {{
                user.consent_status === true
                  ? 'Given'
                  : user.consent_status === false
                  ? 'Revoked'
                  : "Hasn't got a patient history yet"
              }}
            </td>
            <td>{{ user.created_at }}</td>
            <td>
              <button @click="editUser(user)" class="action-button">Edit</button>
              <button @click="deleteUser(user.id)" class="action-button">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </section>

    <section v-if="isEditing" class="edit-user-section">
      <h2>Edit User</h2>
      <form @submit.prevent="updateUser">
        <div class="form-group">
          <label for="edit-name">Name</label>
          <input 
            type="text" 
            id="edit-name" 
            v-model="selectedUser.name" 
            required 
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label for="edit-email">Email</label>
          <input 
            type="email" 
            id="edit-email" 
            v-model="selectedUser.email" 
            required 
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label for="edit-role">Role</label>
          <select id="edit-role" v-model="selectedUser.role" class="form-control" required>
            <option value="admin">Admin</option>
            <option value="medico">Medico</option>
            <option value="paciente">Paciente</option>
          </select>
        </div>

        <button type="submit" class="submit-button">Save Changes</button>
        <button @click="cancelEdit" class="cancel-button">Cancel</button>
      </form>
    </section>

    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="message" class="message">{{ message }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, watch, ComponentPublicInstance } from 'vue';
import axios from 'axios';
import { useRouter, RouteLocationNormalized, NavigationGuardNext} from 'vue-router';
import eventBus from '../eventBus';
import globalData from '../globalData';

export default defineComponent({
  name: 'UsersManagement',
  data() {
    return {
      users: [] as Array<{
        id: number;
        name: string;
        email: string;
        role: string;
        has_patient_history: boolean;
        consent_status: boolean,
        created_at: Date,
      }>,
      selectedUser: {
        id: 0,
        name: '',
        email: '',
        role: '',
      },
      isEditing: false,
      error: '',
      message: '',
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

  mounted() {
    this.fetchUsers();

    watch(
      () => eventBus.usersUpdated, 
      (newValue) => {
        if (newValue) {
          this.fetchUsers();
          eventBus.usersUpdated = false;
        }
      }
    );
  },

  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get('http://localhost:5000/users', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        this.users = response.data;
      } catch (err) {
        this.error = err.response?.data.error || 'Failed to fetch users list.';
      }
    },
    editUser(user: { id: number; name: string; email: string; role: string }) {
      this.selectedUser = { ...user };
      this.isEditing = true;
    },
    async updateUser() {
      try {
        const response = await axios.put(`http://localhost:5000/users/${this.selectedUser.id}`, this.selectedUser, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        this.message = response.data.message || 'User updated successfully.';
        this.error = '';
        this.isEditing = false;
        eventBus.usersUpdated = true;
      } catch (err) {
        this.error = err.response?.data.error || 'Failed to update user.';
        this.message = '';
      }
    },
    async deleteUser(userId: number) {
      try {
        await axios.delete(`http://localhost:5000/users/${userId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        eventBus.usersUpdated = true;
      } catch (err) {
        this.error = err.response?.data.error || 'Failed to delete user.';
      }
    },
    cancelEdit() {
      this.isEditing = false;
      this.selectedUser = { id: 0, name: '', email: '', role: '' };
    },
  },

  beforeRouteEnter(
    to: RouteLocationNormalized,
    from: RouteLocationNormalized,
    next: NavigationGuardNext) {
    
      next((vm) => {
        (vm as ComponentPublicInstance & { fetchUsers: () => void }).fetchUsers();
      });
  },

});
</script>

<style scoped>
.users-management {
  /* Estilos da página de gerenciamento de usuários */
}

.page-title {
  /* Estilos para o título da página */
}

.users-section {
  margin-top: 20px;
}

.users-table {
  width: 100%;
  border-collapse: collapse;
}

.users-table th,
.users-table td {
  padding: 12px;
  border: 1px solid #ccc;
}

.users-table th {
  background-color: #f4f4f4;
  font-weight: bold;
}

.users-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.action-button {
  margin: 0 5px;
}

.edit-user-section {
  margin-top: 30px;
}

.form-group {
  margin-bottom: 15px;
}

.form-control {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
}

.submit-button,
.cancel-button {
  margin-top: 20px;
  margin-right: 10px;
}

.error {
  color: red;
  margin-top: 10px;
}

.message {
  color: green;
  margin-top: 10px;
}
</style>
