from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.messages import get_messages


@login_required
def change_password_view(request):
    # Clear previous messages
    storage = get_messages(request)
    for _ in storage:
        pass  # This clears stored messages

    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, "Your password was successfully updated!")
            return redirect("dashboard")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "accounts/change_password.html", {"form": form})


# ✅ Login View
def login_view(request):
    if request.method == "POST":
        identifier = request.POST["username"]  # Can be email or username
        password = request.POST["password"]
        user = None

        # Check if identifier is an email
        if "@" in identifier:
            try:
                user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                messages.error(request, "Invalid email or password")
                return render(request, "accounts/login.html")

        # Authenticate the user
        user = authenticate(
            request, username=user.username if user else identifier, password=password
        )

        if user is not None:
            login(request, user)
            return redirect("dashboard")  # Redirect to dashboard after login
        else:
            messages.error(request, "Invalid username or password")

    return render(request, "accounts/login.html")


# ✅ Signup View
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Account created successfully! You can now log in."
            )
            return redirect("login")
        else:
            messages.error(request, "Something went wrong. Please check your input.")
    else:
        form = UserCreationForm()

    return render(request, "accounts/signup.html", {"form": form})


# ✅ Forgot Password View
def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST["email"]
        messages.info(
            request,
            f"If an account with {email} exists, a password reset email has been sent.",
        )
        return redirect("login")

    return render(request, "accounts/forgot_password.html")


# ✅ Dashboard View (Protected)
@login_required
def dashboard_view(request):
    return render(request, "accounts/dashboard.html")


# ✅ Profile View (Protected)
@login_required
def profile_view(request):
    return render(request, "accounts/profile.html")


# ✅ Logout View
def logout_view(request):
    logout(request)
    messages.success(request, "You have successfully logged out.")
    return redirect("login")
