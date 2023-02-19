from django.shortcuts import render,redirect
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
# Create your views here.

def registerView(request):
    form = CustomUserCreationForm()
    if request.POST:
        form = CustomUserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, form.errors.as_text())
   
    return render(request, 'home.html', {
        'form': form,
    })


def loginView(request):
    form = AuthenticationForm()
    errors = ''
    if request.POST:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            username = data['username']
            password = data['password']
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.info(request, 'Welcome Back {}!!'.format(
                user.get_username().title()))
            next = request.POST.get('next')
            if next:
                return redirect(next)
            return redirect('/')
        else:
            errorList = form.errors.get_json_data(
                escape_html=True).get('__all__')
            for error in errorList:
                errors += error['message'] + '<br>'
            form = AuthenticationForm()
            return render(request, 'login.html', {
        'form': form,
    })