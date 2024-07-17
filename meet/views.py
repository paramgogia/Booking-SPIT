import json
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import aTimeSlot, FreeSlot
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from datetime import datetime
from django.urls import reverse
from django.db.models import F
import xlsxwriter

# Create your views here.
def index(request):
    #list of times from 9am to 9pm in intervals of 30 mins
    times = ["09.00 am", "09.30 am","10.00 am", "10.30 am", "11.00 am", "11.30 am", "12.00 pm", "12.30 pm", "01.00 pm", "01.30 pm", "02.00 pm", "02.30 pm","03.00 pm", "03.30 pm","04.00 pm", "04.30 pm","05.00 pm", "05.30 pm","06.00 pm", "06.30 pm","07.00 pm", "07.30 pm","08.00 pm", "08.30 pm"]
    date = datetime.now().strftime("%Y-%m-%d")
    status = 0
    user = request.user
    if user.is_authenticated:
        status = FreeSlot.objects.get(email = user.email).lock
    if request.method=="POST":
        if 'form1' in request.POST:
            date = request.POST.get("dateinput")
            print(date)
        elif 'form2' in request.POST:
            user = request.user
            if not user.is_authenticated:
                return redirect("login")
            selected_ids = request.POST.get('selected_ids')
            if selected_ids=="":
                return redirect('index')
            l = selected_ids.split(",")
            room = 0
            date = request.POST.get('dateinput')
            name = request.POST.get('name')
            month = request.POST.get('month')
            year = request.POST.get('year')
            reason = request.POST.get('reason')
            u = FreeSlot.objects.get(email = user.email)
            print(u)
            for i in l:
                j = i.split("-")
                slot = j[1]
                room = int(j[2])
                print(slot, room, date)
                b= aTimeSlot.objects.filter(slot=slot, room = room, date = date)
                if b:
                    continue
                else:
                    x = aTimeSlot.objects.create(slot=slot, room = room, date = date, name = name, email = user.email, month = month, year = year, reason = reason)
                    u.free_slots += 0.5
                    x.save()
                    u.save()
            if u.free_slots > u.total:
                u.lock = 1
                u.save()
        elif 'form4' in request.POST:
            date = request.POST.get("dateinput")
    timeslots = aTimeSlot.objects.filter(date = date)
    num = range(24)
    r = range(3)
    return render(request, 'index.html', {'timeslots':timeslots, 'num':num, 'r': r, 'date': date, 'times': times, 'status':status})

def delete_slot(request):
    times = ["09.00 am", "09.30 am","10.00 am", "10.30 am", "11.00 am", "11.30 am", "12.00 pm", "12.30 pm", "01.00 pm", "01.30 pm", "02.00 pm", "02.30 pm","03.00 pm", "03.30 pm","04.00 pm", "04.30 pm","05.00 pm", "05.30 pm","06.00 pm", "06.30 pm","07.00 pm", "07.30 pm","08.00 pm", "08.30 pm"]
    date = datetime.now().strftime("%Y-%m-%d")
    if request.method=="POST":
        if 'form1' in request.POST:
            date = request.POST.get("dateinput")
            print(date)
        elif 'form2' in request.POST:
            user = request.user
            if not user.is_authenticated:
                return redirect("login")
            selected_ids = request.POST.get('selected_ids')
            if selected_ids=="":
                return redirect('index')
            l = selected_ids.split(",")
            room = 0
            date = request.POST.get('dateinput')
            u = FreeSlot.objects.get(email = user.email)
            for i in l:
                j = i.split("-")
                slot = j[1]
                room = int(j[2])
                a = aTimeSlot.objects.filter(slot=slot, room = room, date = date)
                a.delete()
                u.free_slots += 0.5
                u.charges = u.free_slots * -300 if u.free_slots < 0 else 0
    timeslots = aTimeSlot.objects.filter(date = date)
    num = range(24)
    r = range(3)
    return render(request, 'deletecal.html', {'timeslots':timeslots, 'num':num, 'r': r, 'date': date, 'times': times})

def profile(request):
    mon = datetime.now().strftime("%Y-%m-%d").split("-")[1]
    y = datetime.now().strftime("%Y-%m-%d").split("-")[0]
    objs = FreeSlot.objects.all()
    for o in objs:
        o.free_slots = aTimeSlot.objects.filter(email = o.email, month = mon, year = y).count()*0.5
        o.charges = 0 if o.free_slots < o.total else (o.free_slots - o.total) * 300
        o.save()
    if request.method == "POST":
        if 'form1' in request.POST:
            email = request.POST.get("email")
            return redirect(reverse('edit_user') + f'?email={email}')
        elif 'form2' in request.POST:
            return redirect('change_password')
        elif 'form4' in request.POST:
            email = request.POST.get("email")
            u = FreeSlot.objects.get(email = email)
            u.lock = int(request.POST.get("lock"))
            u.save()
    user = request.user
    free_hours = FreeSlot.objects.get(email = user.email).free_slots
    charges = FreeSlot.objects.get(email = user.email).charges
    total = FreeSlot.objects.get(email = user.email).total
    objs = FreeSlot.objects.all()
    date = datetime.now().strftime("%Y-%m-%d")
    month = date.split("-")[1]
    year = date.split("-")[0]
    if month == "01":
        previous_month = "12"
        previous_year = str(int(year) - 1)  # Subtract 1 from the year for January
    else:
        previous_month = str(int(month) - 1).zfill(2)
        previous_year = year
    print(month, year)
    timeslots_tm = aTimeSlot.objects.filter(email = user.email, month= month, year=year)
    timeslots = sorted(timeslots_tm, key=lambda obj:obj.date)
    timeslots_pm = aTimeSlot.objects.filter(email = user.email, month= previous_month, year=previous_year)
    timeslotspm = sorted(timeslots_pm, key=lambda obj:obj.date)
    if not user.is_authenticated:
        return redirect("login")
    return render(request, 'profile.html', {'timeslots':timeslots, 'timeslotspm':timeslotspm, 'free_hours' : free_hours, 'charges': charges , "objs":objs, 'total':total})

def edit_user(request):
    email = request.GET.get('email')
    u = FreeSlot.objects.get(email = email)
    x = u.total
    us = User.objects.get(email = email)
    if request.method=="POST":
        if 'form1' in request.POST:
            first_name = request.POST.get('first_name')
            last_name = ""
            email = request.POST.get("email")
            password = request.POST.get("password")
            free = request.POST.get("free")
            u.first_name = first_name
            u.last_name = last_name
            u.email = email
            u.total = free
            us.password = password
            u.save()
            us.first_name = first_name
            us.last_name = last_name
            us.email = email
            us.save()
            return redirect('profile')
        else:
            print('Hello')
            email = request.POST.get('email')
            us = User.objects.get(email =email)
            a = aTimeSlot.objects.filter(email = email)
            u = FreeSlot.objects.get(email = email)
            us.delete()
            u.delete()
            a.delete()
            return redirect('profile')
    return render(request, 'edituser.html', {'x':x, 'us':us})

def change_password(request):
    if request.method=="POST":
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        if password == confirmpassword:
            user = request.user
            user.password = password
            user.save()
            login(request, user)
            return redirect('profile')
        return render(request, 'changepassword.html')
    return render(request, 'changepassword.html')

def download_table_as_excel(request):
    objs = FreeSlot.objects.all()

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="Charges.xlsx"'

    workbook = xlsxwriter.Workbook(response, {'remove_timezone': True})
    worksheet = workbook.add_worksheet()

    # Write the table headers
    headers = ['First Name', 'Last Name', 'Email', 'Hours Used', 'Total Free Hours', 'Charges']
    for col, header in enumerate(headers):
        worksheet.write(0, col, header)

    # Write the table data
    for row, obj in enumerate(objs, start=1):
        data = [obj.first_name, obj.last_name, obj.email, obj.free_slots, obj.total, str(obj.charges)+'0']
        for col, value in enumerate(data):
            worksheet.write(row, col, value)

    workbook.close()

    return response


def loginuser(request):
    msg=""
    if request.method == "POST":
        msg="Wrong Credentials!"
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email = email)  
            if user is not None:
                if user.password == password:
                    print("Successful")
                    login(request, user)
                    return redirect("index")
                else:
                    return render(request, 'login.html', {'msg':msg})
        except User.DoesNotExist:
            return render(request, 'login.html', {'msg':msg})
        else:
            return render(request, 'login.html', {'msg':msg})
    else:
       return render(request, "login.html", {'msg':msg})
    
def logoutuser(request):
    logout(request)
    return redirect("index")

def adduser(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        first_name = request.POST.get('first_name')
        free_hours = request.POST.get('free')
        user = User.objects.create(email = email, password = password, first_name = first_name, username = first_name, last_name = "")
        obj = FreeSlot.objects.create(email = email, total=free_hours, free_slots = free_hours, charges = 0, first_name=first_name)
        user.save()
        obj.save()
        return redirect("adduser")
    else:
        return render(request, "adduser.html")