from django.forms import fields
from .models import TodoModel
from django import forms
from django.contrib.auth import models

class TodoForm(forms.Form):
     todos = forms.CharField( max_length=100)

class UpdateForm(forms.ModelForm):
     class Meta:
          model = TodoModel
          fields = ['todos']
          widgets = {
               'todos':forms.TextInput(attrs={
                    'class':'form__field'
               })
          }
          

