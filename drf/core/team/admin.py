from django.contrib import admin

from .models import Team, TeamCreditBalance, TeamCashBalance

admin.site.register(Team)
admin.site.register(TeamCreditBalance)
admin.site.register(TeamCashBalance)
