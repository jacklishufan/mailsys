from django.shortcuts import render, redirect
from django.http import HttpResponse
from login.models import UserTicket, User, LogInActivity
from django.core.mail import send_mail
from django.conf import settings
import hashlib
import random

# Create your views here.
def registration_view(request):
    #return HttpResponse("HELLOW WORD")
    if request.method == "POST":
        print(request.POST)
        data = request.POST
        usr_name = data['usr_input']
        tgt_mail = data['email_input']
        if usr_name =="":
            usr_name = tgt_mail
        new_ticket = UserTicket()
        new_ticket.name = data['usr_input']
        new_ticket.email = tgt_mail
        new_ticket.passwd = data['passwd_input']
        cid = random.randint(1000000,9999999)
        while UserTicket.objects.filter(hash_code=cid,expired=False).exists():
            cid = random.randint(1000000, 9999999)
        new_ticket.hash_code=cid
        new_ticket.save()
        info = request.build_absolute_uri("/registration_confirmation/{}/".format(str(cid)))
        content = 'Here is your registration link: '+info
        res=send_mail('注册确认 Reg Confirmation',
                    "这是您的链接："+content,
                  settings.DEFAULT_FROM_EMAIL,
                  [tgt_mail])
        print(res)

        data = {
            "header": "Success!",
            "desc": "An email containing confirmation link has been sent to address "+ new_ticket.email,
            "action": "/login",
            "action_desc": "log in"
        }
        return render(request, "info.html", data)

    return render(request,"reg.html")

def reg_confirm_view(request,reg_id=0):
    if UserTicket.objects.filter(hash_code=reg_id,expired=False).exists():
        confirmed_ticket = UserTicket.objects.get(hash_code=reg_id,expired=False)

        new_user = User()
        if User.objects.filter(email=confirmed_ticket.email).exists():
            data = {
                "header": "Error!",
                "desc": "Email address "+new_user.email + " has been registered.",
                "action": "/login",
                "action_desc": "log in"
            }
            return render(request, "info.html", data)
        if User.objects.filter(name=confirmed_ticket.name).exists():
            data = {
                "header": "Error!",
                "desc": "User "+new_user.name + " has been registered.",
                "action": "/login",
                "action_desc": "log in"
            }
            return render(request, "info.html", data)
        if confirmed_ticket.has_expired():
            data = {
                "header": "Error!",
                "desc": "Link Expiered",
                "action": "/login",
                "action_desc": "log in"
            }
            confirmed_ticket.expired = True
            confirmed_ticket.save()
            return render(request, "info.html", data)
        confirmed_ticket.expired = True
        confirmed_ticket.save()
        new_user.name = confirmed_ticket.name
        new_user.email = confirmed_ticket.email
        new_user.passwd = confirmed_ticket.passwd
        new_user.save()
        data = {
            "header": "Success!",
            "desc": new_user.name+", You have confirmed your registration",
            "action": "/login",
            "action_desc": "log in"
        }
        return render(request, "info.html", data)
    return HttpResponse(str(reg_id))

def login_view(request):

    if request.method == "POST":
        print(request.POST)
        data = request.POST
        username = data['usr_input']
        passwd = data['passwd_input']
        this_usr = validate(username,passwd,get_client_ip(request))
        if this_usr == 0:
            data = {
                "header": "Account Locked!",
                "desc": username + ", You have made too many wrong attempts, please wait for 10 minute",
                "action": "/login",
                "action_desc": "Back to log in"
            }
            return render(request, "info.html", data)
        if this_usr == -1:
            data = {
                "header": "Wrong Password!",
                "desc": "You have entered the wrong password, please try again",
                "action": "/login",
                "action_desc": "Back to log in"
            }
            return render(request, "info.html", data)
        if this_usr == -2:
            data = {
                "header": "User Not Found!",
                "desc": "You have entered a wrong username or email, please try again",
                "action": "/login",
                "action_desc": "Back to log in"
            }
            return render(request, "info.html", data)
        if this_usr:
            request.session['is_login'] = True
            request.session['user_id'] = this_usr.id
            request.session.set_expiry(600)
            data = {
                "header": "Success!",
                "desc": this_usr.name + ", You have logged in from IP:"+get_client_ip(request),
                "action": "/",
                "action_desc": "Go to HomePage"
            }
            return render(request, "info.html", data)


    return render(request,"login.html")

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def validate(username,passwd,ip):
    if User.objects.filter(email=username).exists():
        this_usr = User.objects.get(email=username)
        acc_log = LogInActivity(user=this_usr)
        if this_usr.locked:
            print("LOCKED")
            return 0
        if str(this_usr.passwd) == passwd:
            acc_log.success = True
            acc_log.save()
            return this_usr
        acc_log.success = False
        acc_log.save()
        return -1
    elif User.objects.filter(name=username).exists():
        this_usr = User.objects.get(name=username)
        acc_log = LogInActivity(user=this_usr)
        if this_usr.locked:
            print("LOCKED")
            return 0
        print(str(this_usr.passwd)==passwd)
        if str(this_usr.passwd) == passwd:
            acc_log.success = True
            acc_log.save()
            return this_usr
        acc_log.success = False
        acc_log.save()
        return -1
    return -2

def test(request):
    data = {
        "header":"Success!",
        "desc": "You have confirmed your registration",
        "action":"/login",
        "action_desc":"log in"

    }
    return render(request,"info.html",data)

def home(request):

    if request.session.get('is_login')==None:
        return redirect('/login')
    else:
        usr_id = request.session['user_id']
        user = User.objects.get(id = usr_id)
        data = {
            "header": "Welcome! "+user.name,
            "desc": user.name + ", You have logged in from"+get_client_ip(request),
            "action": "/logout/",
            "action_desc": "logout"
        }
        return render(request, "info.html", data)
def logout(request):
    request.session.flush()
    return redirect('/')
