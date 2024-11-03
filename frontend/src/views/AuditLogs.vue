<template>
  <div class="audit-logs">
    <h1 class="page-title">Audit Logs</h1>

    <section class="logs-section">
      <table class="logs-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>User ID</th>
            <th>Action</th>
            <th>Timestamp</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="log in logs" :key="log.id">
            <td>{{ log.id }}</td>
            <td>{{ log.user_id }}</td>
            <td>{{ log.action }}</td>
            <td>{{ log.timestamp }}</td>
          </tr>
        </tbody>
      </table>
    </section>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import axios from 'axios';

export default defineComponent({
  name: 'AuditLogs',
  data() {
    return {
      logs: [] as Array<{
        id: number;
        user_id: number;
        action: string;
        timestamp: string;
      }>,
    };
  },
  methods: {
    async fetchAuditLogs() {
      try {
        const response = await axios.get('http://localhost:5000/audit-log', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        this.logs = response.data;
      } catch (error) {
        console.error('Failed to fetch audit logs:', error);
      }
    },
  },
  mounted() {
    this.fetchAuditLogs();
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
