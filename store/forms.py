
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from ckeditor.widgets import CKEditorWidget
from store.models import Customer, Comments, Offer, Support, Seller, Product




class CreateUserForm(UserCreationForm):
    class Meta:
        model = User 
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class ProductForm(forms.ModelForm):
    description = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Product
        fields = ['name','price','category','sub_category', 'description','quantity','digital' , 'available','file' , 'image',]

class UpdateCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = [ 'user']


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


class SellerForm(forms.ModelForm):
    class Meta:
        model = Seller
        fields = ['bio','brand_name', 'location', 'phone', 'payment_method', 'payment_details', 'website']
