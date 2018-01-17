from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views import generic

from .models import OrganizationalUnit
from .models import HardwareAsset
from .models import SoftwareAsset

# Create your views here.

def index(request):
    return render(request, 'hwam/index.html')

class OUIndexView(generic.ListView):
    model = OrganizationalUnit
    template_name = 'hwam/ou_index.html'
    context_object_name = 'ou_list'

    def get_queryset(self):
        """Return a list of organizational units"""
        return OrganizationalUnit.objects.order_by('parent_ou')

class HWIndexView(generic.ListView):
    model = HardwareAsset
    template_name = 'hwam/hw_index.html'
    context_object_name = 'hw_list'

    def get_queryset(self):
        """Return a list of hardware assets"""
        return HardwareAsset.objects.order_by('org_unit')

class SWIndexView(generic.ListView):
    model = SoftwareAsset
    template_name = 'hwam/sw_index.html'
    context_object_name = 'sw_list'

    def get_queryset(self):
        """Return a list of software assets"""
        return SoftwareAsset.objects.order_by('org_unit')

class OUDetailView(generic.DetailView):
    model = OrganizationalUnit
    template_name = 'hwam/ou_detail.html'
    context_object_name = 'ou'

class HWDetailView(generic.DetailView):
    model = HardwareAsset
    template_name = 'hwam/hw_detail.html'
    context_object_name = 'hw'

class SWDetailView(generic.DetailView):
    model = SoftwareAsset
    template_name = 'hwam/sw_detail.html'
    context_object_name = 'sw'
