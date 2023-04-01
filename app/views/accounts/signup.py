from django import forms
from django.utils.translation import gettext_lazy as _


class CreateAccountForm(forms.Form):
    first_name = forms.CharField(label=_("First Name"), max_length=100)
    last_name = forms.CharField(label=_("Last Name"), max_length=100)

    def signup(self, request, user):
        # Django all-auth will have already cleaned the form and returned any
        # errors, so `cleaned_data` is guaranteed to be valid if we get here.
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.save()
        return user
