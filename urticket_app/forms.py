from django import forms
from .models import Event, Ticket, OrderItem, Order
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

class SignupForm(forms.Form):
    USER_TYPES = [('member', 'Member'), ('organizer', 'Organizer')]
    
    user_type = forms.ChoiceField(choices=USER_TYPES, widget=forms.RadioSelect(attrs={'class': 'form-radio text-blue-600'}))
    first_name = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50'}),
        label="First Name"
    )
    last_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50'}),
        label="Last Name"
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50'}),
        label="Phone"
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50'}),
        label="Email"
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50'}),
        label="Password"
    )
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean_password(self):
        password = self.cleaned_data['password']
        validate_password(password)
        return password

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        return phone

class LoginForm(AuthenticationForm):
    user_type = forms.ChoiceField(
        choices=[('member', 'Member'), ('organizer', 'Organizer')],
        widget=forms.RadioSelect(attrs={'class': 'form-radio text-blue-600'}),
        required=False
    )
    username = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50'}), label = 'Email')
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50'}))
    
    
class AddeventForm(forms.ModelForm):
    class Meta:
       model = Event 
       fields = '__all__'
       
       widgets = {
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50',
                'accept': 'image/*', 
                'title': 'Upload event image here'
            }),
            'date_time': forms.DateTimeInput(attrs={
                'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50', 
                'type': 'datetime-local'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50',
                'placeholder': 'Event Title'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50',
                'placeholder': 'Event Location'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-textarea mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50',
                'placeholder': 'Event Description',
                'rows': 4
            }),
            'organizer': forms.Select(attrs={
                'class': 'form-select mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50'
            }),
        }

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = '__all__'
        widgets = {
            'name': forms.Select(attrs={
                'class': 'form-select mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50', 'label': 'Type of Ticket' 
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50',
                'placeholder': 'Ticket Price'
            }),
            'qavailable': forms.NumberInput(attrs={
                'class': 'form-input mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50',
                'placeholder': 'Quantity Available'
            }),
            'event': forms.Select(attrs={
                'class': 'form-select mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring focus:ring-blue-500 focus:ring-opacity-50'
            }),
        }

class TicketPurchaseForm(forms.Form):
    ticket = forms.ModelChoiceField(
        queryset=Ticket.objects.all(),
        widget=forms.Select(attrs={
            'class': 'block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500'
        }),
        label="Select Ticket Type"
    )
    quantity = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'block w-full mt-1 border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500',
            'placeholder': 'Enter quantity'
        }),
        label="Quantity"
    )

    def clean(self):
        cleaned_data = super().clean()
        ticket = cleaned_data.get("ticket")
        quantity = cleaned_data.get("quantity")

        if ticket and quantity and quantity > ticket.qavailable:
            raise forms.ValidationError(f"Only {ticket.qavailable} tickets are available.")
        return cleaned_data


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = []
