from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

from .models import OrganizationalUnit
from .models import HardwareAsset
from .models import SoftwareAsset

# Create your views here.

def index(request):
    return HttpResponse("This is the HWAM index page")

def ou_index(request):
    ou_list = OrganizationalUnit.objects.order_by('unit_name')
    context = {
            'ou_list': ou_list,
    }
    return render(request, 'hwam/ou_index.html', context)

def hw_index(request):
    hw_list = HardwareAsset.objects.order_by('org_unit')
    context = {
            'hw_list': hw_list,
    }
    return render(request, 'hwam/ou_index.html', context)

def sw_index(request):
    sw_list = SoftwareAsset.objects.order_by('org_unit')
    context = {
            'sw_list': sw_list,
    }
    return render(request, 'hwam/ou_index.html', context)

def ou_detail(request, organizational_unit_id):
    response = "Details for organizational unit %s."
    return HttpResponse(response % organizational_unit_id)

def hw_detail(request, hardware_asset_id):
    response = "Details for hardware asset %s."
    return HttpResponse(response % hardware_asset_id)

def sw_detail(request, software_asset_id):
    response = "Details for software asset %s."
    return HttpResponse(response % software_asset_id)

