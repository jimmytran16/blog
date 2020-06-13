from django import forms

from .models import Post

class PostUploadForm(forms.ModelForm):
    def __init__(self, *args, **kwargs): #override the constructor , and set the fields description strip() to be false
        super(PostUploadForm, self).__init__(*args, **kwargs)
        self.fields['description'].strip = False

    class Meta:
        model = Post
        fields = [
            'subject','description','img'
        ]

