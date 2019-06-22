from django.db import models
from django.urls import reverse

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def get_html_url(self):
        url = reverse('calendar:event_edit', args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
