from django.urls import path
from . import views

# URL Configuration
urlpatterns = [
    path('', views.sayhello),
    path('selenium', views.screenshotWithSelenium),
    path('pagespeed', views.screenshotWithPageSpeed),
    path('urlbox', views.screenshotWithUrlbox),
    path('hti', views.screenshotWithHtml2Image),
]
