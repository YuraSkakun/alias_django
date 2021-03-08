from django.contrib import admin
from alias.models import Alias


@admin.register(Alias)
class AliasAdminModel(admin.ModelAdmin):
    fields = ('alias', 'target', 'start', 'end')
    list_display = ('id', 'alias', 'target', 'start', 'end')
    ordering = ['id']
