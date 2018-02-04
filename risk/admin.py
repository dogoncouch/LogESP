from django.contrib import admin

# Register your models here.
from .models import AdvThreatSrcCategory, AdvThreatSrcType
from .models import AdvThreatSource
from .models import NonAdvThreatSrcClass, NonAdvThreatSrcCategory
from .models import NonAdvThreatSrcType, NonAdvThreatSource
from .models import AdvThreatEventCategory, AdvThreatEventType
from .models import NonAdvThreatEventType
from .models import AdvThreatEvent, NonAdvThreatEvent
from .models import VulnerabilityClass, VulnerabilityCategory, VulnerabilityType
from .models import ConditionClass, ConditionCategory, ConditionType
from .models import Vulnerability, RiskCondition
from .models import ImpactType, Impact
from .models import RiskResponseType, RiskResponse


admin.site.register(AdvThreatEventCategory)
admin.site.register(AdvThreatEventType)
admin.site.register(AdvThreatEvent)
admin.site.register(NonAdvThreatEventType)
admin.site.register(NonAdvThreatEvent)
admin.site.register(AdvThreatSrcCategory)
admin.site.register(AdvThreatSrcType)
admin.site.register(AdvThreatSource)
admin.site.register(NonAdvThreatSrcClass)
admin.site.register(NonAdvThreatSrcCategory)
admin.site.register(NonAdvThreatSrcType)
admin.site.register(NonAdvThreatSource)
admin.site.register(VulnerabilityClass)
admin.site.register(VulnerabilityCategory)
admin.site.register(VulnerabilityType)
admin.site.register(ConditionClass)
admin.site.register(ConditionCategory)
admin.site.register(ConditionType)
admin.site.register(Vulnerability)
admin.site.register(RiskCondition)
admin.site.register(ImpactType)
admin.site.register(Impact)
admin.site.register(RiskResponseType)
admin.site.register(RiskResponse)
