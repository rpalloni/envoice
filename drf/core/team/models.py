from tabnanny import verbose
from django.db import models
from django.contrib.auth.models import User

class Team(models.Model):
    tm_id = models.AutoField(primary_key=True) # no auto generation of pk
    tm_name = models.CharField(verbose_name='Name', max_length=255)
    tm_org_number = models.CharField(verbose_name='Organisation Number', max_length=255, blank=True, null=True)
    tm_first_invoice_nbr = models.IntegerField(default=1)
    tm_bank_account = models.CharField(verbose_name='Bank Account', max_length=255, blank=True, null=True)
    tm_created_by = models.ForeignKey(User, 
                            verbose_name='Created by',
                            db_column = 'tm_created_by',
                            related_name='teams', 
                            on_delete=models.CASCADE)

    def __str__(self):
        return self.tm_name

class TeamCreditBalance(models.Model):
    tc_id = models.AutoField(primary_key=True) # no auto generation of pk
    tc_team = models.ForeignKey(Team,
                        verbose_name='Team',
                        db_column='tc_team',
                        related_name='credit_balance',
                        on_delete=models.CASCADE)
    tc_balance = models.DecimalField(verbose_name='Credit balance', max_digits=10, decimal_places=2)

class TeamCashBalance(models.Model):
    th_id = models.AutoField(primary_key=True) # no auto generation of pk
    th_team = models.ForeignKey(Team,
                        verbose_name='Team',
                        db_column='th_team',
                        related_name='cash_balance',
                        on_delete=models.CASCADE)
    th_balance = models.DecimalField(verbose_name='Cash balance', max_digits=10, decimal_places=2)