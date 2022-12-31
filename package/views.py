from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json

from .forms import CreateUserForm
from .models import Packages, Services


# user registration


def RegisterPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')
        if form.error_messages :
            print(form.errors.as_data())
        else:
            return redirect('register')
    context = {'form': form}
    return render(request, 'package/register.html', context)

# user login

def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username OR password is incorrect')
                return redirect('login')
        return render(request, 'package/login.html')

# user logout
def logoutUser(request):
    logout(request)
    return redirect('login')

# home page for logged in user
@login_required(login_url='login')
def Home(request):
    services = Services.objects.all()
    service_list = []
    for service in services:
        details = json.loads(service.details)
        service_list.append([service.name, details['description']])

    if request.method == 'POST':
        services = request.POST.getlist('services_list')
        package_list = []
        for service in services:
            print(service)
            service = Services.objects.get(name=service)
            details = json.loads(service.details) 
            # print(details.get('is_service'))
            if details.get('is_service') != None:
                if details['is_service'] == True:
                    package = Packages.objects.filter(service_ids__contains=service.id)
                    package_list.append(package)
            print(package_list)
        return redirect('home')

    context = {'service_list': service_list}
    return render(request, 'package/home.html', context)
