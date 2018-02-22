from django.contrib import admin

# Register your models here.
from .models import LimitRule, LogEventParser, ParseHelper

admin.site.register(LimitRule)
admin.site.register(LogEventParser)
admin.site.register(ParseHelper)

