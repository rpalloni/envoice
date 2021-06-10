# serialize data from db to app in json

from rest_framework import serializers

from .models import Invoice, Item
from core.client.serializers import ClientSerializer


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        read_only_fields = (
            'it_invoice',
        )
        fields = (
            'it_id',
            'it_descr',
            'it_quantity',
            'it_unit_price',
            'it_net_amount',
            'it_vat_rate',
            'it_discount_rate'
        )


class InvoiceSerializer(serializers.ModelSerializer):
    #iv_client = serializers.StringRelatedField() # Client.__str__
    iv_client = ClientSerializer(read_only=True)
    items = ItemSerializer(many=True)

    iv_bank_account = serializers.CharField(required=False) # not visible in frontend

    class Meta:
        model = Invoice
        read_only_fields = (
            'iv_team',
            'iv_invoice_number',
            'iv_created_by',
            'iv_modified_by',
            'iv_created_at',
            'iv_modified_at'
        ),
        fields = (
            'iv_id',
            'iv_invoice_number',
            'iv_year',
            'iv_sender_reference',
            'iv_invoice_type',
            'iv_due_days',
            'iv_is_credit_for',
            'iv_is_credited',
            'iv_is_sent',
            'iv_is_paid',
            'iv_bank_account',
            'iv_gross_amount',
            'iv_vat_amount',
            'iv_net_amount',
            'iv_discount_amount',

            'iv_client', # related client
            'items', # related items
            'get_due_date', # property
            'get_year' # property
        )

    # add new invoice
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        invoice = Invoice.objects.create(**validated_data)

        for item in items_data:
            Item.objects.create(it_invoice=invoice, **item)
        
        return invoice

    # update invoice data
    def update(self, instance, validated_data):
        # handle nested relation
        items_data = validated_data.pop('items')
        items = instance.items 

        # update fields
        instance.iv_is_paid = validated_data.get('iv_is_paid', instance.iv_is_paid)
        instance.iv_is_credited = validated_data.get('iv_is_credited', instance.iv_is_credited)
        instance.save()
        return instance


'''
python manage.py shell

from core.invoice.models import Invoice
from core.invoice.serializers import InvoiceSerializer
inv = Invoice.objects.all()
invser = InvoiceSerializer(inv, many=True)
invser.data
'''