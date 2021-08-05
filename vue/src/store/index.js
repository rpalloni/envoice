import { createStore } from 'vuex'

export default createStore({
  state: {
    user: {
      id: '',
      username: ''
    },
    isAuthenticated: false,
    token: ''
  },
  mutations: {
    initializeStore(state) {
      // if token is in the browser localStorage
      if(localStorage.getItem('token')) {
        state.token = localStorage.getItem('token')
        state.isAuthenticated = true
        state.user.id = localStorage.getItem('id')
        state.user.username = localStorage.getItem('username')
      } else {
        state.user.id = ''
        state.user.username = ''
        state.token = ''
        state.isAuthenticated = false
      }
    },
    // loading spinner
    setIsLoading(state, status) {
      state.isLoading = status
    },
    setToken(state, token) {
      state.token = token
      state.isAuthenticated = true
    },
    removeToken(state) {
      state.user.id = ''
      state.user.username = ''
      state.token = ''
      state.isAuthenticated = false
    },
    // see Login.vue
    setUser(state, user){
      state.user = user
    }
  },
  actions: {
  },
  modules: {
  }
})
