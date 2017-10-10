from django import forms

class PurchaseForm(forms.Form):
    email = forms.EmailField(label='Enter Email Address', max_length=100)
    total = forms.DecimalField(label='Enter Order Total', decimal_places=2)