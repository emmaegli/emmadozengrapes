from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from blog.models import BlogSubscriber


class BlogSubscriberRegisterForm(forms.Form):

    email = forms.EmailField(required=False)

    user = forms.IntegerField(min_value=1, required=False)

    next_location = forms.CharField(max_length=150, initial="/blog", required=False)

    def clean(self):
        cleaned_data = super().clean()

        if not cleaned_data.get("email", None) and not cleaned_data.get("user", None):
            raise ValidationError(
                "You must specify either an email or user to subscribe"
            )

        if cleaned_data.get("user"):
            try:
                cleaned_data["user"] = User.objects.get(cleaned_data.get("user"))
            except User.DoesNotExist:
                raise ValidationError("You must specify a valid user ID")

        return cleaned_data

    def save(self) -> BlogSubscriber:
        kwargs = {}
        if self.cleaned_data["user"]:
            kwargs["user"] = self.cleaned_data["user"]
        else:
            kwargs["raw_email"] = self.cleaned_data["email"]

        sub, created = BlogSubscriber.objects.get_or_create(**kwargs)
        if created:
            sub.send_registration_confirmation()

        return sub

