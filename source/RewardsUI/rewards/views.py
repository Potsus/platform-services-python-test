import logging
import requests

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from .forms import PurchaseForm


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__)):
        self.logger = logger

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        context['purchase_form'] = PurchaseForm

        response = requests.get("http://rewardsservice:7050/rewards")
        context['rewards_data'] = response.json()

        response = requests.get("http://rewardsservice:7050/clientele")
        context['clientele_data'] = response.json()

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        purchase_form = PurchaseForm(request.POST)
        if purchase_form.is_valid():
            r = requests.post("http://rewardsservice:7050/purchase", data=request.POST)

        context['purchase_form'] = purchase_form


        response = requests.get("http://rewardsservice:7050/rewards")
        context['rewards_data'] = response.json()

        response = requests.get("http://rewardsservice:7050/clientele")
        context['clientele_data'] = response.json()

        return TemplateResponse(
            request,
            self.template_name,
            context
        )   
