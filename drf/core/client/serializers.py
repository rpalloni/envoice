# serialize data from db to app in json

from rest_framework import serializers

from .models import Client

from core.invoice.models import Invoice

class ClientInvoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Invoice
        fields = (
            "iv_id",
            "iv_invoice_number",
            "iv_is_sent",
            "iv_is_paid",
            "iv_gross_amount",
            "iv_vat_amount",
            "iv_net_amount",
            "get_due_date",
            "iv_invoice_type"
        )

class ClientSerializer(serializers.ModelSerializer):

    invoices = ClientInvoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        read_only_fields = (
            'cl_name',
            'cl_created_at',
            'cl_created_by'
        ),
        fields = (
            'cl_id',
            'cl_name',
            'cl_email',
            'cl_org_number',
            'cl_address1',
            'cl_address2',
            'cl_zipcode',
            'cl_place',
            'cl_country',
            'cl_contact_person',
            'cl_contact_reference',
            'invoices'
        )
