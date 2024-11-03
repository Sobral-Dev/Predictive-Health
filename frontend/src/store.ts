import { createStore } from 'vuex'

export default createStore({
  state: {
    isProcessing: false
  },
  mutations: {
    setProcessing(state, status) {
      state.isProcessing = status
    }
  }
})
