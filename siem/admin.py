from django.contrib import admin

# Register your models here.
from .models import DefaultEvent, AuthEvent, RuleEvent
from .models import LimitRule, ParseHelper

admin.site.register(DefaultEvent)
admin.site.register(AuthEvent)
admin.site.register(RuleEvent)
admin.site.register(LimitRule)
admin.site.register(ParseHelper)

