from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView

from .models import OrganizationalUnit
from .models import HardwareAsset
from .models import SoftwareAsset

# Create your views here.

def index(request):
    return render(request, 'hwam/index.html')

class OUIndexView(ListView):
    model = OrganizationalUnit
    template_name = 'hwam/ou_index.html'
    context_object_name = 'ou_list'

    def get_queryset(self):
        """Return a list of parent-less organizational units"""
        parents = OrganizationalUnit.objects.filter(parent_ou=None)
        return parents

class HWIndexView(ListView):
    model = HardwareAsset
    template_name = 'hwam/hw_index.html'
    context_object_name = 'hw_list'

    def get_queryset(self):
        """Return a list of parent-less hardware assets"""
        return HardwareAsset.objects.filter(
                parent_hardware=None).order_by('org_unit')

class HWSearchView(ListView):
    model = HardwareAsset
    template_name = "hwam/hw_search.html"
    paginate_by = 20
    def get_queryset(self):
        filter_val = self.request.GET.get('filter', '')
        #order = self.request.GET.get('orderby', 'name')
        #new_context = HardwareAsset.objects.filter(
        #    name=filter_val,
        #).order_by(order)
        new_context = HardwareAsset.objects.filter(
            name=filter_val,
        )
        return new_context
    def get_context_data(self, **kwargs):
        context = super(HWSearchView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        #context['orderby'] = self.request.GET.get('orderby', 'org_unit')
        return context

class SWIndexView(ListView):
    model = SoftwareAsset
    template_name = 'hwam/sw_index.html'
    context_object_name = 'sw_list'

    def get_queryset(self):
        """Return a tuple of software assets"""
        p = SoftwareAsset.objects.exclude(
            parent_hardware=None).order_by('org_unit')
        c = SoftwareAsset.objects.filter(
            parent_hardware=None).order_by('org_unit')
        if len(p) + len(c) > 0:
            return (p, c)
        else:
            return None

class OUDetailView(DetailView):
    model = OrganizationalUnit
    template_name = 'hwam/ou_detail.html'
    context_object_name = 'ou'

class HWDetailView(DetailView):
    model = HardwareAsset
    template_name = 'hwam/hw_detail.html'
    context_object_name = 'hw'

class SWDetailView(DetailView):
    model = SoftwareAsset
    template_name = 'hwam/sw_detail.html'
    context_object_name = 'sw'

class OUCreateView(CreateView):
    model = OrganizationalUnit
    fields = ['name', 'desc', 'unit_contact', 'parent_ou']
    def get_success_url(self):
        return reverse_lazy('hwam:ou_detail', args=(self.object.id,))

class HWCreateView(CreateView):
    model = HardwareAsset
    fields = ['name', 'desc', 'org_unit',
            'asset_owner', 'asset_custodian',
            'parent_hardware',
            'hardware_type', 'property_id',
            'device_maker', 'device_model',
            'location', 'status',
            'date_added', 'date_eol',
            ]
    def get_success_url(self):
        return reverse_lazy('hwam:hw_detail', args=(self.object.id,))

class SWCreateView(CreateView):
    model = SoftwareAsset
    fields = [
            'name', 'desc', 'org_unit',
            'custodian_swam', 'custodian_csm', 'custodian_vul',
            'parent_hardware', 'parent_software',
            'software_type', 'sw_property_id',
            'package_name', 'package_version',
            'status',
            'date_added', 'date_eol',
            ]
    def get_success_url(self):
        return reverse_lazy('hwam:sw_detail', args=(self.object.id,))

class OUUpdateView(UpdateView):
    model = OrganizationalUnit
    fields = ['name', 'desc', 'unit_contact', 'parent_ou']
    def get_success_url(self):
        return reverse_lazy('hwam:ou_detail', args=(self.object.id,))

class HWUpdateView(UpdateView):
    model = HardwareAsset
    fields = ['name', 'desc', 'org_unit',
            'asset_owner', 'asset_custodian',
            'parent_hardware',
            'hardware_type', 'property_id',
            'device_maker', 'device_model',
            'location', 'status',
            'date_added', 'date_eol',
            ]
    def get_success_url(self):
        return reverse_lazy('hwam:hw_detail', args=(self.object.id,))

class SWUpdateView(UpdateView):
    model = SoftwareAsset
    fields = [
            'name', 'desc', 'org_unit',
            'custodian_swam', 'custodian_csm', 'custodian_vul',
            'parent_hardware', 'parent_software',
            'software_type', 'sw_property_id',
            'package_name', 'package_version',
            'status',
            'date_added', 'date_eol',
            ]
    def get_success_url(self):
        return reverse_lazy('hwam:sw_detail', args=(self.object.id,))


