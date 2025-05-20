from django.contrib import admin

from .models import Message, Room, Topic


class TopicAdmin(admin.ModelAdmin):
    list_display = ("name",)
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Room)
admin.site.register(Topic, TopicAdmin)
admin.site.register(Message)
