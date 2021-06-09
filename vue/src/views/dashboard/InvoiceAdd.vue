<template>
    <div class="page-add-invoice">
        <div class="columns is-multiline">
            <div class="column is-12">
                <h1 class="title">Add invoice</h1>
            </div>
            <div class="column is-12">
                <h2 class="is-size-5 mb-4 has-text-weight-bold">Client</h2>
                <div class="select">
                    <select name="client" v-model="client">
                        <option value="">--- Select client ---</option>
                        <option v-for="client in clients" v-bind:key="client.cl_id" v-bind:value="client">
                            {{ client.cl_name }}
                        </option>
                    </select>
                </div>

                <div class="box mt-4" v-if="client">
                    <p><strong>{{ client.cl_name }}</strong></p>
                    <p><strong>Email:</strong> {{ client.cl_email }}</p>
                    <p v-if="client.cl_address1"> {{ client.cl_address1 }}</p>
                    <p v-if="client.cl_address2"> {{ client.cl_address2 }}</p>
                    <p v-if="client.cl_zipcode || client.cl_place"> {{ client.cl_zipcode }} {{ client.cl_place }}</p>
                    <p v-if="client.cl_country"> {{ client.cl_country }}</p>
                </div>
            </div>

            <div class="column is-12">
                <h2 class="is-size-5 mb-4 has-text-weight-bold">Items</h2>
                <ItemForm 
                v-for="item in invoice.items" 
                v-bind:key="item.item_num" 
                v-bind:initialItem="item"
                v-on:updatePrice="updateTotals">
                </ItemForm>
                <button class="button is-light" @click="addItem">Add+</button>
            </div>

            <div class="column is-12">
                <div class="field">
                    <label class="label">Due days</label>
                    <div class="control">
                        <input class="input" type="number" placeholder="Due days" v-model="invoice.iv_due_days">
                    </div>
                </div>
            </div>

             <div class="column is-12">
                <div class="field">
                    <label class="label">Sender reference</label>
                    <div class="control">
                        <input class="input" type="text" placeholder="Sender reference" v-model="invoice.iv_sender_reference">
                    </div>
                </div>
            </div>

            <div class="column is-12">
                <h2 class="is-size-5 mb-4 has-text-weight-bold">Invoice Total:</h2>

                <p><strong>Net amount</strong>: {{ invoice.iv_net_amount }}</p>
                <p><strong>Vat amount</strong>: {{ invoice.iv_vat_amount }}</p>
                <p><strong>Total amount</strong>: {{ invoice.iv_gross_amount }}</p>
            </div>

            <div class="column is-12">
                <button class="button is-success" @click="saveInvoice">Save</button>
            </div>   

        </div>
    </div>
</template>

<script>
import axios from 'axios'
import {toast} from 'bulma-toast'

// import component
import ItemForm from '@/components/ItemForm.vue' // @ = src

export default {
    name: 'InvoiceAdd',
    components: {
        // register component
        ItemForm
    },
    data() {
        return {
            invoice: {
                items: [
                    {
                        //item_num: 0,
                        it_descr: '',
                        it_unit_price: 0,
                        it_quantity: 1,
                        it_vat_rate: 0,
                        it_net_amount: 0
                    }
                ],
                iv_due_days: 14,
                iv_sender_reference: '',
                iv_net_amount: 0,
                iv_vat_amount: 0,
                iv_gross_amount: 0
            },
            client: '',
            clients: []
        }
    },
    async mounted() {
        // mounted (load data in template) awaits until clients data are received
        await this.getClients()
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
        addItem() {
            this.invoice.items.push({
                item_num: this.invoice.items.length,
                it_descr: '',
                it_unit_price: '',
                it_quantity: 1,
                it_vat_rate: 0,
                it_net_amount: 0
            })
        },
        updateTotals(changedItem) {
            let net_amount = 0
            let vat_amount = 0
            let item = this.invoice.items.filter(i => i.item_num === changedItem.item_num)
            item = changedItem
            for (let i = 0; i < this.invoice.items.length; i++) {
                const vat_rate = this.invoice.items[i].it_vat_rate
                vat_amount += this.invoice.items[i].it_net_amount * (vat_rate / 100)
                net_amount += this.invoice.items[i].it_net_amount
            }
            this.invoice.iv_net_amount = net_amount
            this.invoice.iv_vat_amount = vat_amount
            this.invoice.iv_gross_amount = net_amount + vat_amount
            this.invoice.iv_discount_amount = 0
        },
        saveInvoice() {
            this.invoice.iv_client = this.client
            axios
                .post('/api/v1/invoices/', this.invoice)
                .then(response => {
                    console.log(response.data)
                    toast({
                        message: 'The invoice was added',
                        type: 'is-success',
                        dismissible: true,
                        pauseOnHover: true,
                        duration: 2000,
                        position: 'top-center',
                    })
                    this.$router.push('/dashboard/invoices')
                })
                .catch(error => {
                    console.log(JSON.stringify(error))
                })
        }
    }
    
}
</script>

<style lang="scss">
    .select, .select select {
        width: 100%;
    }
</style>