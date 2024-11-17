from django.forms import ModelForm
from .models import Room
from django.contrib.auth.models import User

class roomForm(ModelForm):
    class Meta:
        model = Room
        fields= '__all__'
        exclude=['Host', 'participants']

class UserForm(ModelForm):
    class Meta:
        model= User
        fields=['username','email']