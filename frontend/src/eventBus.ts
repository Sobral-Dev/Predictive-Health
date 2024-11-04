import { reactive } from 'vue';

interface EventBus {
  usersUpdated: boolean;
  patientsUpdated: boolean;
}

const eventBus: EventBus = reactive({
  usersUpdated: false,
  patientsUpdated: false,
});

export default eventBus
