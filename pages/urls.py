from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

app_name = "pages"

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home' ),
]