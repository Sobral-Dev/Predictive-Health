<template>
  <main>
    <transition name="fade" mode="out-in">

      <div class="users-management">
        <h1 class="page-title">Users Management</h1>

        <section class="users-section">
          <table class="users-table">
            <thead>
              <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Role</th>
                <th>Created At</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="user in paginated" :key="user.id" :title="`id: ${user.id}`">
                <td>{{ user.name }}</td>
                <td>{{ user.email }}</td>
                <td>{{ user.role }}</td>
                <td>{{ new Date(user.created_at).toLocaleString("pt-BR") }}</td>
                <td>
                  <button @click="deleteUser(user.id)" class="action-button">Delete</button>
                </td>
              </tr>
            </tbody>
          </table>
        </section>

        <div class="pagination">
            <button @click="prevPage" :disabled="currentPage === 1">Anterior</button>
            <span>Página {{ currentPage }} de {{ totalPages }}</span>
            <button @click="nextPage" :disabled="currentPage === totalPages">Próxima</button>
        </div>

        <p v-if="error" class="error">{{ error }}</p>
        <p v-if="message" class="message">{{ message }}</p>
      </div>
    </transition>
  </main>
</template>

<script lang="ts">
import { defineComponent, ComponentPublicInstance } from 'vue';
import axios from 'axios';
import { RouteLocationNormalized, NavigationGuardNext} from 'vue-router';

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
      error: '',
      message: '',
      currentPage: 1, 
      perPage: 10,
    };
  },

  mounted() {
    this.fetchUsers();
  },

  methods: {

    async fetchUsers() {
      try {
        const response = await axios.get('http://localhost:5000/users', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        this.users = response.data.users;
      } catch (err) {
        this.error = err.response?.data.error || 'Failed to fetch users list.';
      }
    },
   
    async deleteUser(userId: number) {
      try {
        await axios.delete(`http://localhost:5000/users/${userId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        this.fetchUsers();
      } catch (err) {
        this.error = err.response?.data.error || 'Failed to delete user.';
      }
    },

    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },

    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    },

  },

  computed: {
    paginated() {
      const start = (this.currentPage - 1) * this.perPage;
      const end = start + this.perPage;
      return this.users.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.users.length / this.perPage);
    }
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
