<template>
    <div class="page-login">
        <div class="columns">
            <div class="column is-4 is-offset-4">
                <h1 class="title">Login page</h1>

                <form @submit.prevent="submitForm">
                    <div class="field">
                        <label>Email</label>
                        <div class="control">
                            <input type="email" name="username" class="input" v-model="username">
                        </div>
                    </div>

                    <div class="field">
                        <label>Password</label>
                        <div class="control">
                            <input type="password" name="password" class="input" v-model="password">
                        </div>
                    </div>

                    <div class="notification is-danger" v-if="errors.length">
                        <p v-for="error in errors" v-bind:key="error">{{ error }}</p>
                    </div>

                    <div class="field">
                        <div class="control">
                            <button class="button is-success">Login</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'LogIn',
    data() {
        return {
            username: '',
            password: '',
            errors: []
        }
    },
    methods: {
        // after login, set user information in the browser
        async submitForm(e) {
            axios.defaults.headers.common["Authorization"] = ""
            localStorage.removeItem("token")
            const formData = {
                username: this.username,
                password: this.password
            }
            await axios
                .post("/api/v1/token/login/", formData)
                .then(response => {
                    const token = response.data.auth_token // auth token from the server (see urls.py)
                    this.$store.commit('setToken', token) // call setToken function
                    axios.defaults.headers.common["Authorization"] = "Token " + token
                    localStorage.setItem("token", token)
                })
                .catch(error => {
                    if (error.response) {
                        for (const property in error.response.data) {
                            this.errors.push(`${property}: ${error.response.data[property]}`)
                        }
                        console.log(JSON.stringify(error.response.data))
                    } else if (error.message) {
                        console.log(JSON.stringify(error.message))
                    } else {
                        console.log(JSON.stringify(error))
                    }
                })

            axios
                .get("/api/v1/users/me/")
                .then(response => {
                    this.$store.commit('setUser', {
                        'username': response.data.username,
                        'id': response.data.id
                    })
                    localStorage.setItem('username', response.data.username)
                    localStorage.setItem('userid', response.data.id)

                    this.$router.push('/dashboard') // redirect to dashboard
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        }
    }
}
</script>