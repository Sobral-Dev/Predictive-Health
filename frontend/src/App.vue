<script lang="ts">
import { RouterView } from 'vue-router'
import { defineComponent, watch, ComponentPublicInstance } from 'vue';
import Sidebar from './components/Sidebar.vue';

export default defineComponent({
  name: 'App',
  data() {
    return {
    }
  },

  components: {
    Sidebar
  }
})
</script>

<template>
  <div class="app-container">
    <!-- Menu lateral -->
    <Sidebar />
  </div>

  <router-view v-slot="{ Component }">
    <transition name="fade" mode="out-in">
      <component :is="Component" />
    </transition>
  </router-view>
</template>

<style scoped>
@import './assets/css/base.css';

/* estilização dos elementos do single page */
.app-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-start;
}
</style>
