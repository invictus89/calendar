from django import forms
from django.forms import DateInput
from .models import Event


class EventForm(forms.ModelForm):
  title = forms.CharField(
      label='제목',
      widget=forms.TextInput(attrs={
          'placeholder': 'Enter the title',
      })
  )
  description = forms.CharField(
      label='내용',
      widget=forms.Textarea(attrs={
          'placeholder': 'Ender the description',
          'rows': 5,
          'cols': 50,
      })
  )

  class Meta:
    model = Event
    # fields = '__all__'
    fields = ('title', 'description',)
