from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse

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
    return render(request, 'hwam/hw_index.html', context)

def sw_index(request):
    sw_list = SoftwareAsset.objects.order_by('org_unit')
    context = {
            'sw_list': sw_list,
    }
    return render(request, 'hwam/sw_index.html', context)

def ou_detail(request, organizational_unit_id):
    ou = get_object_or_404(OrganizationalUnit, pk=organizational_unit_id)
    return render(request, 'hwam/ou_detail.html', {'ou': ou})

def hw_detail(request, hardware_asset_id):
    hw = get_object_or_404(HardwareAsset, pk=hardware_asset_id)
    return render(request, 'hwam/hw_detail.html', {'hw': hw})

def sw_detail(request, software_asset_id):
    sw = get_object_or_404(SoftwareAsset, pk=software_asset_id)
    return render(request, 'hwam/sw_detail.html', {'sw': sw})

