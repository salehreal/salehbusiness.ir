from django import forms
from .models import ContactUsModel

# class ContactUsForm(forms.Form):
#     username = forms.CharField(label='', widget=forms.TextInput(attrs={
#         'name': "contact-name", 'id': "contact-name",
#     }))
#     email = forms.EmailField(label='', widget=forms.EmailInput(attrs={
#         'name': "contact-email", 'id': "contact-email",
#     }))
#     phone = forms.CharField(label='', widget=forms.TextInput(attrs={
#         'name': "contact-phone", 'id': "contact-phone",
#     }))
#     message = forms.CharField(label='', widget=forms.Textarea(attrs={
#         'name': "contact-message", 'id': "contact-message", 'cols': "1", 'rows': "2",
#     }))

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUsModel
        fields = "__all__"
        widgets = {
            'username': forms.TextInput(attrs={'name': "contact-name", 'id': "contact-name"}),
            'email': forms.EmailInput(attrs={'name': "contact-email", 'id': "contact-email"}),
            'phone': forms.TextInput(attrs={'name': "contact-phone", 'id': "contact-phone"}),
            'message': forms.Textarea(attrs={'name': "contact-message", 'id': "contact-message"}),
        }
        error_messages = {
            'username': {
                'required': "همه مقادیر را پر کنید",
            }
        }

class AvatarForm(forms.Form):
    img = forms.ImageField()