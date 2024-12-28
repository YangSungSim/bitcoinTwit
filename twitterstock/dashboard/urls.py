from django.urls import path
from dashboard import views

urlpatterns = [
    path('bitcoin/', views.get_bitcoin, name="bitcoin"),
    path('korea-bond/', views.get_korea_bond, name="korea_bond"),
    path('us_bond/', views.get_us_bond, name="us_bond"),
    path('interest/', views.get_interest, name="interest"),
    path('p2p/', views.get_p2p, name="p2p"),
    path('realestate/', views.get_realestate, name="realestate"),
    path('etf/', views.get_etf, name="etf"),
    path('us_index/', views.get_us_index, name="us_index")
]