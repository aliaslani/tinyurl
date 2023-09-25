from django.forms import ModelForm
from .models import URL
import django.forms as forms
from hashlib import md5


class URLForm(ModelForm):
    class Meta:
        model = URL
        fields = ['origin']
            
        def clean_origin(self):
            origin = self.cleaned_data['origin']
            if not origin.startswith('http://') and not origin.startswith('https://'):
                origin = 'http://' + origin
            return origin

        