from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin

from .models import OrganizationalUnit
from .models import HardwareAsset
from .models import SoftwareAsset

# Create your views here.

def index(request):
    return render(request, 'hwam/index.html')

def help_index(request):
    return render(request, 'hwam/help_index.html')

class OUIndexView(ListView):
    model = OrganizationalUnit
    template_name = 'hwam/ou_index.html'
    context_object_name = 'ou_list'
    permission_required = 'hwam.view_organizationalunit'

    def get_queryset(self):
        """Return a list of parent-less organizational units"""
        parents = OrganizationalUnit.objects.filter(parent_ou=None)
        return parents

class HWIndexView(ListView):
    model = HardwareAsset
    template_name = 'hwam/hw_index.html'
    context_object_name = 'hw_list'
    permission_required = 'hwam.view_hardwareasset'

    def get_queryset(self):
        """Return a list of parent-less hardware assets"""
        return HardwareAsset.objects.filter(
                parent_hardware=None).order_by('org_unit')

class HWSearchView(ListView):
    model = HardwareAsset
    template_name = "hwam/hw_search.html"
    context_object_name = 'hw_list'
    permission_required = 'hwam.view_hardwareasset'
    paginate_by = 20
    def get_queryset(self):
        filter_val = self.request.GET.get('filter')
        if filter_val and filter_val != '':
            new_context = HardwareAsset.objects.filter(
                name=filter_val,
            )
            return new_context
        else:
            return HardwareAsset.objects.all()
    def get_context_data(self, **kwargs):
        context = super(HWSearchView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        #context['orderby'] = self.request.GET.get('orderby', 'org_unit')
        return context

class SWIndexView(ListView):
    model = SoftwareAsset
    template_name = 'hwam/sw_index.html'
    context_object_name = 'sw_list'
    permission_required = 'hwam.view_softwareasset'

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

class SWSearchView(ListView):
    model = SoftwareAsset
    template_name = "hwam/sw_search.html"
    context_object_name = 'sw_list'
    permission_required = 'hwam.view_softwareasset'
    paginate_by = 20
    def get_queryset(self):
        filter_val = self.request.GET.get('filter')
        if filter_val and filter_val != '':
            new_context = SoftwareAsset.objects.filter(
                name=filter_val,
            )
            return new_context
        else:
            return SoftwareAsset.objects.all()
    def get_context_data(self, **kwargs):
        context = super(SWSearchView, self).get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        return context

class OUDetailView(DetailView):
    model = OrganizationalUnit
    template_name = 'hwam/ou_detail.html'
    context_object_name = 'ou'
    permission_required = 'hwam.view_organizationalunit'

class HWDetailView(DetailView):
    model = HardwareAsset
    template_name = 'hwam/hw_detail.html'
    context_object_name = 'hw'
    permission_required = 'hwam.view_hardwareasset'

class SWDetailView(DetailView):
    model = SoftwareAsset
    template_name = 'hwam/sw_detail.html'
    context_object_name = 'sw'
    permission_required = 'hwam.view_softwareasset'

class OUCreateView(PermissionRequiredMixin, CreateView):
    model = OrganizationalUnit
    permission_required = 'hwam.add_organizationalunit'
    fields = ['name', 'desc', 'unit_contact', 'parent_ou']
    def get_success_url(self):
        return reverse_lazy('hwam:ou_detail', args=(self.object.id,))

class HWCreateView(PermissionRequiredMixin, CreateView):
    model = HardwareAsset
    permission_required = 'hwam.add_hardwareasset'
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

class SWCreateView(PermissionRequiredMixin, CreateView):
    model = SoftwareAsset
    permission_required = 'hwam.add_softwareasset'
    fields = [
            'name', 'desc', 'org_unit',
            'custodian_swam', 'custodian_csm', 'custodian_vul',
            'parent_hardware', 'parent_software',
            'hostname', 'domain_name',
            'ip4_address_1', 'ip4_address_2',
            'ip4_address_3', 'ip4_address_4', 
            'ip4_address_5', 'ip4_address_6',
            'ip4_address_7', 'ip4_address_8', 
            'ip6_address_1', 'ip6_address_2',
            'ip6_address_3', 'ip6_address_4', 
            'ip6_address_5', 'ip6_address_6',
            'ip6_address_7', 'ip6_address_8', 
            'software_type', 'sw_property_id',
            'package_vendor', 'package_name', 'package_version',
            'status',
            'date_added', 'date_eol',
            ]
    def get_success_url(self):
        return reverse_lazy('hwam:sw_detail', args=(self.object.id,))

class OUUpdateView(PermissionRequiredMixin, UpdateView):
    model = OrganizationalUnit
    permission_required = 'hwam.change_organizationalunit'
    template_name = 'hwam/organizationalunit_update_form.html'
    fields = ['name', 'desc', 'unit_contact', 'parent_ou']
    def get_success_url(self):
        return reverse_lazy('hwam:ou_detail', args=(self.object.id,))

class HWUpdateView(PermissionRequiredMixin, UpdateView):
    model = HardwareAsset
    permission_required = 'hwam.change_hardwareasset'
    template_name = 'hwam/hardwareasset_update_form.html'
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

class SWUpdateView(PermissionRequiredMixin, UpdateView):
    model = SoftwareAsset
    template_name = 'hwam/softwareasset_update_form.html'
    permission_required = 'hwam.change_softwareasset'
    fields = [
            'name', 'desc', 'org_unit',
            'custodian_swam', 'custodian_csm', 'custodian_vul',
            'parent_hardware', 'parent_software',
            'hostname', 'domain_name',
            'ip4_address_1', 'ip4_address_2',
            'ip4_address_3', 'ip4_address_4', 
            'ip4_address_5', 'ip4_address_6',
            'ip4_address_7', 'ip4_address_8', 
            'ip6_address_1', 'ip6_address_2',
            'ip6_address_3', 'ip6_address_4', 
            'ip6_address_5', 'ip6_address_6',
            'ip6_address_7', 'ip6_address_8', 
            'software_type', 'sw_property_id',
            'package_vendor', 'package_name', 'package_version',
            'status',
            'date_added', 'date_eol',
            ]
    def get_success_url(self):
        return reverse_lazy('hwam:sw_detail', args=(self.object.id,))

class OUDeleteView(PermissionRequiredMixin, DeleteView):
    model = OrganizationalUnit
    permission_required = 'hwam.delete_organizationalunit'
    template_name = 'hwam/ou_delete.html'
    context_object_name = 'ou'
    def get_success_url(self):
        return reverse('hwam:ou_index')

class HWDeleteView(PermissionRequiredMixin, DeleteView):
    model = HardwareAsset
    permission_required = 'hwam.delete_hardwareasset'
    template_name = 'hwam/hw_delete.html'
    context_object_name = 'hw'
    def get_success_url(self):
        return reverse('hwam:hw_index')

class SWDeleteView(PermissionRequiredMixin, DeleteView):
    model = SoftwareAsset
    permission_required = 'hwam.delete_softwareasset'
    template_name = 'hwam/sw_delete.html'
    context_object_name = 'sw'
    def get_success_url(self):
        return reverse('hwam:sw_index')
