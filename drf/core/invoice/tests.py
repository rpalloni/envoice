import json

from rest_framework import status
from rest_framework.test import APITestCase

from models import Invoice
from .serializers import InvoiceSerializer
# run test: python manage.py test


class InvoiceViewSetTestCase(APITestCase):

    def setUp(self):
        pass

    def api_authentication(self):
        pass

    def test_invoices(self):
        response = self.client.get("/api/v1/invoices/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
