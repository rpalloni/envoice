<template>
    <div class="page-dashboard">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Dashboard</h1>
            </div>

            <div class="column is-6">
                <div class="box">
                    <h2 class="subtitle">Unpaid invoices</h2>

                    <table class="table is-fullwidth">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Client</th>
                                <th>Amount</th>
                                <th>Due date</th>
                                <th></th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr v-for="invoice in unpaidInvoices" v-bind:key="invoice.iv_id">
                                <td>{{ invoice.iv_invoice_number }}</td>
                                <td>{{ invoice.iv_client.cl_name }}</td>
                                <td>{{ invoice.iv_gross_amount }}</td>
                                <td>{{ invoice.get_due_date }}</td>
                                <td>
                                    <router-link :to="{ name: 'Invoice', params: { id: invoice.iv_id }}">Details</router-link>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="column is-6">
                <div class="box">
                    <h2 class="subtitle">Newest clients</h2>

                    <div v-for="client in clients" v-bind:key="client.cl_id" >
                        <div class="box mb-2">
                            <h3 class="is-size-4 mb-4">{{ client.cl_name }}</h3>

                            <router-link :to="{ name: 'Client', params: { id: client.cl_id }}" class="button is-light">Details</router-link>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'Dashboard',
    data() {
        return {
            invoices: [],
            clients: [],
        }
    },
    mounted() {
        this.getInvoices()
        this.getClients()
    },
    methods: {
        async getInvoices() {
            await axios
                .get('/api/v1/invoices/')
                .then(response => {
                    console.log(response.data.data)
                    for (let i = 0; i < response.data.data.length; i++) {
                        this.invoices.push(response.data.data[i])
                    }
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        },
        getClients() {
            axios
                .get('/api/v1/clients/')
                .then(response => {
                    for (let i = 0; i < response.data.length; i++) {
                        if (this.clients.length <= 5) {
                            this.clients.push(response.data[i])
                        }
                    }
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        }
    },
    computed: {
        unpaidInvoices() {
            return this.invoices.filter(
                invoice => invoice.iv_is_paid === false && invoice.iv_invoice_type == 'invoice')
        },
    }
}
</script>