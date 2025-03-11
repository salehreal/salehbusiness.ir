from django import forms

class DiscountCodeForm(forms.Form):
    code = forms.CharField(max_length=50, label='کد تخفیف')
