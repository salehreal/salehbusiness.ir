from django.db import models

# Create your models here.


class ContactUsModel(models.Model):
    username = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    message = models.TextField()

    def __str__(self):
        return self.phone

    class Meta:
        verbose_name = 'پیام'
        verbose_name_plural = 'پیام ها'

class UploadAvatarModel(models.Model):
    avatar = models.ImageField(upload_to="avatar/")