from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class OrganizationalUnit(models.Model):
    unit_name = models.CharField(max_length=30)
    unit_desc = models.CharField(max_length=200, null=True, blank=True)
    unit_contact = models.ForeignKey(User,
            on_delete=models.PROTECT)
    # To Do: Add permissions (read/create/edit/delete ou assets)
    def __str__(self):
        return self.unit_name
    
class HardwareAsset(models.Model):
    asset_name = models.CharField(max_length=30)
    asset_desc = models.CharField(max_length=200, null=True, blank=True)
    org_unit = models.ForeignKey(OrganizationalUnit,
            related_name='hardware_assets',
            on_delete=models.PROTECT)
    # To Do: Add clearance level
    asset_owner = models.ForeignKey(User,
            related_name='hardware_assets_owned',
            null=True, blank=True, on_delete=models.SET_NULL)
    asset_custodian = models.ForeignKey(User,
            related_name='hardware_assets_cust',
            null=True, blank=True, on_delete=models.SET_NULL)
    device_type = models.CharField(max_length=20, null=True, blank=True)
    property_id = models.CharField(max_length=30, null=True, blank=True)
    location = models.CharField(max_length=40, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    date_added = models.DateField('date added', null=True, blank=True)
    date_eol = models.DateField('end of life', null=True, blank=True)
    def __str__(self):
        return self.asset_name

class SoftwareAsset(models.Model):
    parent_hardware = models.ManyToManyField(HardwareAsset,
            related_name='child_software', blank=True)
    parent_software = models.ManyToManyField('self',
            related_name='child_software', blank=True,
            symmetrical=False)
    asset_name = models.CharField(max_length=30)
    asset_desc = models.CharField(max_length=200, null=True, blank=True)
    org_unit = models.ForeignKey(OrganizationalUnit,
            related_name='software_assets',
            on_delete=models.PROTECT)
    # To Do: Add clearance level
    custodian_swam = models.ForeignKey(User,
            related_name='systems_swam',
            null=True, blank=True, on_delete=models.SET_NULL)
    custodian_csm = models.ForeignKey(User,
            related_name='systems_csm',
            null=True, blank=True, on_delete=models.SET_NULL)
    custodian_vul = models.ForeignKey(User,
            related_name='systems_vul',
            null=True, blank=True, on_delete=models.SET_NULL)
    software_type = models.CharField(max_length=20, null=True, blank=True)
    sw_property_id = models.CharField(max_length=30, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    date_added = models.DateField('date added', null=True, blank=True)
    date_eol = models.DateField('end of life', null=True, blank=True)
    def __str__(self):
        return self.asset_name
