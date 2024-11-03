<template>
  <!-- Menu lateral -->
  <div class="sidebar">
    <div class="logo">
      <p class="logo-text">
       PREDICTIVE <br>
       HEALTH</p>
    </div>

    <nav class="links">
      <RouterLink to="/dashboard">
      <img
        src="../assets/icons/dashboard.png"
        class="icon_img"
        height="50px"
      />  
      Dashboard</RouterLink>
      <RouterLink to="/audit-logs">
        <img
        src="../assets/icons/audit-logs.png"
        class="icon_img"
        height="50px"
        /> 
        Audit Logs</RouterLink>
      <RouterLink to="/health-prediction">
        <img
        src="../assets/icons/health-prediction.png"
        class="icon_img"
        height="45px"
        style="margin-left: 2px; margin-right: 2px;"
        /> 
        Predictions</RouterLink>
      <RouterLink to="/patients/:id">
        <img
        src="../assets/icons/patient-details.png"
        class="icon_img"
        height="50px"
        > 
        Your Details</RouterLink>
      <RouterLink to="/export-data/:id">
        <img
        src="../assets/icons/personal-data-export.png"
        class="icon_img"
        height="40px"
        style="margin-left: 5px; margin-right: 4px;"
        /> 
        Personal Data</RouterLink>
      <RouterLink to="/register-patient">
        <img
        src="../assets/icons/register-patient.png"
        class="icon_img"
        height="50px"
        /> 
        Register Patient</RouterLink>
      <RouterLink to="/patients">
        <img
        src="../assets/icons/show-patients.png"
        class="icon_img"
        height="45px"
        style="margin-right: 4px;"
        /> 
        Patients</RouterLink>
      <RouterLink to="/profile">
        <img
        src="../assets/icons/profile.png"
        class="icon_img"
        height="50px"
        /> 
        User Profile</RouterLink>
      <RouterLink to="/manage-users">
        <img
        src="../assets/icons/manage-users.png"
        class="icon_img"
        height="50px"
        /> 
        Manage Users</RouterLink>
      <RouterLink to="/register-user">
        <img
        src="../assets/icons/register-patient.png"
        class="icon_img"
        height="50px"
        /> 
        Register User</RouterLink>
      <RouterLink to="/change-password">
        <img
        src="../assets/icons/change-password.png"
        class="icon_img"
        height="50px"
        /> 
        Password</RouterLink>
      <RouterLink to="/consent-update/:id">
        <img
        src="../assets/icons/consent-update.png"
        class="icon_img"
        height="50px"
        /> 
        Consent Update</RouterLink>
      <RouterLink to="/">
        <img
        src="../assets/icons/login.png"
        class="icon_img"
        height="50px"
        /> 
        Login</RouterLink>
    </nav>
  </div>
</template>

<script lang="ts">
import { RouterLink } from 'vue-router'

export default {
  data() {
    return {
      animationDelay: false
    }
  },

  methods: {
    changeAnimationDelay() {
      this.animationDelay = true
    }
  }
}
</script>

<style>
@import '../assets/css/base.css';

.sidebar:not(.logo) {
  position: fixed;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
  gap: 2rem;
  top: 0;
  left: 0;
  width: calc(100vw - 80vw);
  height: 100vh;
  background-color: var(--azul-acizentado-0-5);
  padding-top: 1.5%;
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
  display: absolute;
  background-color: transparent;
  height: 100%;
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
  transform: all 0.5s;
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
