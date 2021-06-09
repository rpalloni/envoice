from django.shortcuts import render
from django.core.exceptions import PermissionDenied

from rest_framework import viewsets

from .serializers import TeamSerializer
from .models import Team

class TeamViewSet(viewsets.ModelViewSet):
    serializer_class = TeamSerializer

    # override ModelViewSet methods to retrive and create teams
    def get_queryset(self):
        teams = self.request.user.teams.all() # filter syntax using model related_name

        if not teams:
            Team.objects.create(tm_name='', tm_org_number='', tm_created_by=self.request.user)

        return self.request.user.teams.filter(tm_created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(
            tm_created_by = self.request.user # add fields not coming from the form
        )

    def perform_update(self, serializer):
        obj = self.get_object()
        if self.request.user != obj.tm_created_by:
            raise PermissionDenied('No permission for update this element')
        serializer.save()