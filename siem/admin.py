from django.contrib import admin

# Register your models here.
from .models import LogEvent, RuleEvent
from .models import LimitRule, ParseHelper

admin.site.register(LogEvent)
admin.site.register(RuleEvent)
admin.site.register(LimitRule)
admin.site.register(ParseHelper)

