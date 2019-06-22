from django.db import models
from django.urls import reverse

class Event(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    title_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('-pk',)

    @property
    def get_html_url(self):
        url = reverse('calendar:edit', args=(self.id,))
        bg_color = ''
        if self.title_type == '기념일':
            bg_color = 'bg-primary'
        elif self.title_type == '뉴스':
            bg_color = 'bg-secondary'
        elif self.title_type == '사건 및 사고':
            bg_color = 'bg-danger'
        elif self.title_type == '역사':
            bg_color = 'bg-success'

        return f'<a href="{url}" class="my-day text-white font-weight-bolder {bg_color}"> {self.title} </a>'