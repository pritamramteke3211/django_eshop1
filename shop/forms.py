from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Address

class SignupForm(UserCreationForm):
    class  Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email']
        labels = {'email': 'Email'}
        widgets = {
            'username': forms.TextInput(),
            'first_name': forms.TextInput(),
            'last_name': forms.TextInput(),
            'email': forms.EmailInput(), 
            
        }


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address','phone_number','city','state','zip']
        widgets={
            'address':forms.Textarea(attrs={'class':'form-control',"rows":2, "cols":20}),
            'phone_number':forms.TextInput(attrs={'class':'form-control'}),
            'city':forms.TextInput(attrs={'class':'form-control'}),
            'state':forms.TextInput(attrs={'class':'form-control'}),
            'zip':forms.TextInput(attrs={'class':'form-control'}),
        }