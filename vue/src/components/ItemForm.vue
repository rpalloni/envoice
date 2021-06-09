<template>
    <div class="columns">
        <div class="column is-4">
            <div class="field">
                <label>Description</label>
                <div class="control">
                    <input type="text" class="input" v-model="item.it_descr">
                </div>
            </div>
        </div>

        <div class="column is-2">
            <div class="field">
                <label>Price</label>
                <div class="control">
                    <input type="text" class="input" v-model="item.it_unit_price">
                </div>
            </div>
        </div>

        <div class="column is-2">
            <div class="field">
                <label>Quantity</label>
                <div class="control">
                    <input type="number" class="input" v-model="item.it_quantity">
                </div>
            </div>
        </div>

        <div class="column is-2">
            <div class="field">
                <label>Vat rate</label>
                <div class="control">
                    <div class="select">
                        <select v-model="item.it_vat_rate">
                            <option value="0">0%</option>
                            <option value="4">4%</option>
                            <option value="10">10%</option>
                            <option value="22">22%</option>
                        </select>
                    </div>
                </div>
            </div>
        </div>

        <div class="column is-2">
            <div class="field">
                <label>Gross amount</label>
                <div class="control">
                    <input type="text" class="input" v-bind:value="gross_amount" disabled>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: 'ItemForm',
    props: {
        initialItem: Object // pass item to component
    },
    data() {
        return {
            item: this.initialItem
        }
    },
    computed: {
        // recalculate each time a property change
        gross_amount() {
            const item_pr = this.item.it_unit_price
            const item_qnt = this.item.it_quantity
            const item_vat = this.item.it_vat_rate
            this.item.it_net_amount = item_pr * item_qnt
            this.$emit('updatePrice', this.item) // send update from ItemForm to InvoiceAdd
            return this.item.it_net_amount + (this.item.it_net_amount * (item_vat / 100))
        }
    }
}
</script>