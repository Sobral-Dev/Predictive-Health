import { reactive } from 'vue';

interface EventBus {
  usersUpdated: boolean;
  patientsUpdated: boolean;
  predictionSaved: boolean;
}

const eventBus: EventBus = reactive({
  usersUpdated: false,
  patientsUpdated: false,
  predictionSaved: false,
});

export default eventBus
