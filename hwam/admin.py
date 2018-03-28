from django.contrib import admin

# Register your models here.
from .models import HardwareClass, HardwareCategory, HardwareType
from .models import SoftwareCategory, SoftwareType
from .models import OrganizationalUnit, HardwareAsset, SoftwareAsset

class OrganizationalUnitAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent_ou', 'unit_contact']
    fields = ['name', 'desc', 'unit_contact', 'parent_ou']

class HardwareClassAdmin(admin.ModelAdmin):
    list_display = ['name', 'desc']
    fields = ['name', 'desc']

class HardwareCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'hardware_class']
    fields = ['name', 'desc', 'hardware_class']

class HardwareTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'hardware_category']
    fields = ['name', 'desc', 'hardware_category']

class HardwareAssetAdmin(admin.ModelAdmin):
    list_display = ['name', 'org_unit', 'location',
            'hardware_type', 'is_active']
    fieldsets = [
            (None, {'fields': ['name', 'desc', 'org_unit']}),
            ('Contacts', {'fields': ['asset_owner', 'asset_custodian']}),
            ('Parent Hardware', {'fields': ['parent_hardware']}),
            ('Device Information', {'fields': [
                'hardware_type', 'property_id',
                'device_maker', 'device_model']}),
            ('Status Information', {'fields': ['location', 'status']}),
            ('Life Cycle', {'fields': ['date_added', 'date_eol']}),
            ]
    list_filter = ['name', 'org_unit', 'hardware_type', 'date_added',
            'status', 'asset_owner', 'asset_custodian']

class SoftwareCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'desc']
    fields = ['name', 'desc']

class SoftwareTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'software_category']
    fields = ['name', 'desc', 'software_category']

class SoftwareAssetAdmin(admin.ModelAdmin):
    list_display = ['name', 'org_unit', 'software_type', 'is_active']
    fieldsets = [
            (None, {'fields': ['name', 'desc', 'org_unit']}),
            ('Contacts', {'fields': [
                'custodian_swam', 'custodian_csm', 'custodian_vul']}),
            ('Parent Systems', {'fields': ['parent_hardware', 'parent_software']}),
            ('Device Information', {'fields': [
                'software_type', 'sw_property_id',
                'hostname', 'domain_name',
                'ip4_address_1', 'ip4_address_2',
                'ip4_address_3', 'ip4_address_4',
                'ip6_address_1', 'ip6_address_2',
                'ip6_address_3', 'ip6_address_4',
                'package_name', 'package_version']}),
            ('Status Information', {'fields': ['status']}),
            ('Life Cycle', {'fields': ['date_added', 'date_eol']}),
            ]
    list_filter = ['name', 'org_unit', 'software_type', 'date_added',
            'status', 'custodian_swam', 'custodian_csm', 'custodian_vul']

admin.site.register(OrganizationalUnit, OrganizationalUnitAdmin)
admin.site.register(HardwareClass, HardwareClassAdmin)
admin.site.register(HardwareCategory, HardwareCategoryAdmin)
admin.site.register(HardwareType, HardwareTypeAdmin)
admin.site.register(HardwareAsset, HardwareAssetAdmin)
admin.site.register(SoftwareCategory, SoftwareCategoryAdmin)
admin.site.register(SoftwareType, SoftwareTypeAdmin)
admin.site.register(SoftwareAsset, SoftwareAssetAdmin)
