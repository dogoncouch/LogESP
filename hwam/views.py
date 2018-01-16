from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import OrganizationalUnit
from .models import HardwareAsset
from .models import SoftwareAsset

# Create your views here.

def index(request):
    return HttpResponse("This is the HWAM index page")

class OUIndexView(generic.ListView):
    model = OrganizationalUnit
    template_name = 'hwam/ou_index.html'
    context_object_name = 'ou_list'

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

def ou_detail(request, organizational_unit_id):
    ou = get_object_or_404(OrganizationalUnit, pk=organizational_unit_id)
    return render(request, 'hwam/ou_detail.html', {'ou': ou})

def hw_detail(request, hardware_asset_id):
    hw = get_object_or_404(HardwareAsset, pk=hardware_asset_id)
    return render(request, 'hwam/hw_detail.html', {'hw': hw})

def sw_detail(request, software_asset_id):
    sw = get_object_or_404(SoftwareAsset, pk=software_asset_id)
    return render(request, 'hwam/sw_detail.html', {'sw': sw})

