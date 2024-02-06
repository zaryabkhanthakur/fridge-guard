from django import forms
from .models import FridgeItem, Order
from django.core.exceptions import ValidationError


class UserCreationForm(forms.Form):
    
    GROUPS = (
        ('Chef', "Chef"),
        ('Rider', 'Rider'),
    )

    username = forms.CharField(min_length=3, required=True)
    password = forms.CharField(min_length=8, required=True, widget=forms.PasswordInput)
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=GROUPS, required=True)
    
class RiderInsertionForm(forms.Form):
    order_code = forms.CharField(required=True)
    
    def clean_order_code(self):
        order_code = self.cleaned_data['order_code']
        try:
            order = Order.objects.get(order_code=order_code)
        except Order.DoesNotExist as e:
            raise ValidationError('Order key is invalid')

        return order_code

class ChefInsertionFrom(forms.Form):
    item = forms.ModelChoiceField(queryset=FridgeItem.objects.all(), required=True)
    quantity = forms.IntegerField(min_value=1, required=True)


class ChefRemoveFrom(forms.Form):
    item = forms.ModelChoiceField(queryset=FridgeItem.objects.filter(quantity__gt=0), required=True)
    quantity = forms.IntegerField(min_value=1, required=True)
    
    
    def clean_quantity(self):
        qty = self.cleaned_data.get("quantity")
        item = self.cleaned_data.get("item")
        print(item)
        if qty > item.quantity:
            raise ValidationError(f"You can't take more then available, remainging {item.quantity}")
        
        return qty