from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from blog.models import MyUser


def sign_in_view(request):
    d = {}
    if request.method == "POST":
        data = request.POST
        username = data['username']
        password = data['password']

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            d['error'] = 'User not found'

    return render(request, 'signin.html', context=d)


def sign_up_view(request):
    d = {}
    if request.method == "POST":
        data = request.POST

        firstname = data["firstname"]
        lastname = data["lastname"]
        username = data['username']

        p1 = data["password1"]
        p2 = data["password2"]

        if not User.objects.filter(username=username).exists() and p1 == p2:
            user = User.objects.create(username=username, password=make_password(p1))
            user.save()
            my_user = MyUser.objects.create(user=user)
            my_user.save()
            return redirect('/auth/signin')
        d['error'] = 'User is already exist or password is not same'
    return render(request, 'signup.html')


@login_required(login_url='/signin')
def logout_view(request):
    logout(request)
    return redirect('/auth/signin')


@login_required(login_url='/signin')
def setting_view(request):
    user = User.objects.filter(id=request.user.id).first()
    my_user = MyUser.objects.filter(user=request.user).first()
    d = {
        "user": user,
        "my_user": my_user,
    }
    if request.method == "POST":
        data = request.POST
        firstname = data['firstname']
        lastname = data['lastname']
        email = data['email']
        about = data['about']
        relationship = data['relationship']
        location = data['location']
        working_at = data['working_at']

        user.first_name = firstname
        user.last_name = lastname
        user.email = email
        user.save(update_fields=['first_name', 'last_name', 'email'])

        my_user.about_me = about
        my_user.relationship = relationship
        my_user.location = location
        my_user.working_at = working_at
        my_user.save(update_fields=['about_me', 'relationship', 'location', 'working_at'])

        return redirect('/auth/settings', context=d)

    return render(request, 'setting.html', context=d)
