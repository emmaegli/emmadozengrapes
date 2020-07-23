from django.urls import path
from blog.views import register_subscriber, unsubscribe

urlpatterns = [
    path("subscribe/", register_subscriber, name="register_blog_subscriber"),
    path("unsubscribe/", unsubscribe),
]
