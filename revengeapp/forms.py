from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import ugettext_lazy as _


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
    remember_me = forms.BooleanField(label=_('Remember me'),
                                     required=False,
                                     initial=True)

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


class RevengeMilestoneForm(forms.Form):
    friend = forms.CharField(max_length=100, required=True)
    point = forms.CharField(max_length=100, required=True)
    comment = forms.CharField(max_length=250, required=True)


class AddFriendForm(forms.Form):
    friend = forms.CharField(max_length=100, required=True)
