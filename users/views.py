from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout 
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UpdateUserForm, UpdateProfileForm
from .models import UserProfile


def register_view(request):
    if request.user.is_authenticated:
      messages.info(request, 'You are already registered and logged in')
      return redirect('core:home')
    if request.method == 'POST':
        register_form = CustomUserCreationForm(request.POST)
        if register_form.is_valid():
            user = register_form.save()
            login(request, user)
            messages.success(request, 'Your account has been created successfully!')
            return redirect('core:home')
        else:
            messages.error(request, 'Something went wrong!')
    else:
        register_form = CustomUserCreationForm()

    context = {
        'register_form': register_form
      }
    return render(request, 'users/register.html', context)


def login_view(request):
    if request.user.is_authenticated:
      messages.info(request, 'You are already logged in')
      return redirect('core:home')
    if request.method == 'POST':
        login_form = CustomAuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
          user = login_form.get_user()
          login(request, user)
          messages.success(request, f'Welcome back {user.first_name.capitalize()}') 
          if 'next' in request.POST:
            return redirect(request.POST.get('next'))
          else:
            return redirect('core:home')
    else:
        login_form = CustomAuthenticationForm()
    context = {
        'login_form': login_form
    }
    return render(request, 'users/login.html', context)


@login_required
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.info(request, "You have been logged out successfully.")
        return redirect('core:home')
    else:
        messages.error(request, "Method Not Allowed!")
        return redirect('core:home')


def profile_view(request, slug):
    user_profile = get_object_or_404(UserProfile, slug=slug)
    current_user = request.user
    if current_user.is_authenticated and current_user == user_profile.user:
        if request.method == 'POST':
            update_profile_form = UpdateProfileForm(request.POST, request.FILES, instance=user_profile)
            update_user_form = UpdateUserForm(request.POST, instance=user_profile.user)
            if update_profile_form.is_valid() and update_user_form.is_valid():
                update_profile_form.save()
                update_user_form.save()
                messages.success(request, 'Profile updated successfully')
                return redirect ('users:profile', slug=slug)
            else:
                messages.error(request, 'Something went wrong!')
        else:
            update_profile_form = UpdateProfileForm(instance=user_profile)
            update_user_form = UpdateUserForm(instance=user_profile.user)

        context = {
            'user_profile': user_profile,
            'update_profile_form': update_profile_form,
            'update_user_form': update_user_form,
        }
    else:
        context = {
            'user_profile': user_profile,
        }
    return render(request, 'users/profile.html', context)
