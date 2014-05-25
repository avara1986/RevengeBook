from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _


class SignInForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
        widgets = {'password': forms.PasswordInput}

    def clean(self):
        cleaned_data = super(SignInForm, self).clean()
        self._validate_unique = False
        #import ipdb; ipdb.set_trace()
        username = cleaned_data['username']
        password = cleaned_data['password']
        user = authenticate(username=username, password=password)
        if not user:
            raise forms.ValidationError(_('Username and password are invalid'))
        self.user = user
        return cleaned_data


class SignUpForm(forms.ModelForm):
    validate_password = forms.CharField(label=_("Repeat Password"), widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('username', 'password')
        widgets = {'password': forms.PasswordInput}

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        password1 = cleaned_data['password']
        password2 = cleaned_data['validate_password']

        if password1 != password2:
            raise forms.ValidationError(_('Passwords are different'))

        return cleaned_data

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        clean_password = user.password
        user.set_password(user.password)
        if commit:
            user.save()
        return authenticate(username=user.username, password=clean_password)
