from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'action', 'ip_address', 'created_at', 'is_deleted')
    list_filter = ('action', 'is_deleted', 'created_at')
    search_fields = ('user__username', 'action', 'ip_address')
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy = 'created_at'