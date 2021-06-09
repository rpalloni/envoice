<template>
    <div class="page-invoice">
        <div class="columns is-multiline is-vcentered">

            <div class="column is-8 is-offset-2 mb-5">
                <template v-if="invoice.iv_invoice_type==='invoice'">
                    <h1 class="title"> Invoice - {{ invoice.iv_invoice_number }}</h1>
                </template>
                <template v-else>
                    <h1 class="title"> Credit note - {{ invoice.iv_invoice_number }}</h1>
                </template>
                
                <div class="buttons">
                    <button @click="getPdf()" class="button is-dark">Download PDF</button>

                    <template v-if="!invoice.iv_is_credit_for && !invoice.iv_is_credited">
                        <button @click="setAsPaid()" class="button is-success" v-if="!invoice.iv_is_paid">Set as paid</button>
                        <button @click="createCreditNote()" class="button is-danger" v-if="!invoice.iv_is_paid">Create credit note</button>
                        <button @click="sendReminder()" class="button is-info" v-if="!invoice.iv_is_paid">Send reminder</button>
                    </template>
                </div>
                 
            </div>

            <div class="column is-8 is-offset-2">
                <div class="box">
                    <h3 class="is-size-4 subtitle">Client</h3>

                    <p><strong>{{ client.cl_name }}</strong></p>
                    
                    <p v-if="client.cl_address1">{{ client.cl_address1 }}</p>
                    <p v-if="client.cl_address2">{{ client.cl_address2}}</p>
                    <p v-if="client.cl_zipcode || client.cl_place">{{ client.cl_zipcode }} {{ client.cl_place }}</p>
                    <p v-if="client.cl_country">{{ client.cl_country }}</p>
                </div>
            </div>

            <div class="column is-8 is-offset-2">
                <div class="box">
                    <h3 class="is-size-4 subtitle">Items</h3>

                    <table class="table is-fullwidth">
                        <thead>
                            <tr>
                                <td><strong>Description</strong></td>
                                <td><strong>Quantity</strong></td>
                                <td ><strong>Amount</strong></td>
                                <td><strong>Vat rate</strong></td>
                                <td><strong>Total</strong></td>
                            </tr>
                        </thead>

                        <tbody>
                            <tr v-for="item in invoice.items" v-bind:key="item.it_id">
                                <td>{{ item.it_descr }}</td>
                                <td>{{ item.it_quantity }}</td>
                                <td>{{ item.it_net_amount }}</td>
                                <td>{{ item.it_vat_rate }}%</td>
                                <td>{{ getItemTotal(item) }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="column is-8 is-offset-2">
                <div class="box">
                    <h3 class="is-size-4 subtitle">Summary</h3>

                    <div class="columns">
                        <div class="column is-6">
                            <p><strong>Document type</strong>: {{ getInvoiceType() }}</p>
                            <p v-if="invoice.iv_invoice_type==='credit_note'"><strong>Invoice reference:</strong> {{ invoice_ref }}</p>
                            <p><strong>Net amount:</strong> {{ invoice.iv_net_amount }}</p>
                            <p><strong>Vat amount:</strong> {{ invoice.iv_vat_amount }}</p>
                            <p><strong>Gross amount:</strong> {{ invoice.iv_gross_amount }}</p>
                            <p v-if="invoice.iv_invoice_type==='invoice'"><strong>Bank account:</strong> {{ invoice.iv_bank_account }}</p>
                        </div>
                    
                        <div class="column is-6">
                            <p><strong>Our reference</strong>: {{ invoice.iv_sender_reference }}</p>
                            <p><strong>Client reference</strong>: {{ client.cl_contact_reference }} </p>
                            <p><strong>Due date</strong>: {{ invoice.get_due_date }}</p>
                            <p><strong>Status</strong>: {{ getStatusLabel() }}</p>
                            <p v-if="invoice.iv_invoice_type==='invoice'" style ="color:red">Credited: {{ invoice.iv_is_credited }}</p>
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
const fileDownload = require('js-file-download')

export default {
    name: 'Invoice',
    data() {
        return {
            invoice: {},
            client: '',
            items: [],
            invoice_ref: ''
        }
    },
    async mounted() {
        // mounted (load data in template) awaits until items and invoice data are received
        await this.getInvoice()
        //await this.getItems()
    },
    methods: {
        getInvoice() {
            const invoiceID = this.$route.params.id
            axios
                .get(`/api/v1/invoices/${invoiceID}`)
                .then(response => {
                    console.log(response.data)
                    this.invoice = response.data
                    this.client = response.data.iv_client
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        },
        // data in the InvoiceSerializer: no need for specific data retrieve
        // getItems() {
        //     const invoiceID = this.$route.params.id
        //     axios
        //         .get(`/api/v1/items/?invoice_id=${invoiceID}`)
        //         .then(response => {
        //             this.items = response.data
        //         })
        //         .catch(error => {
        //             console.log(JSON.stringify(error))
        //         })
        // }
        getPdf(){
            const invoiceID = this.$route.params.id
            axios
                .get(`/api/v1/invoices/${invoiceID}/generate-pdf/`, {
                    responseType: 'blob' // file format for fileDownload
                })
                .then(response => {
                    fileDownload(response.data, `invoice_${invoiceID}.pdf`)
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        },
        getStatusLabel() {
            if (this.invoice.iv_is_paid) {
                return 'Is paid'
            } else {
                return 'Is not paid'
            }
        },
        getInvoiceType() {
            if (this.invoice.iv_invoice_type === 'credit_note') {
                return 'Credit note'
            } else {
                return 'Invoice'
            }
        },
        getInvoiceRef() {
            axios
                .get(`/api/v1/invoices/${this.invoice.iv_is_credit_for}/`)
                .then(response => {
                    this.invoice_ref = response.data.iv_invoice_number
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        },
        getItemTotal(item) {
            const unit_price = item.it_unit_price
            const quantity = item.it_quantity
            const net = unit_price * quantity
            const gross = net + (net * (item.it_vat_rate / 100))
            return parseFloat(gross).toFixed(2)
        },
        async setAsPaid() {
            this.invoice.iv_is_paid = true
            await axios
                .patch(`/api/v1/invoices/${this.invoice.iv_id}/`, this.invoice)
                .then(response => {
                    toast({
                        message: 'Invoice paid!',
                        type: 'is-success',
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 2000,
                        position: 'top-center',
                    })
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        },
        async createCreditNote() {

            // update invoice as credited
            this.invoice.iv_is_credited = true
            await axios
                .patch(`/api/v1/invoices/${this.invoice.iv_id}/`, this.invoice)
                .then(response => {
                    toast({
                        message: 'Invoice updated!',
                        type: 'is-danger',
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 2000,
                        position: 'bottom-right',
                    })
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
            
            // create related credit note
            let creditNote = this.invoice
            creditNote.iv_is_credit_for = this.invoice.iv_id // relate invoice and cn
            creditNote.iv_is_credited = false
            creditNote.iv_invoice_type = 'credit_note'

            await axios
                .post('api/v1/invoices/', creditNote)
                .then(response => {
                    toast({
                        message: 'Credit note created!',
                        type: 'is-success',
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 2000,
                        position: 'bottom-right',
                    })
                    this.$router.push('/dashboard/invoices')
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        },
        sendReminder() {
            axios
                .get(`/api/v1/invoices/${this.invoice.iv_id}/send-reminder/`)
                .then(response => {
                    toast({
                        message: 'The reminder was sent',
                        type: 'is-success',
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 2000,
                        position: 'bottom-right',
                    })
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
            }
    }
}
</script>