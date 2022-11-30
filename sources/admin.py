from django.contrib import admin
from sources.models import Config


@admin.register(Config)
class ConfigAdmin(admin.ModelAdmin):
    pass
