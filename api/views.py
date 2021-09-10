from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import JsonResponse

from .mixins import (
	HederaAccount,
	HederaPayment,
	HederaData,
	)

from .models import (
	Invoicing
	)



@method_decorator(login_required, name='dispatch')
class CartView(TemplateView):
	'''
	Basic template view to render a demo cart
	'''
	template_name = "api/cart.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)

		#we need to get the user's hbar balance
		user = self.request.user
		hedera_data = HederaData(user = user)
		context["balance"] = hedera_data.balance()
		
		return context




@login_required
def payment(request):

	'''
	AJAX function to handle a Hedera payment
	'''

	if request.method == "POST":

		user = request.user
		description = request.POST.get("description", None)
		amount = request.POST.get('amount')

		payment = HederaPayment(
			user=user,
			amount=amount,
			description = description,
			).create()

		if payment["message"] == "Perfect":

			invoice = Invoicing(
				user = user,
				amount = int(amount) * 100_000,
				tran_id = payment["tran_id"],
				description = description,
				)
			invoice.save()

			data = {'result': 'Success', "message":payment["message"]}
			return JsonResponse(data)

		else:

			data = {'result': 'Error', "message":payment["message"]}
			return JsonResponse(data)

	else:

		data = {'result': 'Error'}
		return JsonResponse(data)


