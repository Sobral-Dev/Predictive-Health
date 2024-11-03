<script lang="ts">
import { RouterView } from 'vue-router'
import Sidebar from './components/Sidebar.vue'
import { defineComponent } from 'vue'
import eventBus from './eventBus'

export default defineComponent({
  name: 'App',
  data() {
    return {
    }
  },

  created() {
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
