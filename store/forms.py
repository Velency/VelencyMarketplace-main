
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User

from store.models import Customer, Comments, Offer, Support, Withdraw
from django.core.validators import EmailValidator


class CreateUserForm(UserCreationForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter a password with 8 or more characters and at least 1 digit'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UpdateImageForm(forms.Form):
    image = forms.ImageField(required=False)


class UpdateCustomerForm(forms.ModelForm):
    referrer_code = forms.CharField(max_length=5, required=False)
    # zipcode = forms.IntegerField( required=False)
    # country = forms.CharField(max_length=60, required=False)
    # mobile = forms.IntegerField(required=False)

    class Meta:
        model = Customer

        fields = ['first_name', 'last_name', 'country', 'zipcode',
                  'email', 'mobile', 'referrer_code', 'wallet']


class WalletForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['wallet']


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['image']


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
        fields = ['subject', 'email', 'comment']


class WithdrawForm(forms.ModelForm):
    class Meta:
        model = Withdraw
        fields = ['amount']


class FeedbackForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(
        attrs={'placeholder': 'Введите количество токенов которые хотели бы приобрести, и как мы сможем с вами связаться помимо почты'}), )


class ConnectionForm(forms.Form):
    name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15)
    email = forms.EmailField()
    questions = forms.CharField(widget=forms.Textarea)
    agree_to_processing = forms.BooleanField(
        required=True,
        label='Я согласен на обработку данных',
        widget=forms.CheckboxInput(attrs={'class': 'checkbox-styled'})
    )
