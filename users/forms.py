from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import AuthenticationForm

User = get_user_model()


class LoginForm(AuthenticationForm):
    username = forms.EmailField(label='Адрес электронной почты', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(label='Адрес электронной почты', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password_2 = forms.CharField(label='Подтверждение пароля',
                                 widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['email']

    def clean_email(self):
        """Проверяет почту пользователя."""
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('Такая почта уже существует')
        return email

    def clean(self):
        """Проверяет пароли на соответствие."""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_2 = cleaned_data.get('password_2')
        if password is not None and password != password_2:
            self.add_error('password_2', 'Пароли не совпадают')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserAdminCreationForm(forms.ModelForm):
    """Форма создания нового пользователя в админке."""
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password_2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email']

    def clean(self):
        """Проверяет пароли на соответствие."""
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_2 = cleaned_data.get('password_2')
        if password is not None and password != password_2:
            self.add_error('password_2', 'Пароли не совпадают')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    """Форма изменения данных для админа."""
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ['email', 'password', 'is_active', 'admin']

    def clean_password(self):
        return self.initial['password']


class UserChangeForm(forms.ModelForm):
    """Форма изменения данных для пользователя."""
    name = forms.CharField(label='Введите новое имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    surname = forms.CharField(label='Введите новую фамилию', widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone_number = forms.CharField(label='Контактный номер телефона', widget=forms.TextInput(attrs={'class': 'form-control'}))
    street = forms.CharField(label='Улица', widget=forms.TextInput(attrs={'class': 'form-control'}))
    house = forms.CharField(label='Дом', widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['name', 'surname', 'phone_number', 'street', 'house', 'flat']
        widgets = {
            'flat': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '-'})
        }
