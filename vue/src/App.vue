<template>
  <div id="wrapper">
    <nav class="navbar is-dark">
      <div class="navbar-brand">
        <router-link to="/" class="navbar-item"><strong>e-nvoice</strong></router-link>
      </div>

      <div class="navbar-menu">
        <div class="navbar-end">
          <template v-if="$store.state.isAuthenticated">
            <div class="navbar-item">
              user: {{ $store.state.user.username }}
            </div>       
            <router-link to="/dashboard" class="navbar-item"><button class="button is-info">Dashboard</button></router-link>
            <router-link to="/dashboard/clients" class="navbar-item"><button class="button is-warning">Clients</button></router-link>
            <router-link to="/dashboard/invoices" class="navbar-item"><button class="button is-primary">Invoices</button></router-link>
            <router-link to="/dashboard/account" class="navbar-item"><button class="button is-light">Account</button></router-link>
            
          </template>
          <template v-else>
            <router-link to="/" class="navbar-item">Home</router-link>
            <div class="navbar-item">
              <div class="buttons">
                <router-link to="/signup" class="button is-success">Signup</router-link>
                <router-link to="/login" class="button is-light">Login</router-link>
              </div>
            </div>
          </template>
        </div>
      </div>
    </nav>

    
  
    <section class="section">
      <router-view/>

      <!--loading spinner -->
      <div class= "is-loading-bar has-text-centered" v-bind:class="{'is-loading':$store.state.isLoading}">
        <div class="lds-dual-ring"></div>
      </div>
    </section>

    <footer class="footer">
      <p class="has-text-centered">copyright (c) e-nvoice 2020</p>
    </footer>
  </div>
</template>

<script>
import axios from 'axios'
export default {
  name: 'App',
  beforeCreate() {
    // use store/index.js to check auth before creation of app instance
    this.$store.commit('initializeStore') 
     
    const token = this.$store.state.token
    if(token){
      axios.defaults.headers.common['Authorization'] = "Token " + token
    } else {
      axios.defaults.headers.common['Authorization'] = ""
    }
    
  }
}
</script>

<style lang="scss">
.lds-dual-ring {
  display: inline-block;
  width: 60px;
  height: 60px;
}

.lds-dual-ring:after {
  content: " ";
  display: block;
  width: 64px;
  height: 64px;
  margin: 8px;
  border-radius: 50%;
  border: 6px solid #ccc;
  border-color: #ccc transparent;
  animation: lds-dual-ring 1.2s linear infinite;
}

@keyframes lds-dual-ring {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.is-loading-bar {
  height: 0;
  overflow: hidden;
  -webkit-transition: all 0.1s;
  transition: all 0.1s;

  &.is-loading {
    height: 80px;
  }
}

</style>
