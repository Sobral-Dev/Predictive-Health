<template>
  <!-- Menu lateral -->
  <div class="sidebar">
    <div class="logo">
      <p class="logo-text">
       PREDICTIVE <br>
       HEALTH</p>
    </div>

    <nav class="links">
      <RouterLink to="/dashboard" v-if="this.globalData.user_role === 'admin' && this.globalData.user_id !== null">
      <img
        src="../assets/icons/dashboard.png"
        class="icon_img"
        height="50px"
      />  
      Dashboard</RouterLink>
      <RouterLink to="/audit-logs" v-if="this.globalData.user_role === 'admin' && this.globalData.user_id !== null">
        <img
        src="../assets/icons/audit-logs.png"
        class="icon_img"
        height="50px"
        /> 
        Audit Logs</RouterLink>
      <RouterLink to="/doctor-patient-list" v-if="this.globalData.user_role === 'medico' && this.globalData.user_id !== null">
        <img
        src="../assets/icons/dashboard.png"
        class="icon_img"
        height="50px"
        /> 
        Your Patients</RouterLink>
      <RouterLink to="/health-prediction" v-if="this.globalData.user_role === 'paciente' && this.globalData.user_id !== null">
        <img
        src="../assets/icons/health-prediction.png"
        class="icon_img"
        height="45px"
        style="margin-left: 2px; margin-right: 2px;"
        /> 
        Predictions</RouterLink>
      <RouterLink to="/admin-predictions" v-if="this.globalData.user_role === 'admin' && this.globalData.user_id !== null">
        <img
        src="../assets/icons/health-prediction.png"
        class="icon_img"
        height="45px"
        style="margin-left: 2px; margin-right: 2px;"
        /> 
        Predictions</RouterLink>
      <RouterLink to="/doctor-predictions" v-if="this.globalData.user_role === 'medico' && this.globalData.user_id !== null">
        <img
        src="../assets/icons/health-prediction.png"
        class="icon_img"
        height="45px"
        style="margin-left: 2px; margin-right: 2px;"
        /> 
        Predictions</RouterLink>
      <RouterLink to="/user-predictions" v-if="this.globalData.user_role === 'paciente' && this.globalData.user_id !== null">
        <img
        src="../assets/icons/audit-logs.png"
        class="icon_img"
        height="45px"
        style="margin-left: 2px; margin-right: 2px;"
        /> 
        Your History</RouterLink>
      <RouterLink to="/export-data/:id" v-if=" this.globalData.user_id !== null">
        <img
        src="../assets/icons/personal-data-export.png"
        class="icon_img"
        height="40px"
        style="margin-left: 5px; margin-right: 4px;"
        /> 
        Personal Data</RouterLink>
      <RouterLink to="/register-patient" v-if="(this.globalData.user_role === 'admin' || this.globalData.user_role === 'medico') && this.globalData.user_id !== null">
        <img
        src="../assets/icons/register-patient.png"
        class="icon_img"
        height="50px"
        /> 
        Register Patient</RouterLink>
      <RouterLink to="/patients" v-if="(this.globalData.user_role === 'admin' || this.globalData.user_role === 'medico') && this.globalData.user_id !== null">
        <img
        src="../assets/icons/show-patients.png"
        class="icon_img"
        height="45px"
        style="margin-right: 4px;"
        /> 
        Patients</RouterLink>
      <RouterLink to="/profile" v-if="this.globalData.user_id !== null">
        <img
        src="../assets/icons/profile.png"
        class="icon_img"
        height="50px"
        /> 
        User Profile</RouterLink>
      <RouterLink to="/manage-users" v-if="this.globalData.user_role === 'admin' && this.globalData.user_id !== null">
        <img
        src="../assets/icons/manage-users.png"
        class="icon_img"
        height="50px"
        /> 
        Manage Users</RouterLink>
      <RouterLink to="/register-user" v-if="this.globalData.user_role === 'admin' && this.globalData.user_id !== null">
        <img
        src="../assets/icons/register-patient.png"
        class="icon_img"
        height="50px"
        /> 
        Register User</RouterLink>
      <RouterLink to="/change-password" v-if=" this.globalData.user_id !== null">
        <img
        src="../assets/icons/change-password.png"
        class="icon_img"
        height="50px"
        /> 
        Password</RouterLink>
      <RouterLink to="/consent-update/:id" v-if="this.globalData.user_id !== null">
        <img
        src="../assets/icons/consent-update.png"
        class="icon_img"
        height="50px"
        /> 
        Consent Update</RouterLink>
      <a @click="logout()" style="cursor: pointer;" v-if="this.globalData.user_id !== null">
        <img
        src="../assets/icons/login.png"
        class="icon_img"
        height="50px"
        /> 
        Logout</a>
    </nav>
  </div>
</template>

<script lang="ts">
import { RouterLink } from 'vue-router';
import { useRouter } from 'vue-router';
import { watch } from 'vue';
import globalData from '../globalData';

export default {
  data() {
    return {
      animationDelay: false,
      globalData: globalData,
    }
  },

  setup() {
    const router = useRouter();
    return { router };
  },

  created() {
    watch(
      () => globalData.user_role,
      (newRole) => {
        this.globalData.user_role = newRole;
        localStorage.setItem('gd.user_role', this.globalData.user_role)
      }
    );
  },

  methods: {
    changeAnimationDelay() {
      this.animationDelay = true
    },

    logout() {
      this.globalData.user_id = null;
      this.globalData.user_role = null;
      this.globalData.user_name = null;
      this.globalData.isAuthenticated = false;
      this.globalData.user_consent = null;
      this.globalData.has_patient_history = null;

      localStorage.setItem('gd.user_id', this.globalData);
      localStorage.setItem('gd.user_role', this.globalData.user_role);
      localStorage.setItem('gd.user_name', this.globalData.user_name);
      localStorage.setItem('gd.isAuthenticated', this.globalData.isAuthenticated);
      localStorage.setItem('gd.user_consent', this.globalData.user_consent);
      localStorage.setItem('gd.has_patient_history', this.globalData.has_patient_history);

      this.router.push({ name: 'Login' });
    },

  },

}
</script>

<style>
@import '../assets/css/base.css';

.sidebar:not(.logo) {
  position: fixed;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 2rem;
  top: 0;
  left: 0;
  width: calc(100vw - 80vw);
  height: 100vh;
  background-color: var(--azul-acizentado-0-5);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3), 
              0 5px 4px rgba(39, 174, 96, 0.85);
  overflow-y: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.sidebar::-webkit-scrollbar {
  display: none; 
}

.sidebar:hover {
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.4), 0 3px 6px rgba(39, 174, 96, 0.3);
  transition: box-shadow 0.3s ease;
}

.logo {
  background-color: transparent;
  height: auto;
  width: auto;
  font-size: 2rem;
  font-weight: 600;
  color: var(--branco-auxiliar);
  margin-right: 30%;
}

.links {
  width: calc(25vw - 1.5vw);
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  font-size: 1.3rem;
  text-align: center;
  font-weight: 800;
  margin-left: calc(20vw - 18.5vw);
}

.links a.router-link-exact-active,
.links a.router-link-exact-active i {
  transition: all 0.5s;
  color: var(--verde-contraste);
  background-color: transparent;
}

.links a.router-link-exact-active i {
  transition: all 0.5s;
}

.links a.router-link-exact-active:hover {
  transition: all 0.5s;
  padding-left: 0.8%;
}

.links a {
  transition: all 0.5s;
  color: var(--verde-contraste-0-8);
  text-decoration: none;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: center;
  margin-left: 8%;
}

.links a:hover:not(nav a.router-link-exact-active:hover) {
  transition: all 0.5s;
  padding-left: 2%;
}

.icon_img {
  padding-right: 1%;
}
</style>
