<template>
  <main>
    <transition name="fade" mode="out-in">
      <div class="audit-logs">
        <h1 class="page-title">Audit Logs</h1>

        <section class="logs-section">
          <table class="logs-table">
            <thead>
              <tr>
                <th>User ID</th>
                <th>Action</th>
                <th>Timestamp</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="log in paginatedLogs" :key="log.id">
                <td>{{ log.user_id }}</td>
                <td>{{ log.action }}</td>
                <td>{{ new Date(log.timestamp).toLocaleString("pt-BR") }}</td>
              </tr>
            </tbody>
          </table>

          <div class="pagination">
            <button @click="prevPage" :disabled="currentPage === 1">Anterior</button>
            <span>Página {{ currentPage }} de {{ totalPages }}</span>
            <button @click="nextPage" :disabled="currentPage === totalPages">Próxima</button>
          </div>
        </section> 
      </div>
    </transition>
  </main>
</template>

<script lang="ts">
import { defineComponent, watch, ComponentPublicInstance } from 'vue';
import axios from 'axios';
import { RouteLocationNormalized, NavigationGuardNext} from 'vue-router';

export default defineComponent({
  name: 'AuditLogs',
  data() {
    return {
      logs: [],
      currentPage: 1, 
      logsPerPage: 10,
    };
  },

  mounted() {
    this.fetchAuditLogs();
  },

  methods: {
    async fetchAuditLogs() {
      try {
        const response = await axios.get('http://localhost:5000/audit-log', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        this.logs = response.data.logs;
      } catch (error) {
        console.error('Failed to fetch audit logs:', error);
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
    paginatedLogs() {
      const start = (this.currentPage - 1) * this.logsPerPage;
      const end = start + this.logsPerPage;
      return this.logs.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.logs.length / this.logsPerPage);
    }
  },

  beforeRouteEnter(
    to: RouteLocationNormalized,
    from: RouteLocationNormalized,
    next: NavigationGuardNext) {
    
      next((vm) => {
        (vm as ComponentPublicInstance & { fetchAuditLogs: () => void }).fetchAuditLogs();
      });
  },

});
</script>

<style scoped>
.audit-logs {
  /* Estilos da página de logs de auditoria */
}

.page-title {
  /* Estilos para o título da página */
}

.logs-section {
  /* Estilos para a seção de logs */
}

.logs-table {
  width: 100%;
  border-collapse: collapse;
}

.logs-table th,
.logs-table td {
  padding: 12px;
  border: 1px solid #ccc;
}

.logs-table th {
  background-color: #f4f4f4;
  font-weight: bold;
}

.logs-table tr:nth-child(even) {
  background-color: #f9f9f9;
}
</style>
