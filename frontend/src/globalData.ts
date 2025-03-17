import { reactive } from 'vue';

interface Consent {
  id: string;
  name: string;
  description: string;
  mandatory: boolean;
  status: string;
  timestamp: string | null;
  version: number;
}

interface UserData {
  user_id: number | null;
  user_role: string | null;
  user_name: string | null;
  isAuthenticated: boolean;
  user_consent: Consent[];  
  has_patient_history: boolean | null;
}

const globalData = reactive<UserData>({
  user_id: null,
  user_role: '',
  user_name: '',
  isAuthenticated: false,
  user_consent: [], 
  has_patient_history: null,
});

export default globalData;
