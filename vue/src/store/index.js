/* 
A store is a centralized location for data needed across multiple disparate app components 
with centrally defined rules on how those pieces of data can be changed (e.g. logged user). 
Without a store, data have to pass through props down to components and emit up via events to parents.
By having a centralized store, we reduce the complexity of needing to pass/catch
props and events up and down multiple levels and we centralize mutations on sensible data.
*/

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
    // see Login.vue + settings DRF
    setUser(state, user){
      state.user = user
    }
  },
  actions: {
  },
  modules: {
  }
})
