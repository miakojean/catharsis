from django.contrib import admin
from .models import Project, Session, Event, ConversionGoal
# Register your models here.

admin.site.register(Project)
admin.site.register(Session)
admin.site.register(Event)
admin.site.register(ConversionGoal)
