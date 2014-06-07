# encoding: utf-8
from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db.models import Q
from django.utils.translation import ugettext_lazy as _
from revengeusers.models import revengeLvl, revengeUser

class ConfigurationForm(forms.ModelForm):

    validate_password = forms.CharField(required=False, widget=forms.PasswordInput)
    password = forms.CharField(required=False, widget=forms.PasswordInput)
    iduser = forms.CharField()

    class Meta:
        model = get_user_model()
        fields = (
            'iduser',

            'email', 'password', 'validate_password', 'privacy',

            'first_name', 'last_name', 'sex', 'avatar',

            'city', 'state', 'country',

            'url_revenge', 'url_twitter', 'url_fb', 'url_gpus',
            'about_you', 'alert_revengers')

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        if self.user and not kwargs.get('instance'):
            try:
                kwargs.update({'instance': revengeUser.objects.get(pk=self.user.pk)})
            except revengeUser.DoesNotExist:
                pass
        super(ConfigurationForm, self).__init__(*args, **kwargs)
        self.instance.user = self.user
        self.fields['email'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Email*', 'required' : ''})
        self.fields['password'].widget = forms.PasswordInput()
        self.fields['password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Contraseña'})
        self.fields['validate_password'].widget = forms.PasswordInput()
        self.fields['validate_password'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Repita la constraseña'})
        self.fields['privacy'].widget = forms.Select(choices=self.fields['privacy'].choices)
        self.fields['privacy'].widget.attrs.update({'class': 'form-control',})

        self.fields['first_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Nombre*', 'required' : ''})
        self.fields['last_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Apellidos'})
        self.fields['sex'].widget = forms.Select(choices=self.fields['sex'].choices)
        self.fields['sex'].widget.attrs.update({'class': 'form-control',})
        self.fields['avatar'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Avatar*'})

        self.fields['url_twitter'].widget.attrs.update({'class': 'form-control', 'placeholder': 'URL Twitter'})
        self.fields['url_gpus'].widget.attrs.update({'class': 'form-control', 'placeholder': 'URL Facebook'})
        self.fields['url_fb'].widget.attrs.update({'class': 'form-control', 'placeholder': 'URL Google+'})
        self.fields['url_revenge'].widget.attrs.update({'class': 'form-control', 'placeholder': 'URL en RB'})
        self.fields['url_fb'].widget.attrs.update({'class': 'form-control', 'placeholder': 'URL Facebook'})

        self.fields['city'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Ciudad'})
        self.fields['state'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Provincia/estado'})
        self.fields['country'].widget.attrs.update({'class': 'form-control', 'placeholder': 'País'})

        self.fields['about_you'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Acerca de tí'})
        self.fields['alert_revengers'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Aviso para tus vengadores'})

    def clean(self):
        cleaned_data = super(ConfigurationForm, self).clean()
        try:
            password1 = cleaned_data['password']
        except LookupError:
            password1 = ""
        try:
            password2 = cleaned_data['validate_password']
        except LookupError:
            password2 = ""
        if password1 != password2:
            raise forms.ValidationError(_('Passwords are different'))
        try:
            email = cleaned_data["email"]
        except LookupError:
            email = ""
        if get_user_model().objects.filter(Q(email=email), ~Q(id = cleaned_data["iduser"])).count() > 0:
            raise forms.ValidationError(_('Email ya existe'))
        return cleaned_data

    def save(self, commit=True):
        user = super(ConfigurationForm, self).save(commit=False)
        #import ipdb; ipdb.set_trace()
        password = self.cleaned_data["password"]
        if password:
            user.set_password(password)
        else:
            orUser = get_user_model().objects.get(id=user.id)
            user.password = orUser.password
        if commit:
            user.save()
        return user


class RevengeUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username",)

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            get_user_model()._default_manager.get(username=username)
        except get_user_model().DoesNotExist:
            return username
        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_email(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            get_user_model()._default_manager.get(email=email)
        except get_user_model().DoesNotExist:
            return email
        raise forms.ValidationError(
            self.error_messages['duplicate_email'],
            code='duplicate_email',
        )


class RevengeUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()

    def __init__(self, *args, **kwargs):
        super(RevengeUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['friends'].queryset = self.fields['friends'].queryset.exclude(pk=self.instance.pk)


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
        fields = ('username', 'email', 'password')
        widgets = {'password': forms.PasswordInput}

    def clean(self):
        cleaned_data = super(SignUpForm, self).clean()
        try:
            password1 = cleaned_data['password']
        except LookupError:
            password1 = ""
        try:
            password2 = cleaned_data['validate_password']
        except LookupError:
            password2 = ""
        if password1 != password2:
            raise forms.ValidationError(_('Passwords are different'))
        try:
            email = cleaned_data["email"]
        except LookupError:
            email = ""
        if get_user_model().objects.filter(email=email).count() > 0:
            raise forms.ValidationError(_('Email ya existe'))
        return cleaned_data

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        clean_password = user.password
        user.set_password(user.password)
        lvl = revengeLvl.objects.get(id=1)
        if commit:
            user.level = lvl
            user.save()
        return authenticate(username=user.username, password=clean_password)
