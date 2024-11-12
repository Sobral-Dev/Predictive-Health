import { reactive } from 'vue';

interface UserData {
  user_id: number | null;
  user_role: string;
  user_name: string;
  isAuthenticated: boolean;
  user_consent: boolean | null;
}

const globalData = reactive<UserData>({
  user_id: null,
  user_role: '',
  user_name: '',
  isAuthenticated: false,
  user_consent: null
});

export default globalData;
