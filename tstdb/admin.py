from django.contrib import admin
from tstdb.models import Config


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    pass
