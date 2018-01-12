from django.db import models

# Create your models here.

class HardwareAsset(models.Model):
    asset_owner = models.CharField(max_length=30)
    asset_custodian = models.CharField(max_length=30)
    asset_name = models.CharField(max_length=30)
    asset_desc = models.CharField(max_length=200)
    date_added = models.DateTimeField('date added')

class SystemAsset(models.Model):
    asset_owner = models.CharField(max_length=30)
    asset_custodian = models.CharField(max_length=30)
    asset_name = models.CharField(max_length=30)
    asset_desc = models.CharField(max_length=200)
    date_added = models.DateTimeField('date added')

