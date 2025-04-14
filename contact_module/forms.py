from django import forms
from .models import ContactUsModel

class ContactUsForm(forms.ModelForm):
    class Meta:
        model = ContactUsModel
        fields = "__all__"
        widgets = {
            'username': forms.TextInput(attrs={'name': "contact-name", 'id': "contact-name"}),
            # 'email': forms.EmailInput(attrs={'name': "contact-email", 'id': "contact-email"}),
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