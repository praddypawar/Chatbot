from django.shortcuts import render,redirect
from datetime import datetime
from django.contrib import messages
from appclient.models import ClientRegistration,ChatbotRegister
import json
# Create your views here.
def index(request):
    if "email" not in request.session and "type" not in request.session:
        messages.error(request, "Login first")
        return redirect("sign-in")
    if request.session["type"] != "admin":
        messages.error(request, "User not allow")
        return redirect("sign-in")

    client_data = ClientRegistration.objects.all()

    context = {
        "footer": {"url": "https://colorlib.com", 
        "name": "cloud4code", 
        "year": datetime.now().year, 
        "extra_name": "chatbot"},
        "total_client":client_data.count(),
        "client_data":client_data,
        "title":"Admin-Dashboard"
        }

    return render(request, "admin_temp/index.html", context)




def clientview(request):
    if "email" not in request.session and "type" not in request.session:
        messages.error(request, "Login first")
        return redirect("sign-in")
    if request.session["type"] != "admin":
        messages.error(request, "User not allow")
        return redirect("sign-in")

    client_data = ClientRegistration.objects.all()

    context = {
        "footer": {"url": "https://colorlib.com", 
        "name": "cloud4code", 
        "year": datetime.now().year, 
        "extra_name": "chatbot"},
        "client_data":client_data,
        "title":"Admin-Client-view"
        }

    return render(request, "admin_temp/client_view.html", context)



def clientadd(request, pk=0):
    if "email" not in request.session and "type" not in request.session:
        messages.error(request, "Login first")
        return redirect("sign-in")
    if request.session["type"] != "admin":
        messages.error(request, "User not allow")
        return redirect("sign-in")
        
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        designation = request.POST.get("designation")
        password = request.POST.get("password")
        print(fname, lname, email, mobile, designation, password)
        if pk == 0:
            if ClientRegistration.objects.filter(email=email).count() > 0 or ClientRegistration.objects.filter(mobile=mobile).count() > 0:
                messages.warning(request, "Please Check email and number..")
                return redirect("appadmins:clientadd")
            ClientRegistration(fname=fname, lname=lname, email=email, mobile=mobile, designation=designation, password=password).save()

            messages.success(request, "Data added succesfully!")
            return redirect("appadmins:clientadd")
        else:
            update_data = ClientRegistration.objects.get(pk=pk)
            if (ClientRegistration.objects.filter(email=email).count() > 0 or ClientRegistration.objects.filter(mobile=mobile).count() > 0) and (update_data.email != email or update_data.mobile != mobile):
                messages.warning(request, "Please Check email and number..")
                return redirect("appadmins:clientupdate", pk)
            update_data.fname = fname
            update_data.lname = lname
            update_data.email = email
            update_data.mobile = mobile
            update_data.designation = designation
            update_data.password = password
            update_data.save()
            messages.success(request, "Data updated succesfully!")
            return redirect("appadmins:clientview")
    context = {"footer": {"url": "https://colorlib.com", "name": "cloud4code", "year": datetime.now().year, "extra_name": "chatbot"}, "title": "Admin-Client-add"}

    if pk > 0:
        context["client_data"] = ClientRegistration.objects.get(pk=pk)
    return render(request, "admin_temp/client_add.html", context)


def clientdelete(request,pk=0):
    if "email" not in request.session and "type" not in request.session:
        messages.error(request, "Login first")
        return redirect("sign-in")
    if request.session["type"] != "admin":
        messages.error(request, "User not allow")
        return redirect("sign-in")
    if pk!=0:
        ClientRegistration.objects.get(pk=pk).delete()
        messages.success(request,"Data Delete succesfully!")
        return redirect("appadmins:clientview")


def bot_builder(request):
    if "email" not in request.session and "type" not in request.session:
        messages.error(request, "Login first")
        return redirect("sign-in")
    if request.session["type"] != "admin":
        messages.error(request, "User not allow")
        return redirect("sign-in")
    # D:\Chatbot\CHATBOT\clientdb\demo.json
    with open(r"D:\Chatbot\CHATBOT\clientdb\demo.json","r") as rdata:
        data = json.load(rdata)
    # print(data)
    if request.method == "POST":
        try:

            if "all_data_submit" in request.POST:
                botname= request.POST.get("botname")
                bottype= request.POST.get("bottype")
                botlogo= request.FILES.get("botlogo")

                # _chatbotregister = ChatbotRegister(client_id=_register_data,chatbot_name=bot_name,category=bot_type,logo=bot_logo)
                # _chatbotregister.save()
                print("----------------pokkoko",botname,bottype,botlogo)
            else:

                tag = request.POST.get("tag")
                patterns = request.POST.getlist("patterns[]")
                print("tag: ",tag)
                print("patterns: ",patterns)


                btnlabel = request.POST.getlist("btnlabel[]")
                btnname = request.POST.getlist("btnname[]")
                btntheme = request.POST.getlist("btntheme[]")
                restype = request.POST.getlist("restype[]")
                
                red_data = {
                    "tag":str(tag).lower(),
                    "patterns":patterns,
                    "responses":[]
                }
                res_data = ''
                # print(restype,"-----------")
                for i in range(len(restype)):
                    print("i:",i)
                    
                    if restype[i] == "btn":
                        print("btnlabel: ",btnlabel[i])
                        print("btnname: ",btnname[i])
                        print("btntheme: ",btntheme[i])

                        res_data += f"""<div class=\"container text-start\"><div class=\"row justify-content-start form-input-wrap\"><div class=\"col-lg-12\"><button type=\"button\" id=\"dynamicbtn\" onClick=\"GFG_click(this.value)\" value=\"{btnlabel[i]}\" class=\"btn form-input\">{btnlabel[i]}</button></div></div></div>"""

                    if restype[i] == "lbl":
                        print("lbllabel: ",btnlabel[i])
                        print("lblname: ",btnname[i])
                        print("lbltheme: ",btntheme[i])
                        res_data += f"""<div class=\"text-area-wrap\"><div class=\"row\"> <div class=\"col-lg-12\"> <p class=\"bot-chat botside-message\" id=\"bot-msg\">{btnlabel[i]}</p></div> </div></div>"""
                    
                    if restype[i] == "lnk":
                        print("lnklabel: ",btnlabel[i])
                        print("lnkname: ",btnname[i])
                        print("lnktheme: ",btntheme[i])

                red_data["responses"].append(res_data)
                print(red_data,"---------------------------")
                data["intents"].append(red_data)

                with open(r"D:\Chatbot\CHATBOT\clientdb\demo.json","w") as wdata:
                    json.dump(data,wdata,indent=4)

                return render(request,"admin_temp/ajaxforbuilderjson.html",{"data":json.dumps(data, indent=4)})

            
        except Exception as e:
            print(e)      


    context = {"footer": {"url": "https://colorlib.com", "name": "cloud4code", "year": datetime.now().year, "extra_name": "chatbot"}, "title": "Admin-Client-add"}
    return render(request,"admin_temp/builder.html",context)


