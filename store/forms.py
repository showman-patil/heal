from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Review, UserProfile


class UserRegistrationForm(UserCreationForm):
    name = forms.CharField(max_length=200, required=True, label='Name')
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('name', 'email', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common_class = (
            'w-full px-4 py-2 border border-gray-300 rounded-lg '
            'focus:outline-none focus:ring-2 focus:ring-green-500 '
            'focus:border-transparent text-sm'
        )
        placeholders = {
            'name': 'Enter your full name',
            'email': 'Enter your email',
            'username': 'Choose a username',
            'password1': 'Create a password',
            'password2': 'Confirm your password',
        }
        for field_name, field in self.fields.items():
            field_class = common_class
            if field_name in ('password1', 'password2'):
                field_class = f'{common_class} pr-10'
            field.widget.attrs['class'] = field_class
            field.widget.attrs['placeholder'] = placeholders.get(field_name, '')
            field.help_text = ''

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        full_name = self.cleaned_data.get('name', '').strip()
        if full_name:
            name_parts = full_name.split(maxsplit=1)
            user.first_name = name_parts[0]
            user.last_name = name_parts[1] if len(name_parts) > 1 else ''
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
    remember_me = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        common_class = (
            'w-full px-4 py-2 border border-gray-300 rounded-lg '
            'focus:outline-none focus:ring-2 focus:ring-green-500 '
            'focus:border-transparent text-sm'
        )
        self.fields['username'].widget.attrs.update(
            {
                'class': common_class,
                'placeholder': 'Enter username',
            }
        )
        self.fields['password'].widget.attrs.update(
            {
                'class': f'{common_class} pr-10',
                'placeholder': 'Enter password',
                'id': 'id_password',
            }
        )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city', 'state', 'postal_code', 'bio', 'avatar')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your experience...'}),
        }


class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    postal_code = forms.CharField(max_length=20)
    payment_method = forms.ChoiceField(
        choices=[
            ('credit_card', 'Credit Card'),
            ('debit_card', 'Debit Card'),
            ('upi', 'UPI'),
            ('net_banking', 'Net Banking'),
            ('cod', 'Cash on Delivery'),
        ]
    )
