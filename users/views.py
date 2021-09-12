from django.shortcuts import render, redirect, reverse
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse, JsonResponse
from django.conf import settings


from .mixins import (
	FormErrors,
	)

from .forms import (
	UserForm,
	UserProfileForm,
	AuthForm,
	)

from api.mixins import (
	HederaAccount,
	HederaData
	)

from api.models import Invoicing


result = "Error"
message = "Something went wrong. Please check and try again"

def sign_up(request):
	'''
	Basic view for user sign up
	'''
	
	#redirect if user is already signed in
	if request.user.is_authenticated:
		return redirect(reverse('users:account'))

	u_form = UserForm()
	up_form = UserProfileForm()
	
	if request.is_ajax():
		u_form = UserForm(data = request.POST)
		up_form = UserProfileForm(data = request.POST)
		
		#if both forms are valid, do something
		if u_form.is_valid() and up_form.is_valid():
			user = u_form.save()

			#commit = False is used as userprofile.user can not be null
			up = up_form.save(commit = False)
			up.user = user
			up.save()
			user.is_active = True
			user.email = user.username
			user.save()

			#create a Hedera account for user
			hed = HederaAccount(user)
			
			login(request, user)
			result = "Success"
			message = "Your profile is now active"
		else:
			message = FormErrors(u_form, up_form)

		data = {'result': result, 'message': message}
		return JsonResponse(data)
		
	context = {'u_form':u_form, 'up_form':up_form}
	return render(request, 'users/sign_up.html', context)




def sign_in(request):
	'''
	Basic view for user sign in
	'''

	#redirect if user is already signed in
	if request.user.is_authenticated:
		return redirect(reverse('users:account'))
	
	a_form = AuthForm()

	if request.is_ajax():
		a_form = AuthForm(data = request.POST)
		if a_form.is_valid():
			username = a_form.cleaned_data.get('username')
			password = a_form.cleaned_data.get('password')

			#authenticate Django built in authenticate - https://docs.djangoproject.com/en/3.1/ref/contrib/auth/
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				message = 'You are now logged in'
				result = "Success"

		else:
			message = FormErrors(a_form)
		
		data = {'result': result, 'message': message}
		return JsonResponse(data)
	
	context = {'a_form':a_form}
	return render(request, 'users/sign_in.html', context)




def sign_out(request):
	'''
	Basic view for user sign out
	'''
	logout(request)
	return redirect(reverse('users:sign-in'))




@method_decorator(login_required, name='dispatch')
class AccountView(TemplateView):
	'''
	Basic template view to render a demo user account
	'''
	template_name = "users/account.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		#we need to get the user's hbar balance
		user = self.request.user
		hedera_data = HederaData(user = user)
		context["balance"] = hedera_data.balance()

		#get transactions
		transactions = Invoicing.objects.filter(user = user)
		context["transactions"] = transactions

		return context

