from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from django import forms
from .models import ListModel,TaskModel

class UserForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['username', 'email', 'password1', 'password2']
class ListForm(forms.ModelForm):

    class Meta:
        model=ListModel
        fields=['name']

class TaskForm(forms.ModelForm):
    class Meta:
        model=TaskModel
        fields='__all__'

    def __init__(self, *args, user, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['list'].queryset = ListModel.objects.filter(user=user)