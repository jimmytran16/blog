from django import forms

from .models import Post

class PostUploadForm(forms.ModelForm): #forms to upload the profile picture
    def __init__(self, *args, **kwargs): #override the constructor , and set the fields description strip() to be false
        super(PostUploadForm, self).__init__(*args, **kwargs)
        self.fields['description'].strip = False

    class Meta:
        model = Post
        widgets = { #Attach the class attributes to the fields to be able to manually style it
            'subject': forms.TextInput(attrs={'class': 'subjectClass'}),
        }
        fields = [ #These are the fields from the models that you want to include in the forms
            'subject','description','img'
        ]
        labels = { #These are the labels that you want to change for the attribute when displayed 
            'img':'Image',
        }
