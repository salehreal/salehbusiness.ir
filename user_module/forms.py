from django import forms


class RegisterForm(forms.Form):
    pass


class LoginForm(forms.Form):
    pass


class ActiveForm(forms.Form):
    num1 = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'number', 'name': 'num1', 'min': '0', 'max': '9', 'required': 'required'
    }))
    num2 = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'number', 'name': 'num2', 'min': '0', 'max': '9', 'required': 'required'
    }))
    num3 = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'number', 'name': 'num3', 'min': '0', 'max': '9', 'required': 'required'
    }))
    num4 = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'number', 'name': 'num4', 'min': '0', 'max': '9', 'required': 'required'
    }))
    num5 = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'number', 'name': 'num5', 'min': '0', 'max': '9', 'required': 'required'
    }))
    num6 = forms.CharField(widget=forms.TextInput(attrs={
        'type': 'number', 'name': 'num6', 'min': '0', 'max': '9', 'required': 'required'
    }))
