from django.contrib import admin

# Register your models here.
from .models import LogEvent, RuleEvent, LimitRule
from .models import LogEventParser, ParseHelper

admin.site.register(LogEvent)
admin.site.register(RuleEvent)
admin.site.register(LimitRule)
admin.site.register(LogEventParser)
admin.site.register(ParseHelper)

