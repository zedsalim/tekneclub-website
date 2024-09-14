from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import NewUser, UserProfile, Role
from external_data.models import StudyYear, University, Department, Interests

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'bg-gray-700 appearance-none border border-gray-600 rounded w-full py-2 px-4 text-white', 'placeholder': 'First Name', 'autofocus': True})
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'bg-gray-700 appearance-none border border-gray-600 rounded w-full py-2 px-4 text-white', 'placeholder': 'Last Name'})
    )
    username = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'bg-gray-700 appearance-none border border-gray-600 rounded w-full py-2 px-4 text-white', 'placeholder': 'Username'})
    )
    email = forms.EmailField(
        max_length=100,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'bg-gray-700 appearance-none border border-gray-600 rounded w-full py-2 px-4 text-white', 'placeholder': 'Email'})
    )
    gender = forms.ChoiceField(
        choices=UserProfile.GENDER_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'bg-gray-700 border border-gray-600 rounded w-full py-2 px-4 text-white'})
    )
    university = forms.ModelChoiceField(
        queryset=University.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'bg-gray-700 border border-gray-600 rounded w-full py-2 px-4 text-white'})
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'bg-gray-700 border border-gray-600 rounded w-full py-2 px-4 text-white'})
    )
    study_year = forms.ModelChoiceField(
        queryset=StudyYear.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'bg-gray-700 border border-gray-600 rounded w-full py-2 px-4 text-white'})
    )
    interests = forms.ModelMultipleChoiceField(
        queryset=Interests.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'bg-gray-700 border-gray-600 text-white text-left px-3 interests-scrollable'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'bg-gray-700 appearance-none border border-gray-600 rounded w-full py-2 px-4 text-white', 'placeholder': 'Password'})
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'bg-gray-700 appearance-none border border-gray-600 rounded w-full py-2 px-4 text-white', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = NewUser
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2', 'gender', 'university', 'department', 'study_year', 'interests')

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        if not UserProfile.objects.filter(user=user).exists():
            user_profile = UserProfile.objects.create(
                user=user,
                gender=self.cleaned_data.get('gender'),
                university=self.cleaned_data.get('university'),
                department=self.cleaned_data.get('department'),
                study_year=self.cleaned_data.get('study_year')
            )
            user_profile.interests.set(self.cleaned_data.get('interests'))
            participant_role, created = Role.objects.get_or_create(name='Participant')
            user_profile.role.add(participant_role)
        return user

class CustomAuthenticationForm(AuthenticationForm):
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'bg-gray-700 appearance-none border border-gray-600 rounded w-full py-2 px-4 text-white',
            'placeholder': 'Password'
        })
    )

    class Meta:
        model = NewUser
        fields = ('email', 'password')


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'bg-gray-700 appearance-none border border-gray-600 rounded w-full py-2 px-4 text-white', 'placeholder': 'First Name', 'autofocus': True})
    )
    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={'class': 'bg-gray-700 appearance-none border border-gray-600 rounded w-full py-2 px-4 text-white', 'placeholder': 'Last Name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'bg-gray-700 appearance-none border border-gray-600 rounded w-full py-2 px-4 text-white', 'placeholder': 'Email'})
    )
    
    class Meta:
        model = NewUser
        fields = ['first_name', 'last_name', 'email']

class UpdateProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(
        choices=UserProfile.GENDER_CHOICES,
        required=True,
        widget=forms.Select(attrs={'class': 'bg-gray-700 border border-gray-600 rounded w-full py-2 px-4 text-white'})
    )
    profile_pic = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={'class': 'bg-gray-700 appearance-none border border-gray-600 rounded w-full py-2 px-4 text-white'})
    )
    study_year = forms.ModelChoiceField(
        queryset=StudyYear.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'bg-gray-700 border border-gray-600 rounded w-full py-2 px-4 text-white'})
    )
    university = forms.ModelChoiceField(
        queryset=University.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'bg-gray-700 border border-gray-600 rounded w-full py-2 px-4 text-white'})
    )
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=True,
        widget=forms.Select(attrs={'class': 'bg-gray-700 border border-gray-600 rounded w-full py-2 px-4 text-white'})
    )
    interests = forms.ModelMultipleChoiceField(
        queryset=Interests.objects.all(),
        required=True,
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'bg-gray-700 border-gray-600 text-white text-left px-3 interests-scrollable'})
    )
    github_url = forms.URLField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'bg-gray-700 appearance-none border border-gray-600 rounded w-full py-2 px-4 text-white', 'placeholder': 'GitHub URL'})
    )
    linkedin_url = forms.URLField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'bg-gray-700 appearance-none border border-gray-600 rounded w-full py-2 px-4 text-white', 'placeholder': 'LinkedIn URL'})
    )

    class Meta:
        model = UserProfile
        fields = ['gender', 'profile_pic', 'study_year', 'university', 'department', 'interests', 'github_url', 'linkedin_url']
