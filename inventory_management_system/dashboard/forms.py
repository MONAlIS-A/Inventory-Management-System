from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, SetPasswordForm
from . models import Profile, Product, Order
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation

class CreateUserForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields =['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields =['address', 'phone', 'image']

class ProductForm(forms.ModelForm):
    class Meta:
        model =Product
        fields = ['name', 'category', 'quantity']

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['product', 'order_quantity']

#password reset 
class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label=_("Email"), max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class':'form-control'}))

#set password form
class MySetPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(label=_('New password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}), help_text=password_validation.password_validators_help_text_html())
    
    new_password2 = forms.CharField(label=_('Confirm new password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class':'form-control'}))
