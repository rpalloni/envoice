<template>
  <div id="wrapper">
    <Nav/>

    <section class="section">
      <!--listening the router to load specific component -->
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
import Nav from '@/components/Nav'
export default {
  name: 'App',
  components: {
    Nav
  },
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
