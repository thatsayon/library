from django import forms 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 
from .constants import GENDER_TYPE
from .models import UserAccount

class UserRegistrationForm(UserCreationForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    class Meta:
        model = User 
        fields = ['username', 'password1', 'password2', 'first_name', 'last_name', 'email', 'birth_date', 'gender']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit == True:
            user.save()
            birth_date = self.cleaned_data.get('birth_date')
            gender = self.cleaned_data.get('gender')

            UserAccount.objects.create(
                user = user, 
                birth_date = birth_date,
                gender = gender,
                account_no = user.id + 100
            )
        return user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                ) 
            })

class UserUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
        
        if self.instance:
            try:
                user_account = self.instance.account 
            except UserAccount.DoesNotExist:
                user_account = None 

            if user_account:
                self.fields['birth_date'].initial = user_account.birth_date
                self.fields['gender'].initial = user_account.gender
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user_account, created = UserAccount.objects.get_or_create(user=user) 

            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.gender = self.cleaned_data['gender']
        
        return user
                    