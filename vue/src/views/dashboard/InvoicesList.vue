<template>
    <div class="page-invoices">

        <div class="control">
            <router-link to="/dashboard/invoices/add"><button class="button is-danger">Add Invoice</button></router-link>
        </div>

        <div class="section">
            <div class="column is-12">
                <h1 class="title">Find Invoices</h1>
            </div>

            <div class="columns is-vcentered">
                <div class="column is-4">
                    <div class="field">
                        <label class="label">Client</label>
                        <div class="control">
                            <div class="select">
                                <select name="client" v-model="client">
                                    <option value="">--- Select client ---</option>
                                    <option v-for="client in clients" v-bind:key="client.cl_id" v-bind:value="client">
                                        {{ client.cl_name }}
                                    </option>
                                </select>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="column is-4">
                    <div class="field">
                        <label class="label">Year</label>
                        <div class="control">
                            <input class="input" type="number" placeholder="Invoice Year" v-model="year">
                        </div>
                    </div>
                </div>
            </div>
            <div class="field is-grouped">
                <div class="control">
                    <button class="button is-link is-light" @click="getInvoices">Search</button>
                </div>
                <div class="control">
                    <button class="button is-link is-light" @click="clearSearchFields">Clear</button>
                </div>
            </div>

        </div>
        <div class="section">
            <div class="columns is-multiline">
                
                <div class="column is-12" v-if="invoices.length > 0">
                    <div class="column is-12">
                        <h1 class="title">Invoices</h1>
                    </div>
                    <table class="table is-fullwidth">
                        <thead>
                            <tr>
                                <th>#</th>
                                <th>Client</th>
                                <th>Amount</th>
                                <th>Year</th>
                                <th>Due date</th>
                                <th>Type</th>
                                <th>Is paid</th>
                                <th></th>
                            </tr>
                        </thead>

                        <tbody>
                            <tr v-for="invoice in invoices" v-bind:key="invoice.iv_invoice_number">
                                <td>{{ invoice.iv_invoice_number }}</td>
                                <td>{{ invoice.iv_client.cl_name }}</td>
                                <td v-bind:style="[invoice.iv_invoice_type == 'invoice' ? {color: 'green', 'text-align': right } : {color: 'red', 'text-align': right} ]">{{ invoice.iv_gross_amount }}</td>
                                <td>{{ invoice.get_year }}</td>
                                <td>{{ invoice.get_due_date }}</td>
                                <td>{{ invoice.iv_invoice_type }}</td>
                                <td>{{ invoice.iv_is_paid }}</td>
                                <td>
                                    <router-link :to="{ name: 'Invoice', params: { id: invoice.iv_id }}">Details</router-link>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div v-else>No invoices for this search</div>
            </div>
        </div>     
    </div>
</template>

<script>
import axios from 'axios'
export default {
    name: 'Invoices',
    data() {
        return {
            invoices: [],
            clients: [],
            client: '',
            year: ''
        }
    },
    mounted() {
        //this.getInvoices(),
        this.getClients()
    },
    methods: {
        getClients() {
            axios
                .get('/api/v1/clients/')
                .then(response => {
                    this.clients = response.data
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        },
        getInvoices() {
            this.invoices = []; // clear result set
            const params = {
                'selected_client': this.client.cl_id,
                'selected_year': this.year
            }
            axios
                //.get(`/api/v1/invoices/?selected_client=${this.client.cl_id}&selected_year=${this.year}`)
                .get('/api/v1/invoices/', {params})
                .then(response => {
                    console.log(response)
                    for (let i = 0; i < response.data.length; i++) {
                        this.invoices.push(response.data[i])
                    }
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        },
        clearSearchFields(){
            this.client = '',
            this.year = ''
        }
    }
}
</script>