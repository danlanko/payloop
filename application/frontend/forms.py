from django import forms
from ..backend.models import ClientProfile, DemoList
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import TextInput


#  Login form inheriting from Django Authentication Form
class LoginForm(AuthenticationForm):
    username = forms.CharField(required=True, widget=TextInput(attrs={'class': 'form-control',
                                                                      'type': 'text', 'id': 'username',
                                                                      'placeholder': 'Enter Username'}))
    password = forms.CharField(required=True, widget=TextInput(attrs={'class': 'form-control',
                                                                      'type': 'password', 'id': 'password',
                                                                      'placeholder': 'Enter Password'}))


class RegisterProductForm(forms.ModelForm):

    class Meta:

        model = ClientProfile
        exclude = ['user', 'package', 'expiry_date', 'reg_date', 'last_pay_date', 'next_pay_date', 'modules']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
        self.fields['phone'].widget.attrs.update({'type': 'number'})


class DemoForm(forms.ModelForm):

    class Meta:
        model = DemoList
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
            })
