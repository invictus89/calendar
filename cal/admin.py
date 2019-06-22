from django.contrib import admin
from .models import Event

# Register your models here.
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'uploaded_at', 'created_at', 'updated_at',)
admin.site.register(Event, EventAdmin)

