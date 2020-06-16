from django import forms
from .models import User

class ProfilePicForm(forms.ModelForm):
    def __init__(self, *args, **kwargs): #override the constructor , and set the fields description strip() to be false
        super(ProfilePicForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = [
            'profile'
        ]
        labels = {
            'profile':'Profile Pic',
        }
