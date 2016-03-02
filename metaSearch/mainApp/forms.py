from django import forms
from django.contrib.auth.models import User   # fill in custom user info then save it
from django.contrib.auth.forms import UserCreationForm

class MyRegistrationForm(UserCreationForm):
    email = forms.EmailField(required = True)
    first_name = forms.CharField(required = False)
    last_name = forms.CharField(required = False)



    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def save(self,commit = True):
        user = super(MyRegistrationForm, self).save(commit = False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']


        if commit:
            user.save()

        return user

class UpdateProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

