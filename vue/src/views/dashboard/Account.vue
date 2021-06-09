<template>
    <div class="page-my-account">
        <h1 class="title">User Account</h1>
        <p>Username: {{ $store.state.user.username }}</p>
        <hr>
        <div class="buttons">
            <router-link to='/dashboard/account/edit-team' class="button is-warning">Edit team</router-link>
            <button @click="logout()" class="button is-danger">Logout</button>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'Account',
    data () {
        return {
            user: ''
        }
    },
    methods: {
        logout() {
            axios
                .post('/api/v1/token/logout/')
                .then(response => {
                    console.log(response)
                    axios.defaults.headers.common["Authorization"] = ""
                    localStorage.removeItem("token")
                    localStorage.removeItem("username")
                    localStorage.removeItem("userid")

                    this.$store.commit('removeToken')
                    this.$router.push('/login')
                })
                .catch(error => {
                    if (error.response) {
                        console.log(JSON.stringify(error.response.data))
                    } else if (error.message) {
                        console.log(JSON.stringify(error.message))
                    } else {
                        console.log(JSON.stringify(error))
                    }
                })

        }
    }
}
</script>