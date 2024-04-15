from django import forms
from .models import Product
from django.contrib.auth.models import User


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'category','manufacture','quantity', 'image']



from django import forms
from django.contrib.auth.models import User
from .models import UserProfileInfo

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserProfileInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfileInfo
        fields = ('email',)

# forms.py
from django import forms
from .models import Product, CartItem

class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    shipping_address = forms.CharField(max_length=250)
    contact_info = forms.CharField(max_length=20)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(CheckoutForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        # You can add any custom validation logic here.
        return cleaned_data
    
    