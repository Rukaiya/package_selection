from django.shortcuts import render, redirect
from django.http.response import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json
from collections import Counter

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
        addon_list = []
        others_list = []
        service_list = []
        for service in services:
            service = Services.objects.get(name=service)
            details = json.loads(service.details) 
            
            if details.get('is_service') != None:
                if details['is_service'] == True:
                    service_list.append(service.id)
                    package = Packages.objects.filter(service_ids__contains=service.id)
                    package_list.extend(package)
                    
            elif details.get('is_addon') != None:
                if details['is_addon'] == True:
                    addon_list.append(service)
            else:
                others_list.append(service)
                
        package_list = Counter(package_list).most_common(1)
        total_price = 0
        for addon in addon_list:
            total_price += addon.price
        if len(package_list) != 0:
            total_price += package_list[0][0].price
            package_list = package_list[0][0]
        else:
            package_list = []
        context = {'package_list': package_list, 'addon_list': addon_list, 'others_list': others_list, 'total_price': total_price}
        return render(request, 'package/package_suggestion.html', context)

    context = {'service_list': service_list}
    return render(request, 'package/home.html', context)
