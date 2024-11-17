from django.forms import ModelForm
from .models import task

class taskForm(ModelForm):
    class Meta:
        model= task
        fields=['title', 'completed']
