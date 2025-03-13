from django.shortcuts import render, redirect

from . forms import CreateUserForm, LoginForm, ThoughtForm, UpdateUserForm, UpdateProfilePicForm

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required

from django.contrib import messages

from . models import Thought, Profile

from django.contrib.auth.models import User

from django.core.mail import send_mail
from django.conf import settings


# Homepage

def homepage(request):

    return render(request, 'journal/index.html')


# Register

def register(request):

    form = CreateUserForm()

    if request.method == 'POST':

        form = CreateUserForm(request.POST)
        
        if form.is_valid():

            current_user = form.save(commit=False)

            form.save()

            send_mail("Welcome to Edenthought!", "Congratulations on creating your account.", settings.DEFAULT_FROM_EMAIL, [current_user.email])

            # As soon as a user has been created, it gets saved to the database and Django creates a profile and binds the user that was just created to this profile
            profile = Profile.objects.create(user=current_user)

            messages.success(request, "User created!")

            return redirect('my-login')
        
    context = {'RegistrationForm': form}

    return render(request, 'journal/register.html', context)


# Login

def my_login(request):

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect('dashboard')
            
    context = {'LoginForm': form}

    return render(request, 'journal/my-login.html', context)


# Logout

def user_logout(request):

    auth.logout(request)

    return redirect('')


# Dashboard

@login_required(login_url='my-login')
def dashboard(request):

    profile_pic = Profile.objects.get(user=request.user)

    context = {'ProfilePic': profile_pic}

    return render(request, 'journal/dashboard.html', context)


# Create thought

@login_required(login_url='my-login')
def create_thought(request):

    form = ThoughtForm()

    if request.method == 'POST':

        form = ThoughtForm(request.POST)

        if form.is_valid():

            thought = form.save(commit=False)

            thought.user = request.user

            thought.save()
            
            messages.success(request, "Thought created!")

            return redirect('my-thoughts')
        
    context = {'CreateThoughtForm': form}

    return render(request, 'journal/create-thought.html', context)


# My thoughts

@login_required(login_url='my-login')
def my_thoughts(request):

    current_user = request.user.id

    thought = Thought.objects.all().filter(user=current_user)

    context = {'AllThoughts': thought}

    return render(request, 'journal/my-thoughts.html', context)


# Update thought

@login_required(login_url='my-login')
def update_thought(request, pk):

    try:
        # Check the id matches and the user logged in matches the user who created it
        thought = Thought.objects.get(id=pk, user=request.user)

    except:
        return redirect('my-thoughts')

    form = ThoughtForm(instance=thought)

    if request.method == 'POST':

        form = ThoughtForm(request.POST, instance=thought)

        if form.is_valid():

            form.save()

            messages.success(request, "Thought updated!")
            
            return redirect('my-thoughts')
        
    context = {'UpdateThoughtForm': form}

    return render(request, 'journal/update-thought.html', context)


# Delete thought

@login_required(login_url='my-login')
def delete_thought(request, pk):

    try:
        thought = Thought.objects.get(id=pk, user=request.user)

    except:
        return redirect('my-thoughts')
    
    if request.method == 'POST':

        thought.delete()

        messages.success(request, "Thought deleted!")
        
        return redirect('my-thoughts')

    return render(request, 'journal/delete-thought.html')


# Manage profile

@login_required(login_url='my-login')
def manage_profile(request):

    form = UpdateUserForm(instance=request.user)

    profile = Profile.objects.get(user=request.user)

    form_2 = UpdateProfilePicForm(instance=profile)

    if request.method == 'POST':

        form = UpdateUserForm(request.POST, instance=request.user)

        # request.FILES allows for file uploads
        form_2 = UpdateProfilePicForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():

            form.save()

            return redirect('dashboard')

        if form_2.is_valid():

            form_2.save()

            return redirect('dashboard')
        
    context = {'UserUpdateForm': form, 'ProfilePicUpdateForm': form_2}

    return render(request, 'journal/manage-profile.html', context)


# Delete account

@login_required(login_url='my-login')
def delete_account(request):

    if request.method == 'POST':

        deleteUser = User.objects.get(username=request.user)

        deleteUser.delete()

        return redirect("")

    return render(request, 'journal/delete-account.html')