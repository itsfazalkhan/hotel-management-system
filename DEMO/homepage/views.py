from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


# Create your views here.
def hi(request):
    return render(request,'homepage/homepage.html')

def signup(request):

    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        myuser = User.objects.create_user(username,email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname

        myuser.save()

        messages.success(request, "Your Account has been successfully created.")

        return redirect('signin')

    return render(request,"homepage/signup.html")

def signin(request):
    return render(request,"homepage/signin.html")

def signout(request):
    pass