from django.db import models

# Create your models here.

class OrganizationalUnit(models.Model):
    unit_name = models.CharField(max_length=30)
    unit_desc = models.CharField(max_length=200)
    asset_contact = models.CharField(max_length=30)

class HardwareAsset(models.Model):
    asset_owner = models.CharField(max_length=30)
    asset_custodian = models.CharField(max_length=30)
    asset_name = models.CharField(max_length=30)
    asset_desc = models.CharField(max_length=200)
    device_type = models.CharField(max_length=20)
    property_id = models.CharField(max_length=30)
    location = models.CharField(max_length=40)
    status = models.CharField(max_length=20)
    date_added = models.DateTimeField('date added')
    date_eol = models.DateTimeField('end of life')
    org_unit = models.ForeignKey(OrganizationalUnit,
            null=True, on_delete=models.SET_NULL)

class SystemAsset(models.Model):
    parent_hardware = models.ManyToManyField(HardwareAsset)
    parent_systems = models.ManyToManyField('self')
    asset_owner = models.CharField(max_length=30)
    custodian_swam = models.CharField(max_length=30)
    custodian_csm = models.CharField(max_length=30)
    custodian_vul = models.CharField(max_length=30)
    asset_name = models.CharField(max_length=30)
    asset_desc = models.CharField(max_length=200)
    system_type = models.CharField(max_length=20)
    date_added = models.DateTimeField('date added')
    date_eol = models.DateTimeField('end of life')
    org_unit = models.ForeignKey(OrganizationalUnit,
            null=True, on_delete=models.SET_NULL)

