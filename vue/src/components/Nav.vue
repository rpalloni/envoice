<template>
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
</template>

<script>
export default {
    name: 'Nav',

}
</script>