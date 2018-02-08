from django.db import models
from django.core.exceptions import ValidationError

from risk.choices import *

# Create your models here.

def validate_scale_range(value):
    if not 0 < value <= 100:
        raise ValidationError('%s not in 1-100 range' % value)

class VulnerabilityClass(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.name

class VulnerabilityCategory(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    vuln_class = models.ForeignKey(VulnerabilityClass,
            related_name = 'vuln_categories',
            on_delete=models.CASCADE)
    def __str__(self):
        return '/'.join((self.vuln_class.name, self.name))

class VulnerabilityType(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    vuln_category = models.ForeignKey(VulnerabilityCategory,
            related_name = 'vuln_types',
            on_delete=models.CASCADE)
    def __str__(self):
        val = (self.vuln_category.vuln_class.name,
                self.vuln_category.name, self.name)
        return '/'.join(val)

class Vulnerability(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    vuln_type = models.ForeignKey(VulnerabilityType,
            related_name='vulnerabilities',
            null=True, blank=True, on_delete = models.SET_NULL)
    severity = models.IntegerField(validators=[validate_scale_range])
    info_source = models.CharField(max_length=50, null=True, blank=True)
    tier = models.IntegerField(choices=tier_choices, default=3)
    def __str__(self):
        return self.name
    #def __str__(self):
    #    val = (self.vuln_type.vuln_category.vuln_class.name,
    #            self.vuln_type.vuln_category.name,
    #            self.vuln_type.name, self.name)
    #    return '/'.join(val)

class ConditionClass(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.name

class ConditionCategory(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    condition_class = models.ForeignKey(ConditionClass,
            related_name = 'condition_categories',
            on_delete=models.CASCADE)
    def __str__(self):
        return '/'.join((self.condition_class.name, self.name))

class ConditionType(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    condition_category = models.ForeignKey(ConditionCategory,
            related_name = 'condition_types',
            on_delete=models.CASCADE)
    def __str__(self):
        val = (self.condition_category.condition_class.name,
                self.condition_category.name, self.name)
        return '/'.join(val)

class RiskCondition(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    condition_type = models.ForeignKey(ConditionType,
            related_name='risk_conditions',
            null=True, blank=True, on_delete = models.SET_NULL)
    pervasiveness = models.IntegerField(validators=[validate_scale_range])
    info_source = models.CharField(max_length=50, null=True, blank=True)
    tier = models.IntegerField(choices=tier_choices, default=3)
    def __str__(self):
        return self.name
    #def __str__(self):
    #    val = (self.condition_type.condition_category.condition_class.name,
    #            self.condition_type.condition_category.name,
    #            self.condition_type.name, self.name)
    #    return '/'.join(val)

class ImpactType(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.name

class Impact(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    impact_type = models.ForeignKey(ImpactType,
            related_name='impacts',
            null=True, blank=True, on_delete=models.SET_NULL)
    info_source = models.CharField(max_length=50, null=True, blank=True)
    tier = models.IntegerField(choices=tier_choices, default=3)
    severity = models.IntegerField(validators=[validate_scale_range])
    impact_tier = models.IntegerField(choices=tier_choices, default=3)
    def __str__(self):
        return self.name
    #def __str__(self):
    #    return '/'.join(self.impact_type.name, self.name)

class RiskResponseType(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.name

class RiskResponse(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    response_type = models.ForeignKey(RiskResponseType,
            on_delete=models.PROTECT)
    effectiveness = models.IntegerField(validators=[validate_scale_range])
    status = models.IntegerField(choices=status_choices, default=4)
    def __str__(self):
        return '/'.join((self.response_type.name, self.name))

class AdvThreatSrcCategory(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.name

class AdvThreatSrcType(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    source_category = models.ForeignKey(AdvThreatSrcCategory,
            related_name='source_types',
            on_delete=models.CASCADE)
    def __str__(self):
        return '/'.join((self.source_category.name, self.name))

class AdvThreatSource(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    source_type = models.ForeignKey(AdvThreatSrcType,
            related_name='adv_sources', on_delete = models.CASCADE)
    info_source = models.CharField(max_length=50, null=True, blank=True)
    tier = models.IntegerField(choices=tier_choices, default=3)
    in_scope = models.BooleanField(default=True)
    capability = models.IntegerField(validators=[validate_scale_range],
            null=True, blank=True)
    intent = models.IntegerField(validators=[validate_scale_range],
            null=True, blank=True)
    targeting = models.IntegerField(validators=[validate_scale_range],
            null=True, blank=True)
    def __str__(self):
        val = (self.source_type.source_category.name,
                self.source_type.name, self.name)
        return '/'.join(val)

class NonAdvThreatSrcClass(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.name

class NonAdvThreatSrcCategory(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    source_class = models.ForeignKey(NonAdvThreatSrcClass,
            related_name='source_categories',
            on_delete=models.CASCADE)
    def __str__(self):
        return '/'.join((self.source_class.name, self.name))

class NonAdvThreatSrcType(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    source_category = models.ForeignKey(NonAdvThreatSrcCategory,
            related_name='source_types',
            on_delete=models.CASCADE)
    def __str__(self):
        val = (self.source_category.source_class.name,
                self.source_category.name, self.name)
        return '/'.join(val)

class NonAdvThreatSource(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    source_type = models.ForeignKey(NonAdvThreatSrcType,
            related_name='nonadv_sources', on_delete = models.CASCADE)
    info_source = models.CharField(max_length=50, null=True, blank=True)
    tier = models.IntegerField(choices=tier_choices, default=3)
    in_scope = models.BooleanField(default=True)
    range_of_effect = models.IntegerField(
            validators=[validate_scale_range],
            null=True, blank=True)
    def __str__(self):
        val = (self.source_type.source_category.source_class.name,
                self.source_type.source_category.name,
                self.source_type.name, self.name)
        return '/'.join(val)

class AdvThreatEventCategory(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.name

class AdvThreatEventType(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    source_category = models.ForeignKey(AdvThreatEventCategory,
            related_name='event_types',
            on_delete=models.CASCADE)
    def __str__(self):
        return '/'.join((self.source_category.name, self.name))

class AdvThreatEvent(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    event_type = models.ForeignKey(AdvThreatEventType,
            related_name='adv_events', on_delete=models.CASCADE)
    sources = models.ManyToManyField(AdvThreatSource,
            related_name='threat_events', blank=True)
    relevance = models.IntegerField(choices=relevance_choices, default=1)
    info_source = models.CharField(max_length=50, null=True, blank=True)
    tier = models.IntegerField(choices=tier_choices, default=3)
    likelihood_initiation = models.IntegerField(
            validators=[validate_scale_range],
            null=True, blank=True)
    likelihood_impact = models.IntegerField(
            validators=[validate_scale_range],
            null=True, blank=True)
    vulnerabilities = models.ManyToManyField(Vulnerability,
            related_name='threat_events', blank=True)
    impacts = models.ManyToManyField(Impact,
            related_name='adv_threat_events', blank=True)
    responses = models.ManyToManyField(RiskResponse,
            related_name='adv_threat_events', blank=True)
    assigned_risk = models.IntegerField(
            validators=[validate_scale_range],
            null=True, blank=True)
    def __str__(self):
        val = (self.event_type.source_category.name,
                self.event_type.name, self.name)
        return '/'.join(val)
    def calc_likelihood(self):
        if self.likelihood_initiation and self.likelihood_impact:
            return (self.likelihood_initiation + \
                    self.likelihood_impact) // 2
        else:
            return None

class NonAdvThreatEventType(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    def __str__(self):
        return self.name

class NonAdvThreatEvent(models.Model):
    name = models.CharField(max_length=30)
    desc = models.CharField(max_length=200, null=True, blank=True)
    event_type = models.ForeignKey(NonAdvThreatEventType,
            related_name='nonadv_events', on_delete=models.CASCADE)
    sources = models.ManyToManyField(NonAdvThreatSource,
            related_name='threat_events', blank=True)
    relevance = models.IntegerField(choices=relevance_choices, default=1)
    info_source = models.CharField(max_length=50, null=True, blank=True)
    tier = models.IntegerField(choices=tier_choices, default=3)
    likelihood_initiation = models.IntegerField(
            validators=[validate_scale_range],
            null=True, blank=True)
    likelihood_impact = models.IntegerField(
            validators=[validate_scale_range],
            null=True, blank=True)
    risk_conditions = models.ManyToManyField(RiskCondition,
            related_name='threat_events', blank=True)
    impacts = models.ManyToManyField(Impact,
            related_name='nonadv_threat_events', blank=True)
    responses = models.ManyToManyField(RiskResponse,
            related_name='nonadv_threat_events', blank=True)
    assigned_risk = models.IntegerField(
            validators=[validate_scale_range],
            null=True, blank=True)
    def __str__(self):
        val = (self.event_type.name, self.name)
        return '/'.join(val)
    def calc_likelihood(self):
        if self.likelihood_initiation and self.likelihood_impact:
            return (self.likelihood_initiation + \
                    self.likelihood_impact) // 2
        else:
            return None
