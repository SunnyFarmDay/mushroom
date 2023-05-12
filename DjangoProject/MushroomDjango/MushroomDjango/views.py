from django.shortcuts import render
from django.contrib.auth import authenticate, login as log_in, logout as log_out
from .forms import LoginForm
from django.contrib import messages
from django.shortcuts import redirect

def login(request):
    context = {}
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            clean = form.cleaned_data
            username = clean['username']
            password = clean['password']
            user = authenticate(request, username = username, password = password)
            if user:
                log_in(request, user)
                messages.success(request, f"Welcome {user.get_username()}")
                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('SalaryInput:home')
                    
            else:
                messages.error(request, "Incorrect username or password!")
        else:
            messages.success(request, "Input Format Error!")
        context['login_form'] = form


    else:   
        context['login_form'] = LoginForm()
    return render(request, 'Login.html', context)

def logout(request):
    log_out(request)
    messages.info(request, 'You have logged out.')
    return redirect('login')