from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from hwam.choices import *

# Create your models here.

class OrganizationalUnit(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    unit_contact = models.ForeignKey(User,
            on_delete=models.PROTECT)
    parent_ou = models.ForeignKey('self',
            related_name='child_ous',
            null=True, blank=True, on_delete=models.CASCADE)
            #symmetrical=False)
    # To Do: Add permissions (read/create/edit/delete ou assets)
    def __str__(self):
        return self.absolute_name()
    def absolute_name(self):
        if self.parent_ou:
            return '/'.join((self.parent_ou.absolute_name(), self.name))
        else:
            return self.name
    absolute_name.admin_order_field = 'name'
    def children(self):
        return OrganizationalUnit.objects.filter(
                parent_ou=self.pk).order_by('name')
    def serializable_object(self):
        obj = {'name': self.name, 'children': []}
        for child in self.children():
            obj['children'].append(child.serializable_object())
        return obj

class HardwareClass(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.name

class HardwareCategory(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return '/'.join((self.hardware_class.name, self.name))
    hardware_class = models.ForeignKey(HardwareClass,
            related_name='hardware_categories',
            on_delete=models.PROTECT)

class HardwareType(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        val = (self.hardware_category.hardware_class.name,
                self.hardware_category.name, self.name)
        return '/'.join(val)
    hardware_category = models.ForeignKey(HardwareCategory,
            related_name='hardware_types',
            on_delete=models.PROTECT)

class HardwareAsset(models.Model):
    parent_hardware = models.ForeignKey('self',
            related_name='child_hardware',
            null=True, blank=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
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
    hardware_type = models.ForeignKey(HardwareType,
            related_name='assets',
            null=True, blank=True, on_delete=models.SET_NULL)
    device_maker = models.CharField(max_length=20, null=True, blank=True)
    device_model = models.CharField(max_length=20, null=True, blank=True)
    property_id = models.CharField(max_length=30, null=True, blank=True)
    location = models.CharField(max_length=40, null=True, blank=True)
    status = models.IntegerField(choices=status_choices, default=6)
    date_added = models.DateField('date added', default=timezone.now,
            null=True, blank=True)
    date_eol = models.DateField('end of life', null=True, blank=True)
    def __str__(self):
        return self.name
    def is_active(self):
        return self.status == 1
    is_active.admin_order_field = 'status'
    is_active.boolean = True
    is_active.short_description = 'Active?'

class SoftwareCategory(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.name

class SoftwareType(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return '/'.join((self.software_category.name, self.name))
    software_category = models.ForeignKey(SoftwareCategory,
            related_name='software_types',
            on_delete=models.PROTECT)

class SoftwareAsset(models.Model):
    parent_hardware = models.ManyToManyField(HardwareAsset,
            related_name='child_software', blank=True)
    parent_software = models.ManyToManyField('self',
            related_name='child_software', blank=True,
            symmetrical=False)
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
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
    software_type = models.ForeignKey(SoftwareType,
            related_name='assets',
            null=True, blank=True, on_delete=models.SET_NULL)
    hostname = models.CharField(max_length=48, null=True, blank=True)
    domain_name = models.CharField(max_length=48, null=True, blank=True)
    ip4_address_1 = models.CharField(max_length=20, null=True, blank=True)
    ip4_address_2 = models.CharField(max_length=20, null=True, blank=True)
    ip4_address_3 = models.CharField(max_length=20, null=True, blank=True)
    ip4_address_4 = models.CharField(max_length=20, null=True, blank=True)
    ip4_address_5 = models.CharField(max_length=20, null=True, blank=True)
    ip4_address_6 = models.CharField(max_length=20, null=True, blank=True)
    ip4_address_7 = models.CharField(max_length=20, null=True, blank=True)
    ip4_address_8 = models.CharField(max_length=20, null=True, blank=True)
    ip6_address_1 = models.CharField(max_length=42, null=True, blank=True)
    ip6_address_2 = models.CharField(max_length=42, null=True, blank=True)
    ip6_address_3 = models.CharField(max_length=42, null=True, blank=True)
    ip6_address_4 = models.CharField(max_length=42, null=True, blank=True)
    ip6_address_5 = models.CharField(max_length=42, null=True, blank=True)
    ip6_address_6 = models.CharField(max_length=42, null=True, blank=True)
    ip6_address_7 = models.CharField(max_length=42, null=True, blank=True)
    ip6_address_8 = models.CharField(max_length=42, null=True, blank=True)
    package_vendor = models.CharField(max_length=32, null=True, blank=True)
    package_name = models.CharField(max_length=32, null=True, blank=True)
    package_version = models.CharField(max_length=20, null=True, blank=True)
    sw_property_id = models.CharField(max_length=30, null=True, blank=True)
    status = models.IntegerField(choices=status_choices, default=6)
    date_added = models.DateField('date added', default=timezone.now,
            null=True, blank=True)
    date_eol = models.DateField('end of life', null=True, blank=True)
    def __str__(self):
        return self.name
    def is_active(self):
        return self.status == 1
    is_active.admin_order_field = 'status'
    is_active.boolean = True
    is_active.short_description = 'Active?'
