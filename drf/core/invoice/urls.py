from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import InvoiceViewSet, ItemViewSet, generate_pdf, send_reminder, admin_invoice_pdf

router = DefaultRouter()
router.register('invoices', InvoiceViewSet, basename='invoices')
router.register('items', ItemViewSet, basename='items')

urlpatterns = [
    path('', include(router.urls)),
    path('admin/<int:invoice_id>/pdf/',admin_invoice_pdf,  name='admin_invoice_pdf'),
    path('invoices/<int:invoice_id>/generate-pdf/',generate_pdf, name='generate_pdf'),
    path('invoices/<int:invoice_id>/send-reminder/',send_reminder, name='send_reminder')
]