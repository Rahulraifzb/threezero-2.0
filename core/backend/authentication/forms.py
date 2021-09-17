from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

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


