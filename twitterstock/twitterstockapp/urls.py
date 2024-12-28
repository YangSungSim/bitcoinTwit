from django.urls import path
from twitterstockapp import views

urlpatterns = [
    path('get_myasset/', views.get_myasset, name="bitcoin")
]