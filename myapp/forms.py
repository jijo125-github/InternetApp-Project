from django import forms
from myapp.models import Order


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
