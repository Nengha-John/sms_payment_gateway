from django.urls import path
from . import views

app_name = 'auth'
urlpatterns = [
    path('login/',views.loginView,name='login'),
    path('register/',views.registerView,name='register'),
    path('logout',views.logout,name='logout')
]