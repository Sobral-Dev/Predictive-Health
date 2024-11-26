<template> 
  <transition name="fade" mode="out-in">
    <main>
      <div class="user-profile">
        <h1 class="page-title">User Profile</h1>

        <section class="profile-section" v-if="user">
          <div class="profile-item">
            <label><b>Name: </b></label>
            <span>{{ user.name }}</span>
          </div>

          <div class="profile-item">
            <label><b>Email: </b></label>
            <span>{{ user.email }}</span>
          </div>

          <div class="profile-item">
            <label><b>Role: </b></label>
            <span>{{ user.role }}</span>
          </div>

          <div class="profile-item">
            <label><b>Consent Status: </b></label>
            <span>
              {{
                user.consent_status === true
                  ? 'Given'
                  : user.consent_status === false
                  ? 'Revoked'
                  : "Hasn't got a patient history yet"
              }}
            </span>
          </div>

          <div class="profile-item">
            <label><b>With Patient History: </b></label>
            <span>
              {{
                user.has_patient_history === true
                  ? 'Yes'
                  : user.has_patient_history === false
                  ? 'No'
                  : "Hasn't got a patient history yet"
              }}
            </span>
          </div>

          <div class="profile-item">
            <label><b>Created At: </b></label>
            <span>
              {{ user.created_at }}
            </span>
          </div>      

          <button @click="editProfile" class="edit-button">Edit Profile</button>
        </section>

        <section class="edit-section" v-if="isEditing">
          <h2>Edit Profile</h2>
          <form @submit.prevent="updateProfile">
            <div class="form-group">
              <label for="name"><b>Name </b></label>
              <input 
                type="text" 
                id="name" 
                v-model="user.name" 
                required 
                class="form-control"
              />
            </div>

            <div class="form-group">
              <label for="email"><b>Email </b></label>
              <input 
                type="email" 
                id="email" 
                v-model="user.email" 
                required 
                class="form-control"
              />
            </div>

            <button type="submit" class="submit-button">Save Changes</button>
            <button @click="cancelEdit" class="cancel-button">Cancel</button>
          </form>
        </section>

        <section class="patient-section" v-if="patient && this.globalData.user_role === 'paciente'">

          <h1 class="page-title">Patient Profile</h1>
          
          <br>

          <div class="patient-item">          
            <label><b>Name: </b></label>
            <span>{{ patient.name }}</span>
          </div>

          <div class="patient-item">
            <label><b>Age: </b></label>
            <span>{{ patient.age }}</span>
          </div>

          <div class="patient-item">
            <label><b>Role: </b></label>
            <span>{{ patient.medical_conditions }}</span>
          </div>

          <div class="patient-item">
            <label><b>Role: </b></label>
            <span>{{ patient.created_at }}</span>
          </div>
        </section>

        <section v-if="doctors.length > 0 && (this.globalData.user_role === 'paciente' || this.globalData.user_role === 'medico')" class="doctor-section">

          <h1 class="page-title">Associate {{ this.globalData.user_role === 'paciente' ? 'Doctors' : 'Patients' }}</h1>

          <br>

          <ul v-for="doctor in doctors" :key="doctor.id">
            <li><b>{{ this.globalData.user_role === 'paciente' ? 'D' : 'S' }}r(a)</b> {{ doctor.name }}</li>
          </ul>

        </section>

        <p v-if="error" class="error">{{ error }}</p>
        <p v-if="message" class="message">{{ message }}</p>
      </div>
    </main>
  </transition>
</template>

<script lang="ts">
import { defineComponent, watch, ComponentPublicInstance } from 'vue';
import axios from 'axios';
import { RouteLocationNormalized, NavigationGuardNext} from 'vue-router';

export default defineComponent({
  name: 'UserProfile',
  data() {
    return {
      user: {
        name: '',
        email: '',
        role: '',
        consent_status: null,
        has_patient_history: null,
        created_at: Date,
      },
      isEditing: false,
      error: '',
      message: '',
      globalData: {
        user_id: localStorage.getItem('gd.user_id'),
        user_role: localStorage.getItem('gd.user_role')
      },
      patient: [],
      doctors: []
    };
  },

  mounted() {
    this.fetchUserProfile();
    this.fetchPatientProfile();
    this.fetchPatientDoctors();
  },

  methods: {
    async fetchUserProfile() {
      try {
        const response = await axios.get('http://localhost:5000/user/me', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        this.user = response.data;
      } catch (err) {
        this.error = err.response?.data.error || 'Failed to fetch user profile.';
      }
    },
    editProfile() {
      this.isEditing = true;
    },
    async updateProfile() {
      try {
        const response = await axios.put('http://localhost:5000/user/me', this.user, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`,
          },
        });
        this.message = response.data.message || 'Profile updated successfully.';
        this.error = '';
        this.isEditing = false;
      } catch (err) {
        this.error = err.response?.data.error || 'Failed to update profile.';
        this.message = '';
      }
    },
    cancelEdit() {
      this.isEditing = false;
      this.fetchUserProfile();
    },

    async fetchPatientProfile() {

      if (this.globalData.user_role !== 'paciente') {
        return this.patient = {};
      } else {
        try {
          const response = await axios.get(`http://localhost:5000/patients/${this.globalData.user_id}/paciente`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          });
          this.patient = response.data;
        } catch (err) {
          this.error = err.response?.data.error || 'Failed to fetch patient profile.';
        }
      };
     
    },

    async fetchPatientDoctors() {

      if (this.globalData.user_role !== 'paciente') {
       
        if (this.globalData.user_role === 'medico') {

          try {
            const response = await axios.get(`http://localhost:5000/doctor/${this.globalData.user_id}/patients`, {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
              },
            });
            this.doctors = response.data;
          } catch (err) {
            this.error = err.response?.data.error || 'Failed to fetch user associate patients.';
            this.doctors = {};
          }
        } else {
          return this.doctors = {};
        };
      } else {
        try {
          const response = await axios.get(`http://localhost:5000/patient/doctors`, {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`,
            },
          });
          this.doctors = response.data;
        } catch (err) {
          this.error = err.response?.data.error || 'Failed to fetch user associate doctors.';
          this.doctors = {};
        }
      };
    },
  
  },

  beforeRouteEnter(
    to: RouteLocationNormalized,
    from: RouteLocationNormalized,
    next: NavigationGuardNext) {
    
      next((vm) => {
        (vm as ComponentPublicInstance & { fetchUserProfile: () => void }).fetchUserProfile();
      });
  },

});
</script>

<style scoped>
.user-profile {
  /* Estilos da página de perfil do usuário */
}

.page-title {
  /* Estilos para o título da página */
}

.profile-section {
  margin-top: 20px;
}

.profile-item, .patient-item {
  margin-bottom: 15px;
}

.edit-section {
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

.submit-button, .cancel-button {
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
