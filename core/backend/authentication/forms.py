from django.db.models import fields
from core.backend.authentication.models import Profile,Social
from django import forms
from django.contrib.auth import models
from django.contrib.auth.forms import UserCreationForm,PasswordChangeForm
from django.contrib.auth.models import User
from django.forms import widgets
from django.utils.translation import ugettext_lazy as _


class RegisterationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username","email","password1","password2"]

    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"placeholder":"John deo","class":"form-control"})
        self.fields["email"].widget.attrs.update({"placeholder":"john@gmail.com","class":"form-control"})
        self.fields["password1"].widget.attrs.update({"placeholder":"............","class":"form-control"})
        self.fields["password2"].widget.attrs.update({"placeholder":"............","class":"form-control"})

class LoginForm(forms.Form):
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "placeholder":"john@example.com",
                "class":"form-control form-control-merge"
            }
        )
    )

    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                "placeholder":"...........",
                "class":"form-control form-control-merge"
            }
        )
    )

class NewPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ["old_password","new_password1","new_password2"]

    def __init__(self,*args,**kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget.attrs.update({"placeholder":"Old Password","class":"form-control"})
        self.fields["new_password1"].widget.attrs.update({"placeholder":"New Password","class":"form-control"})
        self.fields["new_password2"].widget.attrs.update({"placeholder":"Confirm New Password","class":"form-control"})

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["first_name","last_name","username","email"]


    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["first_name"].widget.attrs.update({"placeholder":"John","class":"form-control"})
        self.fields["last_name"].widget.attrs.update({"placeholder":"Deo","class":"form-control"})
        self.fields["username"].widget.attrs.update({"placeholder":"johndeo","class":"form-control"})
        self.fields["email"].widget.attrs.update({"placeholder":"johndeo@gmail.com","class":"form-control"})

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.exclude(pk=self.instance.pk).filter(username=username).exists():
            raise forms.ValidationError(u'Username "%s" is already in use.' % username)
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.exclude(email=self.instance.email).filter(email=email).exists():
            raise forms.ValidationError(u'Email "%s" is already exists.' % email)
        return email

class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ["mobile","image","bio","birthday","state","street_address","website"]
        widgets = {
            'birthday': widgets.DateInput(attrs={'type': 'date'})
        }

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["mobile"].widget.attrs.update({"placeholder":"1 234 567 8900","class":"form-control phone-number-mask"})
        self.fields["image"].widget.attrs.update({"hidden":True,"accept":"image/*","id":"account-upload"})
        self.fields["bio"].widget.attrs.update({"placeholder":"Your Bio data here...","class":"form-control",'rows':4,'style':'resize:none;'})
        self.fields["birthday"].widget.attrs.update({"type":"date","placeholder":"Birth Date","class":"form-control flatpickr flatpickr-input active"})
        self.fields["state"].widget.attrs.update({"placeholder":"State...","class":"form-control"})
        self.fields["street_address"].widget.attrs.update({"placeholder":"Address...","class":"form-control"})
        self.fields["website"].widget.attrs.update({"placeholder":"Website Url","class":"form-control"})

    
    def clean_mobile(self):
        mobile = self.cleaned_data.get("mobile")
        if Profile.objects.exclude(mobile=self.instance.mobile).filter(mobile=mobile).exists():
            raise forms.ValidationError(u'Mobile "%s" is already exists.' % mobile)
        return mobile

class SocialUpdateForm(forms.ModelForm):
    class Meta:
        model = Social
        fields = ["facebook","instagram","twitter","github","linkedIn","skype"]

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["instagram"].widget.attrs.update({"placeholder":"https://www.instagram.com/rahulraifzb","class":"form-control"})
        self.fields["facebook"].widget.attrs.update({"placeholder":"https://www.facebook.com/rahulraifzb","class":"form-control"})
        self.fields["twitter"].widget.attrs.update({"placeholder":"https://www.twitter.com/rahulraifzb","class":"form-control"})
        self.fields["github"].widget.attrs.update({"placeholder":"https://github.com/rahulraifzb","class":"form-control"})
        self.fields["skype"].widget.attrs.update({"placeholder":"https://join.skype.com/invite/UGQNE4baJzNN","class":"form-control"})
        self.fields["linkedIn"].widget.attrs.update({"placeholder":"https://www.linkedin.com/in/rahulraifzb","class":"form-control"})

    def clean_facebook(self):
        facebook = self.cleaned_data.get("facebook")
        if Social.objects.exclude(facebook=self.instance.facebook).filter(facebook=facebook).exists():
            raise forms.ValidationError(u'Facebook url "%s" already associated with another user.'% facebook)
        return facebook

    def clean_instagram(self):
        instagram = self.cleaned_data.get("instagram")
        if Social.objects.exclude(instagram=self.instance.instagram).filter(instagram=instagram).exists():
            raise forms.ValidationError(u'Instagram url "%s" already associated with another user.' % instagram)
        return instagram

    def clean_twitter(self):
        twitter = self.cleaned_data.get("twitter")
        if Social.objects.exclude(twitter=self.instance.twitter).filter(twitter=twitter).exists():
            raise forms.ValidationError(u'Twitter url "%s" already associated with another user.' % twitter)
        return twitter

    def clean_github(self):
        github = self.cleaned_data.get("github")
        if Social.objects.exclude(github=self.instance.github).filter(github=github).exists():
            raise forms.ValidationError(u'Github url "%s" already associated with another user.' % github)
        return github

    def clean_skype(self):
        skype = self.cleaned_data.get("skype")
        if Social.objects.exclude(skype=self.instance.skype).filter(skype=skype).exists():
            raise forms.ValidationError(u'Skype url "%s" already associated with another user.' % skype)
        return skype

    def clean_linkedin(self):
        linkedin = self.cleaned_data.get("linkedin")
        if Social.objects.exclude(linkedin=self.instance.linkedin).filter(linkedin=linkedin).exists():
            raise forms.ValidationError(u'LinkedIn url "%s" already associated with another user.' % linkedin)
        return linkedin

    