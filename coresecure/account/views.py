from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.
def login(request):
    if request.method == 'POST':
        username = request.POST['email']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request, 'invalid Credentials')
            return redirect('login')

    else:
        return render(request, 'login.html')


def register(request):
    try:
        if request.method == 'POST':
            first_name = request.POST['first_name']
            username = request.POST['email']
            email = username
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 == password2:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Username or Email Taken')
                    return redirect('/accounts/register')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Email Taken')
                    return redirect('/accounts/register')
                else:
                    user = User.objects.create_user(first_name=first_name, username=username,
                                                    password=password1, email=email)
                    user.save()
                    print('user created')
                    messages.info(request, 'Account Successively created. Now login to proceed')
                    return redirect('/accounts/login')
            else:
                print("Password Not matching")
                messages.info(request, 'Password Not matching...')
                return redirect('/accounts/register')

            return redirect('/')
        else:
            return render(request, 'register.html')
    finally:
        pass


def logout(request):
    auth.logout(request)
    messages.info(request, 'Logged out successively')
    return redirect('/')
