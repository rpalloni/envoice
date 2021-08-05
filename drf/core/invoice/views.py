import json
import pdfkit
import time

from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMultiAlternatives

from rest_framework import viewsets
from rest_framework import status, authentication, permissions
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from .serializers import InvoiceSerializer, ItemSerializer
from .models import Invoice, Item
# from .query import FindQuery
from core.client.models import Client
from core.team.models import Team
from core.utils.pagination import CustomPagination

PDFCSS = str(settings.BASE_DIR) + '/static/css/pdf.css'


class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        
        # input value from search page
        user = self.request.user.id
        year = self.request.GET.get('selected_year')
        client = self.request.GET.get('selected_client')

        filters = {}

        if user:
            filters['iv_created_by'] = user

        if year:
            filters['iv_year'] = year

        if client:
            filters['iv_client'] = client

        # print(Invoice.objects.filter(**filters).query)
        result = Invoice.objects.filter(**filters)
        time.sleep(3) # fake delay to test laoding spinner

        return result


        # q = FindQuery()
        # user = self.request.user.id
        # year = self.request.GET.get('selected_year')
        # client = self.request.GET.get('selected_client')

        # q.set_filters(user, year, client)
        # qs = q.apply_filter()
        # print(qs)
        # result = Invoice.objects.filter(iv_id__in=[q.iv_id for q in qs])


    def perform_create(self, serializer):
        client_id = self.request.data['iv_client']['cl_id']
        team = self.request.user.teams.first()
        client = self.request.user.clients.get(cl_id=client_id)
        invoice_number = team.tm_first_invoice_nbr
        team.tm_first_invoice_nbr = invoice_number + 1
        team.save()
        serializer.save(iv_created_by=self.request.user,
                        iv_team=team,
                        iv_client=client,
                        iv_modified_by=self.request.user,
                        iv_invoice_number=invoice_number,
                        iv_bank_account=team.tm_bank_account)

    def perform_update(self, serializer):
        obj = self.get_object()
        if self.request.user != obj.iv_created_by:
            raise PermissionDenied('No permission for update this element')
        serializer.save()


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer

    def get_queryset(self):
        invoice_id = self.request.GET.get('invoice_id')
        return Item.objects.filter(it_invoice=invoice_id)


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def generate_pdf(request, invoice_id):
    invoice = get_object_or_404(Invoice, iv_id=invoice_id, iv_created_by=request.user)
    team = Team.objects.filter(tm_created_by=request.user).first()
    template_name = 'pdf_invoice.html'
    if invoice.iv_is_credit_for:
        template_name = 'pdf_creditnote.html'
    template = get_template(template_name)
    html = template.render(context={'invoice': invoice, 'team': team})
    pdf = pdfkit.from_string(html, False, options={}, css=PDFCSS)
    # response to browser
    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
    return response


@api_view(['GET'])
@authentication_classes([authentication.TokenAuthentication])
@permission_classes([permissions.IsAuthenticated])
def send_reminder(request, invoice_id):
    invoice = get_object_or_404(Invoice, iv_id=invoice_id, iv_created_by=request.user)
    team = Team.objects.filter(tm_created_by=request.user).first()

    subject = 'Unpaid invoice'
    from_email = 'no-reply@envoice.eu'
    to = [invoice.iv_client.cl_email]
    text_content = 'You have an unpaid invoice. Invoice number: #' + str(invoice.iv_invoice_number)
    html_content = 'You have an unpaid invoice. Invoice number: #' + str(invoice.iv_invoice_number)

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")

    template = get_template('pdf_invoice.html')
    html = template.render(context={'invoice': invoice, 'team': team})
    pdf = pdfkit.from_string(html, False, options={}, css=PDFCSS)

    if pdf:
        name = 'invoice_%s.pdf' % invoice.iv_invoice_number
        msg.attach(name, pdf, 'application/pdf')

    msg.send()

    return Response()


def admin_invoice_pdf(request, invoice_id):
    if request.user.is_superuser:
        invoice = get_object_or_404(Invoice, iv_id=invoice_id)
        template_name = 'pdf_invoice.html'
        if invoice.iv_is_credit_for:
            template_name = 'pdf_creditnote.html'
        template = get_template(template_name)
        html = template.render(context={'invoice': invoice})
        pdf = pdfkit.from_string(html, False, options={}, css=PDFCSS)
        # response to browser
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
        return response