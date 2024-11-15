import { reactive } from 'vue';

interface UserData {
  user_id: number | null;
  user_role: string | null;
  user_name: string | null;
  isAuthenticated: boolean;
  user_consent: boolean | null;
  has_patient_history: boolean | null;
}

const globalData = reactive<UserData>({
  user_id: null,
  user_role: '',
  user_name: '',
  isAuthenticated: false,
  user_consent: null,
  has_patient_history: null,
});

export default globalData;
