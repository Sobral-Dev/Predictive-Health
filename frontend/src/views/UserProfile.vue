<template>
  <div class="user-profile">
    <h1 class="page-title">User Profile</h1>

    <section class="profile-section" v-if="user">
      <div class="profile-item">
        <label>Name:</label>
        <span>{{ user.name }}</span>
      </div>

      <div class="profile-item">
        <label>Email:</label>
        <span>{{ user.email }}</span>
      </div>

      <div class="profile-item">
        <label>Role:</label>
        <span>{{ user.role }}</span>
      </div>

      <div class="profile-item">
        <label>Consent Status:</label>
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
        <label>With Patient History:</label>
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
        <label>Created At:</label>
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
          <label for="name">Name</label>
          <input 
            type="text" 
            id="name" 
            v-model="user.name" 
            required 
            class="form-control"
          />
        </div>

        <div class="form-group">
          <label for="email">Email</label>
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

    <p v-if="error" class="error">{{ error }}</p>
    <p v-if="message" class="message">{{ message }}</p>
  </div>
</template>

<script lang="ts">
import { defineComponent, watch, ComponentPublicInstance } from 'vue';
import axios from 'axios';
import { useRouter, RouteLocationNormalized, NavigationGuardNext} from 'vue-router';
import globalData from '../globalData';

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
      gd: globalData,
    };
  },

  mounted() {
    this.fetchUserProfile();
  },

  created() {
    watch(
      () => globalData.user_consent,
      (newConsent) => {
        this.gd.user_consent = newConsent;
      }
    );
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

.profile-item {
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
