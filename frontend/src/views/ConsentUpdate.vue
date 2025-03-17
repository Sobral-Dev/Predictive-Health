<template>
  <main>
    <transition name="fade" mode="out-in">
      <div class="consent-update">
        <h1 class="page-title" style="padding-bottom: 25px;">Update Consent</h1>

        <section class="consent-section">

          <div 
          class="form-group" 
          v-for="term in terms" :key="term.id" 
          style="padding: 15px; background-color: darkslategrey; border-radius: 10px; margin: 20px"
          >
          
          <label :for="'consent-status-' + term.id">{{ term.name }}</label>
          
          <h5>Status: 
            <b :style="term.status === true ? 'color: green' : term.status === false ? 'color: red' : 'color: gray'">
              {{ term.status === true ? 'Given' : term.status === false ? 'Revoked' : 'Pending' }}
            </b> - 
            (<b :style="term.mandatory === true ? 'color: blue' : ''">
              {{ term.mandatory === true ? 'Mandatory' : 'Optional' }}
            </b>)
          </h5>

          <p style="font-size: smaller;">• {{ term.term_description }}</p>

          <h6 v-if="term.version > 1"
              style="font-size: 12pt; padding-top: 10px; cursor: pointer; display: flex; align-items: center;"
              @click="showDescription[term.id] = !showDescription[term.id]"
          >
            <span style="margin-right: 5px; font-size: 12pt;">
              {{ !showDescription[term.id] ? '▶' : '▼'}} <!-- Ícone de dropdown -->
            </span> 
            <b>New Version (v{{ term.version }})</b>
            
          </h6>

          <p v-if="term.version > 1 && showDescription[term.id]" style="font-size: 14pt; padding-left: 15px;">
            • {{ term.version_description }}
          </p>

          <select 
            :id="'consent-status-' + term.id" 
            v-model="selectedConsents[term.id]" 
            class="form-control" 
            style="width: 80%;"
            required
          >
            <option :value="null"></option>
            <option v-if="term.status !== true" :value="true">Given</option>
            <option v-if="term.status !== false" :value="false">Revoked</option>
          </select>
        </div>

        <button @click="updateConsent()" class="submit-button">Update Consent</button>

          <p v-if="message" class="message">
            {{ message }} <br> 
          </p>
          <p v-if="error && error !== 'No Patient'" class="error">{{ error }}</p>
        </section>
      </div>
    </transition>
  </main>  
</template>

<script lang="ts">
import { defineComponent, watch, ComponentPublicInstance } from 'vue';
import axios from 'axios';
import { useRouter, RouteLocationNormalized, NavigationGuardNext} from 'vue-router';
import Swal from 'sweetalert2';

export default defineComponent({
  name: 'ConsentUpdate',
  data() {
    return {
      message: '',
      error: '',
      globalData: {
        user_consent: localStorage.getItem('gd.user_consent'),
        user_role: localStorage.getItem('gd.user_role')
      },
      terms: [],
      selectedConsents: {},
      showDescription: {},
    };
  },

  setup() {
    const router = useRouter();
    return { router };
  },

  mounted() {
    this.getConsentStatus();
    window.addEventListener("force-consent-refresh", this.getConsentStatus);
  },

  beforeUnmount() {
    window.removeEventListener("force-consent-refresh", this.getConsentStatus);
  },

  methods: {

    setMessage(msg: string) {
      this.message = msg;
      setTimeout(() => {
        this.message = ""; 
      }, 5000);
    },

    setError(err: string) {
      this.error = err;
      setTimeout(() => {
        this.error = ""; 
      }, 5000);
    },
    
    async updateConsent() {
     
      const updatedConsents = this.terms
          .filter(term => this.selectedConsents[term.id] !== null) 
          .map(term => ({
              term_id: term.id,
              consent_status: this.selectedConsents[term.id] === true || this.selectedConsents[term.id] === false 
                              ? this.selectedConsents[term.id] : null,
              version: term.version,
              mandatory: term.mandatory
          }));

      if (updatedConsents.length === 0) {
          this.setMessage("No changes made.");
          return;
      }

      // Verifica se algum termo obrigatório está sendo revogado
      const mandatoryRevoked = updatedConsents.some((consent) => consent.mandatory && consent.consent_status === false);

      if (mandatoryRevoked) {
        Swal.fire({
          title: "Are you sure?",
          text: "Revoking a mandatory consent will prevent you from using the system.",
          icon: "warning",
          showCancelButton: true,
          confirmButtonColor: "#d33",
          cancelButtonColor: "#3085d6",
          confirmButtonText: "Yes, revoke it",
          cancelButtonText: "Cancel",
          reverseButtons: true,
          allowOutsideClick: false,
        }).then((result) => {
          if (!result.isConfirmed) {
            console.log("Revocation cancelled. Consent update aborted.");
            return; 
          }

          // Se o usuário confirmou, prossegue com a requisição
          this.sendConsentUpdate(updatedConsents);
        });

        return; // Impede que o código continue enquanto o Swal não for resolvido
      }

      // Se nenhum termo obrigatório foi revogado, envia a atualização normalmente
      this.sendConsentUpdate(updatedConsents);
    
    },

    async sendConsentUpdate(updatedConsents: any) {

        try {
            const response = await axios.post(
                `http://localhost:5000/update-consent`,
                { consents: updatedConsents },
                {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('token')}`,
                    },
                }
            );

            console.log("Enviando request para `http://localhost:5000/update-consent`")

            this.setMessage(response.data.message);
            this.error = '';

            this.getConsentStatus();

        } catch (err) {
            this.setError(err.response?.data.error || `Failed to update consent ${err}`);
            this.message = '';
        }
    },
      
    async getConsentStatus() {
        
        try {
          const response = await axios.get(
            `http://localhost:5000/patients/consent/current`,
            {
              headers: {
                Authorization: `Bearer ${localStorage.getItem('token')}`,
              },
            }
          );

          this.terms = response.data.consents;

        } catch (err) {
          this.setError(`Failed to get user consent status: ${err}`);
        }

    },

    beforeRouteEnter(
      to: RouteLocationNormalized,
      from: RouteLocationNormalized,
      next: NavigationGuardNext) {
      
        next((vm) => {
          (vm as ComponentPublicInstance & { getConsentStatus: () => void }).getConsentStatus();
        });

    },

  },

});
</script>

<style scoped>
@import '../assets/css/base.css';

.initial-consent {
  color: var(--azul-contraste);
}

.initial-consent b {
  color: var(--azul-vibrante);
}

.consent-update {
  /* Estilos da página de atualização de consentimento */
}

.page-title {
  /* Estilos para o título da página */
}

.consent-section {
  /* Estilos da seção de formulário */
}

.form-group {
  margin-bottom: 15px;
}

.form-control {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
}

.submit-button {
  margin-top: 20px;
}

.message {
  color: green;
  margin-top: 10px;
}

.error {
  color: red;
  margin-top: 10px;
}
</style>
