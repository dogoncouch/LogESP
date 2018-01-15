from django.contrib import admin

# Register your models here.
from .models import OrganizationalUnit,HardwareAsset, SoftwareAsset

admin.site.register(OrganizationalUnit)
admin.site.register(HardwareAsset)
admin.site.register(SoftwareAsset)
