from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from PIL import Image
# Create your models here.


class Profile(models.Model):
    theme_choices = (
        ("light_theme","Light Theme"),
        ("dark_theme","Dark Theme"),
    )
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")
    mobile = models.CharField(max_length=12,null=True,blank=True)
    image = models.ImageField(upload_to="profile",default="avatar.png",null=True,blank=True)
    theme = models.CharField(choices=theme_choices,max_length=15)
    bio = models.TextField(blank=True,null=True)
    birthday = models.DateTimeField(null=True,blank=True)
    state = models.CharField(max_length=100,null=True,blank=True)
    street_address = models.CharField(max_length=200,null=True,blank=True)
    website = models.CharField(max_length=200,null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} profile'

    @property
    def get_image_url(self):
        url = None
        try:
            url = self.image.url
        except:
            url = None
        return url

    @property
    def get_theme_setting(self):
        return self.theme

    def save(self,*arg,**kwargs):
        super().save()

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300,300)
            img.thumbnail(output_size)
            img.save(self.image.path)

class Social(models.Model):
    profile = models.OneToOneField(Profile,on_delete=models.CASCADE,related_name="social")
    facebook = models.CharField(max_length=100,null=True,blank=True)
    instagram = models.CharField(max_length=100,null=True,blank=True)
    twitter = models.CharField(max_length=100,null=True,blank=True)
    github = models.CharField(max_length=100,null=True,blank=True)
    linkedIn = models.CharField(max_length=100,null=True,blank=True)
    skype = models.CharField(max_length=100,null=True,blank=True)

    def __str__(self):
        return f'{self.profile.user.username} Social links'