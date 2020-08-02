from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.forms.widgets import TextInput
from .models import Product, Packages, BannerText, Education


#  Login form inheriting from Django Authentication Form
class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, widget=TextInput(attrs={'class': 'form-control',
                                                                      'type': 'text', 'id': 'username',
                                                                      'placeholder': 'Enter Username'}))
    password = forms.CharField(required=True, widget=TextInput(attrs={'class': 'form-control',
                                                                      'type': 'password', 'id': 'password',
                                                                      'placeholder': 'Enter Password'}))


class NewProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })


class EducationForm(forms.ModelForm):

    class Meta:
        model = Education
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })


class PackageForm(forms.ModelForm):

    class Meta:
        model = Packages
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
        self.fields['des'].widget.attrs.update({'cols': '2', 'rows': '6'})


class BannerTextForm(forms.ModelForm):

    class Meta:
        model = BannerText
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
        self.fields['activate'].widget.attrs.update({'class': '',
                                                     'data-toggle': "switchery",
                                                     'data-color': "#2e7ce4"
                                                     })

    def clean(self):
        cleaned_data = super().clean()
        activate = self.cleaned_data['activate']
        if activate is True:
            for item in BannerText.objects.all():
                item.activate = False
                item.save()
        return cleaned_data

