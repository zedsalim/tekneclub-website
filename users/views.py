from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout 
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from .forms import *
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


def password_reset_request(request):
    if request.user.is_authenticated:
        messages.error(request, "Please log out first.")
        return redirect('core:home')
    User = get_user_model()
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            user = User.objects.filter(email=email).first()
            if user:
                site = get_current_site(request)
                subject = "Password Reset Request"
                email_template_name = "users/password_reset_email.html"
                context = {
                    'email': email,
                    'domain': site.domain,
                    'site_name': site.name,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol': 'https' if request.is_secure() else 'http',
                }
                email_body = render_to_string(email_template_name, context)
                send_mail(subject, email_body, settings.DEFAULT_FROM_EMAIL, [email], fail_silently=False)
                messages.info(request, f"Password reset email sent to {email}")
                request.session['password_reset_requested'] = True
            else:
                messages.error(request, f"Account not found with this email.")
                return redirect('users:password_reset')
            return redirect('users:password_reset_done')
    else:
        form = CustomPasswordResetForm()

    context = {
        'form': form,
    }
    return render(request, 'users/password_reset.html', context)

def password_reset_done(request):
    if request.user.is_authenticated:
        messages.error(request, "Please log out first.")
        return redirect('core:home')

    if request.session.get('password_reset_requested', False):
        del request.session['password_reset_requested']
        return render(request, 'users/password_reset_done.html')
    else:
        messages.error(request, "Unauthorized access")
        return redirect('users:password_reset')


def password_reset_confirm(request, uidb64, token):
    if request.user.is_authenticated:
        messages.error(request, "Please log out first.")
        return redirect ('core:home')
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            form = CustomSetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, f"Password reset successfully")
                return redirect('users:login')
        else:
            form = CustomSetPasswordForm(user)
        
        context = {
            'form': form,
        }
        return render(request, 'users/password_reset_confirm.html', context)

    else:
        messages.error(request, "Invalid password reset attempt")
        return redirect('core:home')