from django.contrib import admin

# Register your models here.
from .models import LogEvent, RuleEvent, LimitRule

admin.site.register(LogEvent)
admin.site.register(RuleEvent)
admin.site.register(LimitRule)

