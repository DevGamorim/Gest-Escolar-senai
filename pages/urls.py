from django.urls import path
from django.urls.resolvers import URLPattern

from . import views

app_name = "pages"

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home' ),
    path('perfil/criar/',views.criar_user,name='perfil_criar_user')
]