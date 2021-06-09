from django.shortcuts import render
from django.core.exceptions import PermissionDenied

from rest_framework import viewsets

from .serializers import ClientSerializer
from .models import Client

class ClientViewSet(viewsets.ModelViewSet):
    serializer_class = ClientSerializer
    
    # override ModelViewSet methods to retrive and create clients
    def get_queryset(self):
        #return Client.objects.filter(cl_created_by=self.request.user) # show only userXY clients
        return self.request.user.clients.all() # different filter syntax using model related_name

    def perform_create(self, serializer):
        serializer.save(
            cl_created_by = self.request.user # add fields not coming from the form
        )

    def perform_update(self, serializer):
        obj = self.get_object()
        if self.request.user != obj.cl_created_by:
            raise PermissionDenied('No permission for update this element')
        serializer.save()