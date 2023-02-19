from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserChangeForm,UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    password1: forms.Field = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2: forms.Field = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username','email','password1','password2')

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Passwords don\'t match')
        return password2
    
    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user

class CustomUserChangeForm(UserChangeForm):
    password1: forms.Field = forms.CharField(label='Password',widget=forms.PasswordInput)
    password2: forms.Field = forms.CharField(label='Confirm Password',widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('username','email','password1','password2')