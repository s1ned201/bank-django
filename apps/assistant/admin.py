from django.contrib import admin
from .models import ChatMessage

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'short_message', 'created_at')
    search_fields = ('user__username', 'message')

    def short_message(self, obj):
        return obj.message[:50]