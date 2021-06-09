<template>
    <div class="page-clients">
        <nav class="breadcrumb" aria-label="breadcrumbs">
            <ul>
                <li><router-link to="/dashboard">Dashboard</router-link></li>
                <li><router-link to="/dashboard/clients">Clients</router-link></li>
                <li><router-link :to="{ name: 'Client', params: { id: client.cl_id }}">Edit</router-link></li>
                <li class="is-active"><router-link :to="{ name: 'ClientEdit', params: { id: client.cl_id }}"> {{ client.cl_name }}</router-link></li>
            </ul>
        </nav>
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Edit client: {{ client.cl_name }}</h1>
            </div>
            <div class="column is-6">
                <div class="field">
                    <label>Name</label>
                    
                    <div class="control">
                        <input type="text" name="name" class="input" v-model="client.cl_name">
                    </div>
                </div>

                <div class="field">
                    <label>Email</label>
                    
                    <div class="control">
                        <input type="email" name="email" class="input" v-model="client.cl_email">
                    </div>
                </div>

                <div class="field">
                    <label>Organisation Number</label>
                    
                    <div class="control">
                        <input type="email" name="email" class="input" v-model="client.cl_org_number">
                    </div>
                </div>

                <div class="field">
                    <label>Address 1</label>
                    
                    <div class="control">
                        <input type="text" name="address1" class="input" v-model="client.cl_address1">
                    </div>
                </div>

                <div class="field">
                    <label>Address 2</label>
                    
                    <div class="control">
                        <input type="text" name="address2" class="input" v-model="client.cl_address2">
                    </div>
                </div>
            </div>

            <div class="column is-6">
                <div class="field">
                    <label>Zipcode</label>
                    
                    <div class="control">
                        <input type="text" name="zipcode" class="input" v-model="client.cl_zipcode">
                    </div>
                </div>

                <div class="field">
                    <label>Place</label>
                    
                    <div class="control">
                        <input type="text" name="place" class="input" v-model="client.cl_place">
                    </div>
                </div>

                <div class="field">
                    <label>Country</label>
                    
                    <div class="control">
                        <input type="text" name="country" class="input" v-model="client.cl_country">
                    </div>
                </div>

                <div class="field">
                    <label>Contact Person</label>
                    
                    <div class="control">
                        <input type="text" name="country" class="input" v-model="client.cl_contact_person">
                    </div>
                </div>

                <div class="field">
                    <label>Contact Reference</label>
                    
                    <div class="control">
                        <input type="text" name="country" class="input" v-model="client.cl_contact_reference">
                    </div>
                </div>
            </div>

            <div class="column is-12">
                <div class="field">
                    <div class="control">
                        <button class="button is-success" @click="submitForm">Save</button>
                    </div>
                </div>
                <div>
                    {{ error }}
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
import {toast} from 'bulma-toast'
export default {
    name: 'ClientEdit',
    data(){
        return {
            client: {},
            error: ''
        }
    },
    mounted() {
        this.getClient()
    },
    methods: {
        getClient() {
            const clientID = this.$route.params.id // dynamic router >> params: { id: client.cl_id }
            axios
                .get(`/api/v1/clients/${clientID}`)
                .then(response => {
                    this.client = response.data
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        },
        submitForm() {
            const clientID = this.$route.params.id
            // use patch instead of post to update only changed data
            axios
                .patch(`/api/v1/clients/${clientID}/`, this.client)
                .then(response => {
                    toast({
                        message: 'The change was saved',
                        type: 'is-success',
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 2000,
                        position: 'top-center',
                    })
                    
                    this.$router.push('/dashboard/clients')
                })
                .catch(error => {
                    this.error = error.message
                    console.log(JSON.stringify(error.message))
                })
        }

    }
}
</script>