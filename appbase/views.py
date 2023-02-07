
from django.shortcuts import render,redirect
import ast
from django.contrib import messages

from appclient.models import ClientRegistration

def index(request):
    return render(request,"index.html")

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print("email: ", email, "password: ", password)
        if email == "admin@admin.com" and password == "123":
            print("adminnnnnnnn")
            # messages.success(request,"Admin login succesfully!")
            request.session["email"] = email
            request.session["type"]="admin"
            return redirect("appadmins:index")
            
        else:
            if data :=ClientRegistration.objects.filter(email=email,password=password):
                print(data[0].email,data[0].password,"================")
                request.session["email"] = email
                request.session["id"] = data[0].pk
                request.session["type"]="client"
                return redirect("appclient:index")
            else:
                messages.error(request, "Wrong credentials, Please try again!")
                return redirect("sign-in")
    context = {"title": "CBMS : sign-in"}
    return render(request, "login.html", context)

def register(request):

    if request.method == "POST":
        fname = request.POST.get("fname")
        lname= request.POST.get("lname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        designation = request.POST.get("designation")
        password = request.POST.get("password")

        print(fname,lname,email,mobile,designation,password)
        if ClientRegistration.objects.filter(email=email).count() == 0 and ClientRegistration.objects.filter(mobile=mobile).count() == 0:
            ClientRegistration(fname=fname,lname=lname,email=email,mobile=mobile,designation=designation,password=password).save()
            messages.success(request,"Your registration succesfully done!")
            return redirect("sign-in")
        else:
            messages.warning(request,"Please Check your email and number..")
            return redirect("sign-up")
    context = {
        "title":"CBMS : sign-up"
    }
    # messages.success(request,"Your registration succesfully done!")
    return render(request,"register.html",context)
    
def logout(request):
    if "id" in request.session:
        del request.session["id"]
    
    if "email" in request.session:
        del request.session["email"]

    if "type" in request.session:
        del request.session["type"]

    return redirect("sign-in")