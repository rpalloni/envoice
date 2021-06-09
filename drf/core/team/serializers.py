# serialize data from db to app in json

from rest_framework import serializers

from .models import Team

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        read_only_fields = (
            'tm_created_by'
        ),
        fields = (
            'tm_id',
            'tm_name',
            'tm_org_number',
            'tm_first_invoice_nbr',
            'tm_bank_account'
        )