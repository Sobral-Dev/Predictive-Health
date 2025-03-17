<template>
  <div>
    <!-- Botão para abrir o pop-up -->
    <button @click="showConsentModal = true; fetchConsentRequests()" class="consent-button">Show Doctor Requests</button>

    <!-- Modal de Solicitações de Consentimento -->
    <div v-if="showConsentModal" class="modal-overlay">
      <div class="modal-content">
        <h2>Doctor Requests</h2>
        
        <!-- Lista de Solicitações -->
        <div class="request-container" v-if="consentRequests.length > 0">
          <div class="request-card" v-for="request in consentRequests" :key="request.id">
              <p><b>Doctor:</b> {{ request.doctor_name }}</p>
              <p>
                <b>Status: </b> 
                <i :style="request.consent_status === 'accepted' ? 'color: rgba(88, 101, 242, 1);' : 'color: rgba(241, 196, 15, 1);'">
                {{ request.consent_status === 'accepted' ? 'Accepted' : 'Pending' }}
                </i></p>
              
              <!-- Botões de Ação -->
              <div class="buttons-options">
                <button v-if="request.consent_status !== 'accepted'" @click="respondToConsent(request.id, 'accepted')" class="accept-button">Accept</button>
                <button v-if="request.consent_status === 'accepted'"@click="respondToConsent(request.id, 'rejected')" class="reject-button">Reject</button>
              </div>
            </div>
            <div class="buttons-options close">
                <button @click="showConsentModal = false" class="close-button">Close</button>
            </div>
        </div>
        
        <div class="request-container" v-else>
            <p style="margin: 0; padding: 0; text-align: center;">You haven't requests at this moment.</p>
            <div class="buttons-options close">
                <button @click="showConsentModal = false" class="close-button">Close</button>
            </div>
        </div>       
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import axios from 'axios';

export default {
  data() {
    return {
      showConsentModal: false,
      consentRequests: [] 
    };
  },
  mounted() {
    this.fetchConsentRequests();
  },
  methods: {

    async fetchConsentRequests() {
      try {
        const response = await axios.get('http://localhost:5000/doctor-patient/requests', {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });

        this.consentRequests = response.data;

        if (Array.isArray(this.consentRequests)) {
        const consentRequests = response.data;

        const patients_pending = consentRequests.filter(request => request.consent_status === 'pending');
        const patients_accepted = consentRequests.filter(request => request.consent_status === 'accepted');

        console.log('Pending Requests:', patients_pending);
        console.log('Accepted Requests:', patients_accepted);

        if (patients_pending.length > 0) {
            this.showConsentModal = true;
        }

        } 

      } catch (error) {
        console.error('Error when trying to fetch doctor requests:', error);
      }
    },

    async respondToConsent(requestId, status) {
      try {
        const response = await axios.post('http://localhost:5000/doctor-patient/consent', {
          doctor_patient_id: requestId,
          consent_status: status
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        console.log(response.data.message);

        const event = new Event("force-fetchPatientDoctors-refresh");
        window.dispatchEvent(event);

        this.fetchConsentRequests();

      } catch (error) {
        console.error('Error when trying answer the request:', error);
      }
    }
  }
};
</script>

<style scoped>
@import '../assets/css/base.css';

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

.modal-content {
  background-color: darkslategrey;
  padding: 15px 15px;
  border-radius: 10px;
  width: 400px;
  max-width: 90%;
  text-align: center;
  overflow-y: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
  min-height: 35vh;
  max-height: 80vh;
}

.consent-button,
.accept-button,
.reject-button,
.close-button {
  padding: 10px 15px;
  margin: 5px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.consent-button {
  background-color: #007bff;
  color: white;
  border-color: var(--azul-vibrante);
}

.consent-button:hover {
  background-color: #007bff;
  color: white;
}

.accept-button {
  background-color: #28a745;
  color: white;
}

.accept-button:hover {
  background-color: #28a745;
  color: white;
}

.reject-button {
  background-color: #dc3545;
  color: white;
}

.reject-button:hover {
  background-color: #dc3545;
  color: white;
}


.close-button {
  background-color: #6c757d;
  color: white;
  margin-bottom: 5px;
}

.close-button:hover {
  background-color: #6c757d;
  color: white;
}

.request-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-top: 15px;
    margin-bottom: 15px;
}

.request-card {
    background-color: var(--azul-acizentado);
    padding: 10px 15px;
    margin: 5px;
    border-radius: 5px;
    display: flex;
    flex-direction: column;
    gap: 5px;
    justify-content: center;
}

button:hover {
    opacity: 0.9;
}

p {
    align-self: flex-start;
}

.buttons-options {
    margin-top: 10px;
}
</style>