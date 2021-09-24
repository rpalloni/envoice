import json
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

# docker-compose exec envoice_api bash
# run migrations
# run test: python manage.py test core

# WARNING: each test must start with "test" to be visible

class SignupTests(APITestCase):

    def test_signup(self):
        data = {"username": "test1@testcase.eu", "password": "pwd_12345"}
        response = self.client.post("/api/v1/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class InvoiceTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="test2@testcase.eu", password="pwd_6789")
        self.token = Token.objects.create(user=self.user)
        self.api_authentication()

    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key) # token header

    def test_invoices(self):
        response = self.client.get("/api/v1/invoices/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
