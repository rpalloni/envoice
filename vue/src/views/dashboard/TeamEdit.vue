<template>
    <div class="edit-team">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Edit team</h1>
            </div>
                        <div class="column is-6">
                <div class="field">
                    <label>Name</label>
                    
                    <div class="control">
                        <input type="text" name="name" class="input" v-model="team.tm_name">
                    </div>
                </div>

                <div class="field">
                    <label>Organisation Number</label>
                    
                    <div class="control">
                        <input type="text" name="email" class="input" v-model="team.tm_org_number">
                    </div>
                </div>

                <div class="field">
                    <label>Invoice number sequence start</label>
                    
                    <div class="control">
                        <input type="number" name="invoice_nbr" class="input" v-model="team.tm_first_invoice_nbr">
                    </div>
                </div>

                <div class="field">
                    <label>Bank account</label>
                    
                    <div class="control">
                        <input type="text" name="bank_account" class="input" v-model="team.tm_bank_account">
                    </div>
                </div>

                <div class="column is-12">
                <div class="field">
                    <div class="control">
                        <button class="button is-success" @click="submitForm">Save</button>
                    </div>
                </div>
            </div>

            </div>
        </div>
    </div> 
</template>

<script>
import axios from 'axios'
import {toast} from 'bulma-toast'
export default {
    name: 'TeamEdit',
    data() {
        return {
            team: {}
        }
    },
    async mounted() {
        // if there is not a team for the user:
        // first, send a request to create an instance (only with tm_first_invoice_nbr, tm_created_by)
        // second, get team data back and load in the template (mounted awaits until this is done)
        // template is pre-filled with generated data and ready to be completed (tm_name, tm_org_number)
        await this.getOrCreateTeam()
    },
    methods: {
        getOrCreateTeam() {
            axios
                .get('/api/v1/teams/')
                .then(response => {
                    this.team = response.data[0]
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        },
        submitForm() {
            axios
                .patch(`/api/v1/teams/${this.team.tm_id}/`, this.team)
                .then(response => {
                    toast({
                        message: 'The change was saved',
                        type: 'is-success',
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 2000,
                        position: 'top-center',
                    })

                    this.$router.push('/dashboard/account')
                })
                .catch(error => {
                    this.error = error.message
                    console.log(JSON.stringify(error.message))
                })
        
        }
    }
}
</script>