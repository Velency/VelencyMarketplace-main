
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from store.models import Customer, Comments, Offer, Support



class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'placeholder': 'Enter a password with 8 or more characters and at least 1 digit'}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



class UpdateCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name','last_name', 'email', 'mobile', 'image', 'country', 'state', 'city', 'address', 'referrer_code']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'country': forms.TextInput(attrs={'class': 'form-control'}),
            'state': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'zipcode': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['subject', 'comment', 'rate']
       
class CustomerOfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = ['subject', 'email', 'comment']


class SupportForm(forms.ModelForm):
    class Meta:
        model = Support
        fields = [ 'subject', 'email', 'comment']

class FeedbackForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)


class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'email', 'image', 'mobile', 'address', 'country', 'city', 'state', 'zipcode', 'referral_code']

