from django.urls import path
from . import views




urlpatterns = [
    path('', views.home),
    path('Login/', views.Login),
    path('Blogs',views.Blogs),
]