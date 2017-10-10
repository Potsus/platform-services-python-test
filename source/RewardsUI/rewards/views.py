import logging
import requests

from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from .forms import PurchaseForm, UserFilter


class RewardsView(TemplateView):
    template_name = 'index.html'

    def __init__(self, logger=logging.getLogger(__name__)):
        self.logger = logger

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        
        # Handle the filter input
        context['clientele_data'] = [None]
        form = UserFilter(request.GET)
        email = request.GET.get('email')
        if email != None and email != '' and form.is_valid():
            response = requests.get("http://rewardsservice:7050/customer", params=request.GET)
            context['clientele_data'] = [response.json()]
            if context['clientele_data'] == [None]:
                form.add_error(None, 'User not found')
        
        if context['clientele_data'] == [None]:
            response = requests.get("http://rewardsservice:7050/clientele")
            context['clientele_data'] = response.json()



        context['user_filter'] = form

        #fill in the rest of the page context
        context['purchase_form'] = PurchaseForm

        response = requests.get("http://rewardsservice:7050/rewards")
        context['rewards_data'] = response.json()

        return TemplateResponse(
            request,
            self.template_name,
            context
        )

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        form = PurchaseForm(request.POST)
        if form.is_valid():
            r = requests.post("http://rewardsservice:7050/purchase", data=request.POST)

        context['purchase_form'] = form
        context['user_filter']   = UserFilter


        response = requests.get("http://rewardsservice:7050/rewards")
        context['rewards_data'] = response.json()

        response = requests.get("http://rewardsservice:7050/clientele")
        context['clientele_data'] = response.json()

        return TemplateResponse(
            request,
            self.template_name,
            context
        )   