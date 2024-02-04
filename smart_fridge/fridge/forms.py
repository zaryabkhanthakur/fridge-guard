from django import forms


class UserCreationForm(forms.Form):
    
    GROUPS = (
        ('Chef', "Chef"),
        ('Rider', 'Rider'),
    )

    username = forms.CharField(min_length=3, required=True)
    password = forms.CharField(min_length=8, required=True, widget=forms.PasswordInput)
    email = forms.EmailField(required=True)
    role = forms.ChoiceField(choices=GROUPS, required=True)
    
