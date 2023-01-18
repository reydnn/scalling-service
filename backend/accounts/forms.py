from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm


class AccountCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email")


class AccountChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ("username", "email")
