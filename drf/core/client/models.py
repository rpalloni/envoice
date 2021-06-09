from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    cl_id = models.AutoField(primary_key=True) # no auto generation of pk
    cl_name = models.CharField(verbose_name='Name', max_length=255)
    cl_email = models.EmailField(verbose_name='Email')
    cl_org_number = models.CharField(verbose_name='Organisation Number', max_length=255, blank=True, null=True)
    cl_address1 = models.CharField(verbose_name='Address1', max_length=255, blank=True, null=True)
    cl_address2 = models.CharField(verbose_name='Address2', max_length=255, blank=True, null=True)
    cl_zipcode = models.CharField(verbose_name='ZipCode', max_length=255, blank=True, null=True)
    cl_place = models.CharField(verbose_name='Place', max_length=255, blank=True, null=True)
    cl_country = models.CharField(verbose_name='Country', max_length=255, blank=True, null=True)
    cl_contact_person = models.CharField(verbose_name='Contact Person', max_length=255, blank=True, null=True)
    cl_contact_reference = models.CharField(verbose_name='Contact Reference', max_length=255, blank=True, null=True)
    cl_created_by = models.ForeignKey(User, 
                            verbose_name='Created by',
                            db_column = 'cl_created_by',
                            related_name='clients', 
                            on_delete=models.CASCADE)
    cl_created_at = models.DateTimeField(verbose_name='Created at', auto_now_add=True)

    def __str__(self):
        return self.cl_name
