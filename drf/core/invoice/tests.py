from model_bakery import baker # delegate field creation

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from core.client.models import Client
from core.team.models import Team
from core.invoice.models import Invoice, Item

# docker-compose exec envoice_api bash
# run migrations
# run test: python manage.py test core

# WARNING: each test must start with 'test' to be visible

class SignupTests(APITestCase):

    def test_signup(self):
        data = {'username': 'test1@testcase.eu', 'password': 'pwd_12345'}
        response = self.client.post('/api/v1/users/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class InvoiceTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='test2@testcase.eu', password='pwd_6789')
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key) # token header

    def test_get_invoices(self):
        response = self.client.get('/api/v1/invoices/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invoice(self):
        self.client.force_authenticate(user=self.user) # directly authenticate the request for testing
        self.invoice = baker.make(Invoice, iv_id=888)
        response = self.client.get('/api/v1/invoices/', kwargs={'iv_id':888})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invoice_create(self):
        client = baker.make(Client)
        team = baker.make(Team)
        invoice = Invoice.objects.create(
            # not null fields
            iv_client=client,
            iv_team=team,
            iv_invoice_number=123,
            iv_gross_amount=1200,
            iv_vat_amount=200,
            iv_net_amount=1000,
            iv_discount_amount=5,
            iv_created_by=self.user,
            iv_modified_by=self.user)
        self.assertEqual(str(invoice), f'{client.cl_name} - {invoice.iv_invoice_number}')
        self.assertEqual(Invoice.objects.count(),1)

    def test_invoice_has_items(self):
        item1 = baker.make(Item)
        item2 = baker.make(Item)
        invoice = baker.make(Invoice)
        invoice.items.add(item1)
        invoice.items.add(item2)
        self.assertEqual(invoice.items.count(), 2)

    