from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.views import View


# Create your views here.

# --------- CLASS BASED VIEW --------------

class Signup(View):
    def get(self,request):
        user = request.session.get('Username')
        if user is not None:
            return redirect('shop')
        else:
            return render(request,'user/signup.html')
        
    
    def post(self,request):
        Username = request.POST.get('Username')
        Email = request.POST.get('Email')
        Password = request.POST.get('Password')
        Password2 = request.POST.get('Password2')
        my_user = User.objects.create_user(Username,Email,Password)
        my_user.save()
        return redirect('login')
        # if user is login:
        #     return redirect('shop')
       
        

# ------- FUNCTION BASED VIEW ------------

# def signup(request):
#     if request.method == 'POST':
#         Username = request.POST.get('Username')
#         Email = request.POST.get('Email')
#         Password = request.POST.get('Password')
#         Password2 = request.POST.get('Password2')
#         my_user = User.objects.create_user(Username,Email,Password)
#         my_user.save()
#         return redirect('login')
#     return render(request,'user/signup.html')

def login_user(request):
    if request.method == 'POST':
        Username = request.POST.get('Username')
        Password = request.POST.get('Password')
        user = authenticate(request,username = Username,password = Password)
        print(user)
        if user is not None:
            request.session['Username']= Username
            login(request,user)
            print(request.session.get('Username'))
            print(user)
            return redirect('shop')
        else:
            return HttpResponse("Invalid username or password")

    return render(request,'user/login.html')

def logout_user(request):
    logout(request)
    return redirect('login')

    