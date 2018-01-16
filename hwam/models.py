from django.db import models

# Create your models here.

class OrganizationalUnit(models.Model):
    unit_name = models.CharField(max_length=30)
    unit_desc = models.CharField(max_length=200, null=True, blank=True)
    unit_contact = models.CharField(max_length=30, null=True, blank=True)
    def __str__(self):
        return self.unit_name
    
class HardwareAsset(models.Model):
    asset_name = models.CharField(max_length=30)
    asset_desc = models.CharField(max_length=200, null=True, blank=True)
    org_unit = models.ForeignKey(OrganizationalUnit,
            null=True, blank=True, on_delete=models.SET_NULL)
    asset_owner = models.CharField(max_length=30, null=True, blank=True)
    asset_custodian = models.CharField(max_length=30, null=True, blank=True)
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
            blank=True, symmetrical=False)
            #through='HWAssetNesting', through_fields=('child', 'parent'))
    parent_software = models.ManyToManyField('self',
            blank=True, symmetrical=False)
            #through='SWAssetNesting', through_fields=('child', 'parent'))
    asset_name = models.CharField(max_length=30)
    asset_desc = models.CharField(max_length=200, null=True, blank=True)
    org_unit = models.ForeignKey(OrganizationalUnit,
            null=True, blank=True, on_delete=models.SET_NULL)
    custodian_swam = models.CharField(max_length=30, null=True, blank=True)
    custodian_csm = models.CharField(max_length=30, null=True, blank=True)
    custodian_vul = models.CharField(max_length=30, null=True, blank=True)
    software_type = models.CharField(max_length=20, null=True, blank=True)
    sw_property_id = models.CharField(max_length=30, null=True, blank=True)
    status = models.CharField(max_length=20, null=True, blank=True)
    date_added = models.DateField('date added', null=True, blank=True)
    date_eol = models.DateField('end of life', null=True, blank=True)
    def __str__(self):
        return self.asset_name

#class HWAssetNesting(models.Model):
#    parent = models.ForeignKey(HardwareAsset, on_delete=models.CASCADE)
#    child = models.ForeignKey(SoftwareAsset, on_delete=models.CASCADE)

#class SWAssetNesting(models.Model):
#    parent = models.ForeignKey(SoftwareAsset, on_delete=models.CASCADE)
#    child = models.ForeignKey(SoftwareAsset, on_delete=models.CASCADE,
#            related_name='child_asset')

