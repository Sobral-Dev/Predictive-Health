<template>
  <main>
    <transition name="fade" mode="out-in">
      <div class="admin-dashboard"> 
        <h1 class="dashboard-title">Admin Dashboard</h1>
        
        <section class="stats-section">
          <h2 class="section-title">Overview</h2>
          <div class="stats">
            <div class="stat-item">
              <h3 class="stat-title">Total Users</h3>
              <p class="stat-value">{{ totalUsers }}</p>
            </div>
            <div class="stat-item">
              <h3 class="stat-title">Total Patients</h3>
              <p class="stat-value">{{ totalPatients }}</p>
            </div>
          </div>
        </section>

        <section class="actions-section">
          <h2 class="section-title">Actions</h2>
          <button @click="goToUsersManagement" class="action-button">Manage Users</button>
          <button @click="goToPatientsManagement" class="action-button">Manage Patients</button>
          <button @click="goToAuditLogs" class="action-button">View Audit Logs</button>
        </section>
      </div>
    </transition>
  </main>
</template>

<script lang="ts">
import { defineComponent, watch, ComponentPublicInstance } from 'vue';
import axios from 'axios';
import { useRouter, RouteLocationNormalized, NavigationGuardNext} from 'vue-router';
import eventBus from '../eventBus';
import globalData from '../globalData';

export default defineComponent({
  name: 'AdminDashboard',
  data() {
    return {
      totalUsers: 0,
      totalPatients: 0,
      gd: globalData,
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

  mounted() {
    this.fetchDashboardData();

     watch(
      () => eventBus.usersUpdated, (newValue) => {
        if (newValue) {
           this.fetchDashboardData();
          eventBus.usersUpdated = false;
        }
      }
    );

    watch(() => eventBus.patientsUpdated, (newValue) => {
      if (newValue) {
        this.fetchDashboardData();
        eventBus.patientsUpdated = false; 
      }
    });
  },

  beforeRouteEnter(
    to: RouteLocationNormalized,
    from: RouteLocationNormalized,
    next: NavigationGuardNext) {
    
      next((vm) => {
        (vm as ComponentPublicInstance & { fetchDashboardData: () => void }).fetchDashboardData();
      });
  },

  methods: {
    async fetchDashboardData() {
      try {
        const usersResponse = await axios.get('http://localhost:5000/users', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        const patientsResponse = await axios.get('http://localhost:5000/patients', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });

        this.totalUsers = usersResponse.data.length;
        this.totalPatients = patientsResponse.data.length;
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error);
      }
    },
    goToUsersManagement() {
      this.router.push({ name: 'UsersManagement' });
    },
    goToPatientsManagement() {
      this.router.push({ name: 'ShowPatients' });
    },
    goToAuditLogs() {
      this.router.push({ name: 'AuditLogs' });
    },
  },

});
</script>

<style scoped>
.admin-dashboard {
  /* Estilos da página de dashboard */
}

.dashboard-title {
  /* Estilos para o título do dashboard */
}

.stats-section {
  /* Estilos da seção de estatísticas */
}

.section-title {
  /* Estilos para os títulos das seções */
}

.stats {
  /* Estilos do contêiner de estatísticas */
}

.stat-item {
  /* Estilos dos itens de estatísticas */
}

.stat-title {
  /* Estilos dos títulos de estatísticas */
}

.stat-value {
  /* Estilos para os valores de estatísticas */
}

.actions-section {
  /* Estilos da seção de ações */
}

.action-button {
  /* Estilos dos botões de ação */
}
</style>
