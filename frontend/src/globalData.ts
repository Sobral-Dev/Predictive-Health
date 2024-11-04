import { reactive } from 'vue';

interface UserData {
  user_id: number | null;
  user_role: string;
  user_name: string;
  isAuthenticated: boolean;
}

const globalData = reactive<UserData>({
  user_id: null,
  user_role: '',
  user_name: '',
  isAuthenticated: false,
});

export default globalData;
