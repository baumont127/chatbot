from django.urls import path
from django.conf.urls import include
from . import views


urlpatterns = [
    path('login',views.login_page,name = "login"),
    path('', views.index, name='index'),
    path('add_ressource', views.form_ressource_view, name='form_ressource'),
    path('validation', views.validation, name='validation'),
    path('logout', views.logout_view, name='logout'),
    path('sign_in', views.signin, name='sign_in'),
]