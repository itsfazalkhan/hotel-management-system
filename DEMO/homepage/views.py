import calendar
import time

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from . import models
from DEMO import settings
from datetime import datetime, date
import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="root", passwd="123456", database="hotel")
mycursor = mydb.cursor()


# Create your views here.
def home(request):
    return render(request, 'homepage/index.html')


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username):
            messages.error(request, 'Username already exist! Please try some other username')
            return redirect('/signup')

        if User.objects.filter(email=email):
            messages.error(request, 'Email already registered!')
            return redirect('/signup')

        if len(username) > 10:
            messages.error(request, 'Username must be under 10 characters')

        if pass1 != pass2:
            messages.error(request, "Passwords didn't match!")

        if not username.isalnum():
            messages.error(request, 'Username must be Alpha-Numeric')
            return redirect('/signup')

        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.is_active = False
        myuser.save()

        messages.success(request,
                         "Your Account has been successfully created. We have sent you an email, please confirm your email inorder to activate your account")

        # Welcome Email

        subject = "Welcome to Beach-view"
        message = "Hello " + myuser.first_name + "!!\n" + "Your account has been successfully created.\n\nThank you for joining us!"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        # Email Address Confirmation

        current_site = get_current_site(request)
        emai_subject = "Confirm your email at Beach-view"
        message2 = render_to_string('email_confirmation.html', {
            'name': myuser.first_name,
            'doamin': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)
        })
        email = EmailMessage(
            emai_subject,
            message2,
            settings.EMAIL_HOST_USER,
            [myuser.email]
        )
        email.fail_silently = True
        email.send()

        return redirect('/signup')

    return render(request, "homepage/signup.html")


def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request, 'homepage/index.html', {'fname': fname})

        else:
            messages.error(request, 'Bad Credentials!')
            return redirect('signin')

    return render(request, 'homepage/signin.html')


def activate(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        myuser = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        myuser = None

    if myuser is not None and generate_token.check_token(myuser, token):
        myuser.is_active = True
        myuser.save()
        login(request, myuser)
        return redirect("/booking")
    else:
        return render(request, 'activation_failed.html')


def signout(request):
    logout(request)
    messages.success(request, 'Logged Out successfully')
    return redirect('/index')


def index(request):
    return render(request, 'homepage/index.html')


def booking(request):
    e = 0
    d = 0
    dp = 0
    s = 0
    i = 0
    room_id = 0

    stay = 0
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("SELECT count(*) FROM economy_available;")
    eavail = mycursor.fetchone()
    for i in eavail:
        e += int(i)
    mycursor.execute("SELECT count(*) FROM deluxe_available")
    davail = mycursor.fetchone()
    for i in davail:
        d += int(i)
    if (e >= d):
        dp += d
    if (e <= d):
        dp += e
    mycursor.execute("SELECT count(*) FROM suite_available")
    savail = mycursor.fetchone()
    for i in savail:
        s += int(i)
    if request.method == "POST":

        fname = request.POST['fname']
        lname = request.POST['lname']
        phone = request.POST['phone']
        email = request.POST['email']
        enum = request.POST['enum']
        dnum = request.POST['dnum']
        dpnum = request.POST['dpnum']
        snum = request.POST['snum']
        check_in = datetime.strptime(request.POST['check_in'], "%Y-%m-%d")
        check_out = datetime.strptime(request.POST['check_out'], "%Y-%m-%d")
        res_date = datetime.strftime(date.today(), "%Y-%m-%d")
        stay = check_out - check_in

        if check_out > check_in:
            x = "INSERT INTO cust_info(fname,lname,email,phone,status) VALUES(%s,%s,%s,%s,%s);"
            mycursor.execute(x, [fname, lname, email, phone, 'Booked'])
            mydb.commit()
            mycursor.execute("Select * from cust_id ;")
            r = mycursor.fetchall()
            cust_id = r[-1]
            x = ''.join(map(str, cust_id))
            cust_id = int(x)
            res_id = cust_id * 2 + 3

            if not enum == '':
                mycursor.execute("SELECT * FROM economy_available;")
                y = mycursor.fetchmany(size=int(enum))
                for room_id in y:
                    z = int(''.join(map(str, room_id)))
                    t = (cust_id, res_id, z, stay.days, check_in, check_out, res_date)
                    sql = "Insert into reservation(cust_id,reservation_id,room_id,stay,check_in,check_out,res_date)values(%s,%s,%s,'%s','%s','%s','%s')" % t
                    mycursor.execute(sql)
                    sql = "Update room_info set status='Booked' where room_id=%s;"
                    mycursor.execute(sql, [z])
                    res_id += 1
                    mydb.commit()

            if not dnum == '':
                mycursor.execute("SELECT * FROM deluxe_available;")
                y = mycursor.fetchmany(size=int(dnum))
                for room_id in y:
                    z = int(''.join(map(str, room_id)))
                    t = (cust_id, res_id, z, stay.days, check_in, check_out, res_date)
                    sql = "Insert into reservation(cust_id,reservation_id,room_id,stay,check_in,check_out,res_date)values(%s,%s,%s,'%s','%s','%s','%s')" % t
                    mycursor.execute(sql)
                    sql = "Update room_info set status='Booked' where room_id=%s;"
                    mycursor.execute(sql, [z])
                    res_id += 1
                    mydb.commit()

            if not dpnum == '':
                mycursor.execute("SELECT * FROM deluxe_available;")
                y = mycursor.fetchmany(size=int(dpnum))
                mycursor.execute("SELECT * FROM economy_available;")
                q = mycursor.fetchmany(size=int(dpnum))
                for room_id in y + q:
                    z = int(''.join(map(str, room_id)))
                    t = (cust_id, res_id, z, stay.days, check_in, check_out, res_date)
                    sql = "Insert into reservation(cust_id,reservation_id,room_id,stay,check_in,check_out,res_date)values(%s,%s,%s,'%s','%s','%s','%s')" % t
                    mycursor.execute(sql)
                    sql = "Update room_info set status='Booked' where room_id=%s;"
                    mycursor.execute(sql, [z])
                    res_id += 1
                    mydb.commit()

            if not snum == '':
                mycursor.execute("SELECT * FROM suite_available;")
                y = mycursor.fetchmany(size=int(snum))
                for room_id in y:
                    z = int(''.join(map(str, room_id)))
                    t = (cust_id, res_id, z, stay.days, check_in, check_out, res_date)
                    sql = "Insert into reservation(cust_id,reservation_id,room_id,stay,check_in,check_out,res_date)values(%s,%s,%s,'%s','%s','%s','%s')" % t
                    mycursor.execute(sql)
                    sql = "Update room_info set status='Booked' where room_id=%s;"
                    mycursor.execute(sql, [z])
                    res_id += 1
                    mydb.commit()
            cust_id += 1
            return redirect("/review")

    return render(request, 'homepage/booking.html', {'e': e, 'd': d, 'dp': dp, 's': s})


def check(request):
    a = 0;
    b = 0;
    c = 0;
    d = 0
    total = 0
    if request.method == "POST":
        enum = request.POST['enum']
        dnum = request.POST['dnum']
        dpnum = request.POST['dpnum']
        snum = request.POST['snum']
        check_in = datetime.strptime(request.POST['check_in'], "%Y-%m-%d")
        check_out = datetime.strptime(request.POST['check_out'], "%Y-%m-%d")
        stay = check_out - check_in
        if check_out > check_in:
            mycursor.execute("SELECT price FROM room_class where class_id = 1;")
            eprice = mycursor.fetchone()
            for i in eprice:
                a += int(i)
            mycursor.execute('SELECT price FROM room_class where class_id = 2;')
            dprice = mycursor.fetchone()
            for i in dprice:
                b += int(i)
            mycursor.execute('SELECT price FROM room_class where class_id = 3;')
            dpprice = mycursor.fetchone()
            for i in dpprice:
                c += int(i)
            mycursor.execute('SELECT price FROM room_class where class_id = 4;')
            sprice = mycursor.fetchone()
            for i in sprice:
                d += int(i)
            total = ((a * int(enum)) + (b * int(dnum)) + (c * int(dpnum)) + (d * int(snum))) * stay.days
        else:
            total = 'Date-Error'
    return render(request, 'homepage/check.html', {"total": total})


def cancel():
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("SELECT * FROM CUST_ID;")
    r = mycursor.fetchall()
    cid = ''.join(map(str, r[-1]))
    mycursor.execute("SELECT room_id FROM RESERVATION WHERE CUST_ID=%s;", [cid])
    rooms = mycursor.fetchall()
    for room in rooms:
        room = ''.join(map(str, rooms))
        mycursor.execute("UPDATE room_info SET  STATUS='Available' WHERE room_id=%s;", [cid])
    mycursor.execute("UPDATE CUST_INFO SET  STATUS='Cancelled' WHERE CUST_ID=%s;", [cid])
    mycursor.execute("DELETE FROM reservation WHERE CUST_ID=%s;", [cid])
    mycursor.execute("UPDATE room_info SET  STATUS='Available' WHERE room_id=%s;", [cid])
    mydb.commit()


def review(request):
    mycursor = mydb.cursor(buffered=True)
    mycursor.execute("SELECT * FROM CUST_ID;")
    r = mycursor.fetchall()
    cid = ''.join(map(str, r[-1]))
    mycursor.execute("SELECT * FROM CUST_INFO where cust_id=%s;", [cid])
    cust_info = mycursor.fetchone()

    (cust_id, fname, lname, email, status, phone) = cust_info
    mycursor.execute("SELECT room_id FROM reservation where cust_id=%s;", [cust_id])
    rooms = mycursor.fetchall()
    for room in rooms:
        room = ''.join(map(str, rooms))
    mycursor.execute("SELECT check_in,check_out FROM reservation where cust_id=%s;", [cust_id])
    a = mycursor.fetchone()
    (check_in, check_out) = a
    check_in = datetime.strftime(check_in, "%d-%m-%Y")
    check_out = datetime.strftime(check_out, "%d-%m-%Y")
    mycursor.execute("SELECT status FROM cust_info where cust_id=%s;", [cust_id])
    b = mycursor.fetchone()
    (status) = b
    status = ''.join(map(str, status))
    if request.method == "POST":
        cancel()

    return render(request, 'homepage/review.html',
                  {"cust_id": cust_id, "fname": fname, "lname": lname, "email": email, "status": status, "phone": phone,
                   "room": room, "check_in": check_in, "check_out": check_out})
