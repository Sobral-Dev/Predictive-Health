import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router';
import AdminDashboard from '../views/AdminDashboard.vue';
import AuditLogs from '../views/AuditLogs.vue';
import ChangePassword from '../views/ChangePassword.vue';
import ConsentUpdate from '../views/ConsentUpdate.vue';
import HealthPrediction from '../views/HealthPrediction.vue';
import Login from '../views/Login.vue';
import PatientDetails from '../views/PatientDetails.vue';
import PersonalDataExport from '../views/PersonalDataExport.vue';
import RegisterPatient from '../views/RegisterPatient.vue';
import ShowPatients from '../views/ShowPatients.vue';
import UserProfile from '../views/UserProfile.vue';
import UsersManagement from '../views/UsersManagement.vue';
import UserRegistration from '../views/UserRegistration.vue';
import DoctorPatientList from '../views/DoctorPatientList.vue';
import DoctorPredictions from '../views/DoctorPredictions.vue';
import AdminPredictions from '../views/AdminPredictions.vue';
import UserPredictions from '../views/UserPredictions.vue';
import axios from 'axios';
import Swal from 'sweetalert2';

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Login',
    component: Login,
  },
    {
    path: '/login',
    name: 'Login2',
    component: Login,
  },
  {
    path: '/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
    meta: { requiresAuth: true, allowedRoles: ['medico', 'admin'] },
  },
  {
    path: '/audit-logs',
    name: 'AuditLogs',
    component: AuditLogs,
    meta: { requiresAuth: true, allowedRoles: ['admin'] },
  },
  {
    path: '/change-password',
    name: 'ChangePassword',
    component: ChangePassword,
    meta: { requiresAuth: true, allowedRoles: ['medico', 'admin', 'paciente'] },
  },
  {
    path: '/consent-update/:id',
    name: 'ConsentUpdate',
    component: ConsentUpdate,
    meta: { requiresAuth: true, allowedRoles: ['medico', 'admin', 'paciente'] },
    props: true,
  },
  {
    path: '/health-prediction',
    name: 'HealthPrediction',
    component: HealthPrediction,
    meta: { requiresAuth: true, allowedRoles: ['medico', 'admin', 'paciente'] },
  },
  {
    path: '/patients/:id',
    name: 'PatientDetails',
    component: PatientDetails,
    meta: { requiresAuth: true, allowedRoles: ['medico', 'admin'] },
    props: true,
  },
  {
    path: '/export-data/:id',
    name: 'PersonalDataExport',
    component: PersonalDataExport,
    meta: { requiresAuth: true, allowedRoles: ['medico', 'admin', 'paciente'] },
    props: true,
  },
  {
    path: '/register-patient',
    name: 'RegisterPatient',
    component: RegisterPatient,
    meta: { requiresAuth: true, allowedRoles: ['medico', 'admin'] },
  },
  {
    path: '/doctor-patient-list',
    name: 'DoctorPatientList',
    component: DoctorPatientList,
    meta: { requiresAuth: true, allowedRoles: ['medico'] },
  },
  {
    path: '/doctor-predictions',
    name: 'DoctorPredictions',
    component: DoctorPredictions,
    meta: { requiresAuth: true, allowedRoles: ['medico'] },
  },
  {
    path: '/admin-predictions',
    name: 'AdminPredictions',
    component: AdminPredictions,
    meta: { requiresAuth: true, allowedRoles: ['admin'] },
  },
  {
    path: '/user-predictions',
    name: 'UserPredictions',
    component: UserPredictions,
    meta: { requiresAuth: true, allowedRoles: ['paciente'] },
  },
  {
    path: '/patients',
    name: 'ShowPatients',
    component: ShowPatients,
    meta: { requiresAuth: true, allowedRoles: ['medico', 'admin'] },
  },
  {
    path: '/profile',
    name: 'UserProfile',
    component: UserProfile,
    meta: { requiresAuth: true, allowedRoles: ['medico', 'admin', 'paciente'] },
  },
  {
    path: '/manage-users',
    name: 'UsersManagement',
    component: UsersManagement,
    meta: { requiresAuth: true, allowedRoles: ['admin'] },
  },
  {
    path: '/register-user',
    name: 'UserRegistration',
    component: UserRegistration,
    meta: { requiresAuth: true, allowedRoles: ['admin'] },
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// 🚀 Função para verificar os consentimentos do usuário
async function checkUserConsents(): Promise<{ valid: boolean; issueType?: string }> {
  const token = localStorage.getItem("token");
  if (!token) return { valid: false, issueType: "unauthenticated" };

  try {
    const consentResponse = await axios.get("http://localhost:5000/patients/consent/current", {
      headers: { Authorization: `Bearer ${token}` },
    });

    const consents = consentResponse.data.consents;
    const pendingMandatory = consents.find(term => term.mandatory && term.status !== true);
    const pendingOptional = consents.find(term => !term.mandatory && term.status === "pending");

    if (pendingMandatory) {
      return { valid: false, issueType: "mandatory" };
    }
    if (pendingOptional) {
      return { valid: false, issueType: "optional" };
    }

    return { valid: true };
  } catch (error: any) {
    console.error(`Error checking consents: ${error}`);
    return { valid: false, issueType: "error" };
  }
}

// 🚀 Interceptador de requisições PUT, DELETE e POST
axios.interceptors.request.use(async (config) => {
  const token = localStorage.getItem("token");

  if (!token) return config; // Se não estiver autenticado, não faz nada.

  // 🚨 Exceções: Permite requisições para /login, /logout e /update-consent sem bloqueio.
  const excludedRoutes = [
    "/login", 
    "/logout", 
    "/update-consent"
    ];

  if (
    excludedRoutes.some((route) => config.url?.includes(route)) || 
    router.currentRoute.value.name === "Login" || 
    router.currentRoute.value.name === "Login2" ||
    router.currentRoute.value.name === "ConsentUpdate"
    ) {

    return config;
    
  }

  // ⚡️ Se for uma requisição PUT, DELETE ou POST, verifica os consentimentos do usuário
  if (["put", "delete", "post"].includes(config.method?.toLowerCase() || "")) {
    const consentStatus = await checkUserConsents();

    if (!consentStatus.valid) {
      console.log("⛔ User has consent issues. Blocking request...");

      // ❌ Bloqueia a requisição antes de abrir o Swal
      Promise.reject(new axios.Cancel("Consent issue detected"));

      // 🛑 Mostra um alerta para o usuário
      Swal.fire({
        title: consentStatus.issueType === "mandatory" ? "Mandatory Consent Required" : "Optional Consent Pending",
        text: consentStatus.issueType === "mandatory"
          ? "You must accept all mandatory consents before proceeding."
          : "There's an optional consent pending. Please review it.",
        icon: "warning",
        confirmButtonText: "Go to Consent Page",
        allowOutsideClick: false,
        customClass: {
          popup: "custom-popup-class",
        },
      }).then(() => {
        router.push(`/consent-update/${localStorage.getItem('gd.user_id')}}`);
      });
    }
  }

  return config;
});

// 🚀 Guarda de navegação para verificar autenticação e consentimentos
router.beforeEach(async (to, from, next) => {
  if (to.matched.some(record => record.meta.requiresAuth)) {
    const token = localStorage.getItem("token");

    try {
      const authResponse = await axios.get("http://localhost:5000/isAuthenticated", {
        headers: { Authorization: `Bearer ${token}` },
      });

      if (authResponse.status !== 200) {
        console.log("⛔ User not authenticated. Redirecting to Login...");
        return next({ name: "Login" });
      }

      console.log("✅ User is authenticated. Checking consents...");

      const consentStatus = await checkUserConsents();

      if (!consentStatus.valid) {
        console.log("⛔ User has consent issues. Redirecting to Update Consent...");

        if (to.name === "ConsentUpdate") {
          console.log("🔄 User going to Update Consent page. Forcing refresh...");
          const event = new Event("force-consent-refresh");
          window.dispatchEvent(event);
          
          return next();
        }

        if (from.name === "ConsentUpdate") {
          console.log("🔄 User already in Update Consent page. Forcing refresh...");
          const event = new Event("force-consent-refresh");
          window.dispatchEvent(event);
          
        }

        // ❌ Bloqueia a navegação antes de abrir o Swal
        next(false);

        Swal.fire({
          title: consentStatus.issueType === "mandatory" ? "Mandatory Consent Required" : "Optional Consent Pending",
          text: consentStatus.issueType === "mandatory"
            ? "You must accept all mandatory consents before proceeding."
            : "There's an optional consent pending. Please review it.",
          icon: "warning",
          confirmButtonText: from.name === 'ConsentUpdate' ? "OK" : "Go to Consent Page",
          allowOutsideClick: false,
          customClass: {
            popup: "custom-popup-class",
          },
        }).then(() => {
            
          router.push(`/consent-update/${localStorage.getItem("gd.user_id")}`);

        });

        return;

      }

      console.log("✅ User has all required consents. Proceeding...");
      next();
    } catch (error: any) {
      console.log(`Token expired or user not authenticated. Redirecting to Login... msg: ${error}`);
      if (to.name !== "Login") {
        return next({ name: "Login" });
      }
    }
  } else {
    next();
  }
});

export default router;
