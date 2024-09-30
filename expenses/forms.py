from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from .models import Group, Member, Expense, ExpenseCategory

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        help_texts = {
            'username': None,
            'email': None,
            'password1': None,
            'password2': None,
        }


    def __init__(self, *args, **kwargs):
        group = kwargs.pop('group', None)
        super().__init__(*args, **kwargs)
        if group:
            self.fields['participants'].queryset = group.members.all()

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', max_length=150)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name']

class MemberForm(forms.ModelForm):
    class Meta:
        model = Member
        fields = ['name']

class ExpenseForm(forms.ModelForm):
    num_people = forms.IntegerField(min_value=1, initial=1, label="Number of People to Split Among")
    member_names = forms.CharField(
        label="Members to Split With",
        max_length=255,
        help_text="Enter member names separated by commas"
    )


    class Meta:
        model = Expense
        fields = ['member', 'amount', 'category', 'description', 'member_names']
        widgets = {
            'description': forms.TextInput(attrs={
                'placeholder': 'if any'  
            }),
        }

    

    def clean_num_people(self):
        num_people = self.cleaned_data.get('num_people')
        if num_people < 1:
            raise forms.ValidationError("Number of people must be at least 1.")
        return num_people
