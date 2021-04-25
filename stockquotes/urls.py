from django.urls import path
from stockquotes import views

urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
]