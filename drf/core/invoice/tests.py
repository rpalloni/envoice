import json

from rest_framework import status
from rest_framework.test import APITestCase

# run test: python manage.py test core


class InvoiceTests(APITestCase):

    def test_invoices(self):
        response = self.client.get("/api/v1/invoices/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
