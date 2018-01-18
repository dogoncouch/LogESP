from django.db import models
from django.core.exceptions import ValidationError

from risk.choices import *

# Create your models here.

def validate_scale_range(value):
    if not 0 <= value <= 100:
        raise ValidationError('%s not in 0-100 range' % value)

def validate_tier_range(value):
    if not 1 <= value <= 3:
        raise ValidationError('%s not in 1-3 range' % value)

class ThreatSrcCategory(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)

class ThreatSrcType(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    source_category = models.ForeignKey(ThreatSrcCategory,
            related_name='source_types',
            on_delete=models.CASCADE)

class AdvThreatSource(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    source_type = models.ForeignKey(ThreatSrcType,
            related_name='adv_sources',
            null=True, blank=True, on_delete = models.SET_NULL)
    info_source = models.CharField(max_length=50, null=True, blank=True)
    tier = models.IntegerField(validators=[validate_tier_range])
    in_scope = models.BooleanField(default=True)
    capability = models.IntegerField(validators=[validate_scale_range])
    intent = models.IntegerField(validators=[validate_scale_range])
    targeting = models.IntegerField(validators=[validate_scale_range])

class NonAdvThreatSource(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    source_type = models.ForeignKey(ThreatSrcType,
            related_name='nonadv_sources',
            null=True, blank=True, on_delete = models.SET_NULL)
    info_source = models.CharField(max_length=50, null=True, blank=True)
    tier = models.IntegerField(validators=[validate_tier_range])
    in_scope = models.BooleanField(default=True)
    range_of_effect = models.IntegerField(validators=[validate_scale_range])

class ThreatEventCategory(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)

class AdvThreatEvent(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(ThreatEventCategory,
            related_name='adv_events',
            null=True, blank=True, on_delete=models.SET_NULL)
    sources = models.ManyToManyField(AdvThreatSource,
            related_name='threat_events', blank=True)
    relevance = models.IntegerField(choices=relevance_choices, default=1)
    info_source = models.CharField(max_length=50, null=True, blank=True)
    tier = models.IntegerField(validators=[validate_tier_range])
    likelihood_initiation = models.IntegerField(validators=[validate_scale_range])
    likelihood_impact = models.IntegerField(validators=[validate_scale_range])

class NonAdvThreatEvent(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(ThreatEventCategory,
            related_name='nonadv_events',
            null=True, blank=True, on_delete=models.SET_NULL)
    sources = models.ManyToManyField(NonAdvThreatSource,
            related_name='threat_events', blank=True)
    relevance = models.IntegerField(choices=relevance_choices, default=1)
    info_source = models.CharField(max_length=50, null=True, blank=True)
    tier = models.IntegerField(validators=[validate_tier_range])
    likelihood_initiation = models.IntegerField(validators=[validate_scale_range])
    likelihood_impact = models.IntegerField(validators=[validate_scale_range])

class ConditionClass(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)

class ConditionCategory(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    condition_class = models.ForeignKey(ConditionClass,
            related_name = 'condition_categories',
            on_delete=models.CASCADE)

class ConditionType(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    condition_category = models.ForeignKey(ConditionCategory,
            related_name = 'condition_types',
            on_delete=models.CASCADE)

class Vulnerability(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    condition_type = models.ForeignKey(ConditionType,
            related_name='vulnerabilities',
            null=True, blank=True, on_delete = models.SET_NULL)
    severity = models.IntegerField(validators=[validate_scale_range])
    info_source = models.CharField(max_length=50, null=True, blank=True)
    tier = models.IntegerField(validators=[validate_tier_range])
    threat_events = models.ManyToManyField(AdvThreatEvent,
            related_name='vulnerabilities', blank=True)

class Condition(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    condition_type = models.ForeignKey(ConditionType,
            related_name='conditions',
            null=True, blank=True, on_delete = models.SET_NULL)
    pervasiveness = models.IntegerField(validators=[validate_scale_range])
    info_source = models.CharField(max_length=50, null=True, blank=True)
    tier = models.IntegerField(validators=[validate_tier_range])
    threat_events = models.ManyToManyField(NonAdvThreatEvent,
            related_name='conditions', blank=True)

class ImpactType(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)

class Impact(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    impact_type = models.ForeignKey(ImpactType,
            related_name='impacts',
            null=True, blank=True, on_delete=models.SET_NULL)
    info_source = models.CharField(max_length=50, null=True, blank=True)
    tier = models.IntegerField(validators=[validate_tier_range])
    severity = models.IntegerField(validators=[validate_scale_range])
    impact_tier = models.IntegerField(validators=[validate_tier_range])
    #ous_impacted = 
    #hw_impacted = 
    #sw_impacted = 
    adv_events = models.ForeignKey(AdvThreatEvent,
            related_name='impacts',
            null=True, blank=True, on_delete = models.SET_NULL)
    nonadv_events = models.ForeignKey(NonAdvThreatEvent,
            related_name='impacts',
            null=True, blank=True, on_delete = models.SET_NULL)
