<template>
    <div class="page-clients">
        <nav class="breadcrumb" aria-label="breadcrumbs">
            <ul>
                <li><router-link to="/dashboard">Dashboard</router-link></li>
                <li><router-link to="/dashboard/clients">Clients</router-link></li>
                <li class="is-active"><router-link :to="{ name: 'Client', params: { id: `${client.cl_id}` }}">{{ client.cl_name }}</router-link></li>
            </ul>
        </nav>

        <div class="columns is-multiline">
            <div class="column is-12">
               <h3 class="is-size-4 mb-4">{{ client.cl_name }}</h3>
               <router-link :to="{ name: 'ClientEdit', params: { id: `${client.cl_id}`}}" class="button is-danger">Edit client</router-link>
            </div>

            
            <div class="column is-12">
                <div class="box">
                    <h2 class="subtitle">Contact details</h2>

                    <p><strong>{{ client.cl_name }}</strong></p>
                    
                    <p v-if="client.cl_address1">{{ client.cl_address1 }}</p>
                    <p v-if="client.cl_address2">{{ client.cl_address2 }}</p>
                    <p v-if="client.cl_zipcode || client.cl_place">{{ client.cl_zipcode }} {{ client.cl_place }}</p>
                    <p v-if="client.cl_country">{{ client.cl_country }}</p>
                </div>
            </div>

            <div class="column is-12" v-if="unpaidInvoices.length">
                <div class="box">
                    <h2 class="subtitle">Unpaid invoices</h2>

                    <table class="table is-fullwidth">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Amount</th>
                                <th>Due date</th>
                                <th></th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr v-for="invoice in unpaidInvoices" v-bind:key="invoice.id">
                                <td>{{ invoice.iv_invoice_number }}</td>
                                <td>{{ invoice.iv_gross_amount }}</td>
                                <td>{{ invoice.get_due_date }}</td>
                                <td>
                                    <router-link :to="{ name: 'Invoice', params: { id: invoice.iv_id } }">Details</router-link>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="column is-12" v-if="paidInvoices.length">
                <div class="box">
                    <h2 class="subtitle">Paid invoices</h2>

                    <table class="table is-fullwidth">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Amount</th>
                                <th>Due date</th>
                                <th></th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr v-for="invoice in paidInvoices" v-bind:key="invoice.id">
                                <td>{{ invoice.iv_invoice_number }}</td>
                                <td>{{ invoice.iv_gross_amount }}</td>
                                <td>{{ invoice.get_due_date }}</td>
                                <td>
                                    <router-link :to="{ name: 'Invoice', params: { id: invoice.iv_id } }">Details</router-link>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
            
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'Client',
    data () {
        return {
            client: {
                invoices: []
            }
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
        }
    },
    computed: {
        unpaidInvoices() {
            return this.client.invoices.filter(invoice => invoice.iv_is_paid === false)
        },
        paidInvoices() {
            return this.client.invoices.filter(invoice => invoice.iv_is_paid === true)
        }
    }
}
</script>