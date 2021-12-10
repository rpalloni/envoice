import decimal
from datetime import timedelta

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import User

from core.client.models import Client
from core.team.models import Team

# docker-compose exec envoice_api bash
# use shell: python manage.py shell

# invoice head
class Invoice(models.Model):
    INVOICE = 'invoice'
    CREDIT_NOTE = 'credit_note'

    CHOICES_TYPE = (
        (INVOICE, 'Invoice'),
        (CREDIT_NOTE, 'Credit note')
    )
    iv_id = models.AutoField(primary_key=True) # no auto generation of pk
    iv_invoice_number = models.IntegerField(verbose_name='Invoice Number', default=1)
    iv_year = models.IntegerField(verbose_name='Invoice Year', validators=[MaxValueValidator(2100)],
                                    blank=True, null=True, help_text="Generated from created at year")
    iv_team = models.ForeignKey(Team, 
                    verbose_name='Related Team',
                    db_column = 'iv_team',
                    related_name='invoices', # one team - many invoices
                    on_delete=models.CASCADE)
    iv_client = models.ForeignKey(Client, 
                        verbose_name='Related Client',
                        db_column = 'iv_client',
                        related_name='invoices', # one client - many invoices
                        on_delete=models.CASCADE)
    iv_sender_reference = models.CharField(verbose_name='Sender Reference', max_length=255, blank=True, null=True)
    iv_invoice_type = models.CharField(verbose_name='Invoice Type', max_length=20, choices=CHOICES_TYPE, default=INVOICE)
    iv_due_days = models.IntegerField(verbose_name='Due days', default=14)
    iv_is_credit_for = models.ForeignKey('self', # only for credit note => reference to self
                            verbose_name='Credit for invoice',
                            db_column = 'iv_is_credit_for',
                            on_delete=models.CASCADE, 
                            blank=True, 
                            null=True)
    iv_is_credited = models.BooleanField(verbose_name='Is credited', default=False)
    iv_is_sent = models.BooleanField(verbose_name='Is sent', default=False)
    iv_is_paid = models.BooleanField(verbose_name='Is paid', default=False)
    iv_bank_account = models.CharField(verbose_name='Bank Account', max_length=255, blank=True, null=True)
    iv_gross_amount = models.DecimalField(verbose_name='Gross amount', max_digits=10, decimal_places=2)
    iv_vat_amount = models.DecimalField(verbose_name='VAT amount', max_digits=10, decimal_places=2)
    iv_net_amount = models.DecimalField(verbose_name='Net amount', max_digits=10, decimal_places=2)
    iv_discount_amount = models.DecimalField(verbose_name='Discount amount', max_digits=10, decimal_places=2)
    iv_created_by = models.ForeignKey(User, 
                            verbose_name='Created by',
                            db_column = 'iv_created_by',
                            related_name='created_invoices', 
                            on_delete=models.CASCADE)
    iv_modified_by = models.ForeignKey(User, 
                            verbose_name='Modified by',
                            db_column = 'iv_modified_by',
                            related_name='modified_invoices', 
                            on_delete=models.CASCADE)
    iv_created_at = models.DateTimeField(auto_now_add=True)
    iv_modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-iv_created_at',)

    @property
    def get_due_date(self):
        return (self.iv_created_at + timedelta(days=self.iv_due_days)).strftime("%Y-%m-%d")

    @property
    def get_year(self):
        return self.iv_created_at.strftime('%Y')

    def __str__(self):
        return f'{self.iv_client.cl_name} - {self.iv_invoice_number}'


@receiver(post_save,sender=Invoice)
def save_state(sender,instance,**kwargs):
    '''update invoice year from create date '''
    if instance.iv_created_at:
        Invoice.objects.update(iv_year=instance.iv_created_at.strftime('%Y'))

    
# invoice rows
class Item(models.Model):
    it_id = models.AutoField(primary_key=True) # no auto generation of pk
    it_invoice = models.ForeignKey(Invoice, 
                        verbose_name='Related Invoice',
                        db_column = 'it_invoice',
                        related_name='items', 
                        on_delete=models.CASCADE)
    it_descr = models.CharField(verbose_name='Description', max_length=255)
    it_quantity = models.IntegerField(verbose_name='Quantity', default=1)
    it_unit_price = models.DecimalField(verbose_name='Price', max_digits=10, decimal_places=2)
    it_net_amount = models.DecimalField(verbose_name='Net amount', max_digits=10, decimal_places=2)
    it_vat_rate = models.IntegerField(verbose_name='VAT rate', default=0)
    it_discount_rate = models.IntegerField(verbose_name='Discount rate', default=0)
    
    def get_gross_amount(self):
        vat_rate = decimal.Decimal(self.it_vat_rate/100) # float to decimal
        return round(self.it_net_amount + (self.it_net_amount * vat_rate), 2)

    def __str__(self):
        return f'{self.it_descr} - {self.it_unit_price}'



