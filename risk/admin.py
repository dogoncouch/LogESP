from django.contrib import admin

# Register your models here.
from .models import ThreatSrcCategory, ThreatSrcType
from .models import AdvThreatSource, NonAdvThreatSource
from .models import ThreatEventType
from .models import AdvThreatEvent, NonAdvThreatEvent
from .models import ConditionClass, ConditionCategory, ConditionType
from .models import Vulnerability, RiskCondition
from .models import ImpactType, Impact

#class AdvThreatEventAdmin(admin.ModelAdmin):
#    list_display = ['name', 'desc']
#    fields = ['name', 'desc']

#class NonAdvThreatEventAdmin(admin.ModelAdmin):
#    list_display = ['name', 'desc']
#    fields = ['name', 'desc']

admin.site.register(AdvThreatEvent)
admin.site.register(NonAdvThreatEvent)
admin.site.register(ThreatSrcCategory)
admin.site.register(ThreatSrcType)
admin.site.register(AdvThreatSource)
admin.site.register(NonAdvThreatSource)
admin.site.register(ThreatEventType)
admin.site.register(ConditionClass)
admin.site.register(ConditionCategory)
admin.site.register(ConditionType)
admin.site.register(Vulnerability)
admin.site.register(RiskCondition)
admin.site.register(ImpactType)
admin.site.register(Impact)

