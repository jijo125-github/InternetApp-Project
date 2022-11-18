from django import forms
from django.contrib.auth.forms import UserCreationForm
from myapp.models import Order, Client


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('client', 'product', 'num_units')

        widgets = {
            'client': forms.RadioSelect(),
        }

        labels = {
            'num_units': 'Quantity',
            'client': 'Client Name',
        }


class InterestForm(forms.Form):
    # interested = forms.CharField(widget=forms.RadioSelect)
    interested = forms.ChoiceField(choices=[(1, 'Yes'), (0, 'No')], widget=forms.RadioSelect)
    quantity = forms.IntegerField(min_value=1)
    comments = forms.CharField(required=False, widget=forms.Textarea, label='Additional Comments')


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    username = forms.CharField(max_length=100, required=True)
    password1 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput())
    email = forms.EmailField(required=True)

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')
