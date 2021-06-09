from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from .models import Invoice, Item


def invoice_pdf(invoice):
    return mark_safe('<a href="{}">PDF</a>'.format(
        reverse('admin_invoice_pdf', args=[invoice.iv_id])) # forward to function
        )
invoice_pdf.short_description = 'Download pdf'


class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['iv_invoice_number', 'iv_client', invoice_pdf] # add selection menu
    readonly_fields = ['iv_year'] # set read only fields


admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Item)
