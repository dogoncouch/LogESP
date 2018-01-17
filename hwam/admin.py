from django.contrib import admin

# Register your models here.
from .models import OrganizationalUnit,HardwareAsset, SoftwareAsset

class OrganizationalUnitAdmin(admin.ModelAdmin):
    list_display = ['unit_name', 'parent_ou', 'unit_contact']
    fields = ['unit_name', 'unit_desc', 'unit_contact', 'parent_ou']

class HardwareAssetAdmin(admin.ModelAdmin):
    list_display = ['asset_name', 'org_unit', 'location',
            'device_type', 'is_active']
    fieldsets = [
            (None, {'fields': ['asset_name', 'asset_desc', 'org_unit']}),
            ('Contacts', {'fields': ['asset_owner', 'asset_custodian']}),
            ('Device Information', {'fields': ['device_type', 'property_id']}),
            ('Status Information', {'fields': ['location', 'status']}),
            ('Life Cycle', {'fields': ['date_added', 'date_eol']}),
            ]
    list_filter = ['asset_name', 'org_unit', 'device_type', 'date_added',
            'status', 'asset_owner', 'asset_custodian']

class SoftwareAssetAdmin(admin.ModelAdmin):
    list_display = ['asset_name', 'org_unit', 'software_type', 'is_active']
    fieldsets = [
            (None, {'fields': ['asset_name', 'asset_desc', 'org_unit']}),
            ('Contacts', {'fields': [
                'custodian_swam', 'custodian_csm', 'custodian_vul']}),
            ('Parent Systems', {'fields': ['parent_hardware', 'parent_software']}),
            ('Device Information', {'fields': [
                'software_type', 'sw_property_id',
                'package_name', 'package_version']}),
            ('Status Information', {'fields': ['status']}),
            ('Life Cycle', {'fields': ['date_added', 'date_eol']}),
            ]
    list_filter = ['asset_name', 'org_unit', 'software_type', 'date_added',
            'status', 'custodian_swam', 'custodian_csm', 'custodian_vul']

admin.site.register(OrganizationalUnit, OrganizationalUnitAdmin)
admin.site.register(HardwareAsset, HardwareAssetAdmin)
admin.site.register(SoftwareAsset, SoftwareAssetAdmin)
