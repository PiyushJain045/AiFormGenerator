from django.contrib import admin
from .models import UserFormTemplate, FormResponse


@admin.register(UserFormTemplate)
class UserFormTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'created_at', 'updated_at')
    search_fields = ('name', 'user__username')
    ordering = ('-created_at',)

admin.site.register(FormResponse)