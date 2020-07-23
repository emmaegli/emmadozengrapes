from django.db import models
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.tokens import PasswordResetTokenGenerator


from blog.forms import BlogSubscriberRegisterForm
from blog.models import BlogSubscriber, BlogPage
from django.utils import timezone

# Create your views here.


def register_subscriber(request):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = BlogSubscriberRegisterForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Successfully signed up for email subscription! You should receive a verification email shortly",
            )
    else:
        form = BlogSubscriberRegisterForm()

    redirect_url = form["next_location"].value() or form["next_location"].initial

    return redirect(redirect_url)


def unsubscribe(request):
    token = request.GET.get("token", None)
    if not token:
        return redirect("/blog")
    try:
        subscriber = BlogSubscriber.objects.filter(
            models.Q(raw_email=token) | models.Q(user__email=token)
        )
    except BlogSubscriber.DoesNotExist:
        pass

    messages.SUCCESS(
        "You have successfully unsubscribed to Emma Dozen Grapes Newsletter"
    )
    return redirect("/blog")

