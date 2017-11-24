from django.shortcuts import render, redirect
from models import User
from django.contrib import messages

# Create your views here.

def main(request): # the root route will redirect to the main page (login/registration)
    return redirect('/main')

def index(request): # renders the login/registration page
    return render(request, 'login_app/index.html')

def create(request): # creates user
    errors = User.objects.user_validator(request.POST) # returns errors
    if len(errors): # if there are errors
        for error in errors:
            messages.error(request, error) # create flash message
    else: # if no errors
        new_user = User.objects.create_user(request.POST) # create user
        # success message for creating a account!
        messages.success(request, "Successfully registered! Welcome " + str(new_user.name)+"! Please login.") # display success message
    return redirect('/') # redirects back to root (/main)

def login(request): # login
    result = User.objects.login_validator(request.POST) # returns dictionary with error message and user
    if len(result['errors']): # if there are any errors
        for error in result['errors']: # error message
            messages.error(request, error)
        return redirect('/') # redirects to main page if error
    else: # if no error message
        # set request.session variables according to user's fields
        request.session['name']=result['user'].name
        request.session['username']=result['user'].username
        # request.session['last_name']=result['user'].last_name
        # request.session['email']=result['user'].email
        request.session['id']=result['user'].id
        # success message when logged in !
        messages.success(request,'You have successfuly logged in !') # display success message
        return redirect('/main/') # redirects to dashboard page

# def dashboard(request):
#     # return redirect('/dashboard')
#     return render(request, 'login_app/dashboard.html')

def logout(request): # logs out
    request.session.flush() # clears out session
    return redirect('/main') # redirects to root route
