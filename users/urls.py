from django.conf.urls import url
from django.urls import path
from . import views


app_name = "users"

urlpatterns = [
	
	path('', views.sign_in, name="sign-in"),
	url(r'^sign-up', views.sign_up, name="sign-up"),
	url(r'^sign-out', views.sign_out, name="sign-out"),
	url(r'^account', views.AccountView.as_view(), name="account"),
	]