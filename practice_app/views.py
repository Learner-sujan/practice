from django.shortcuts import render, redirect
from django.urls import reverse
from .models import record
from .forms import uploadForm, loginForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate , login, logout
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime

x = datetime.datetime.now() 
day = x.day
month = x.month
year = x.year

# Create your views here.

def userLogin(request):
    Form = loginForm()
    return render(request, 'login.html', { 'loginForm': Form })

def loginAttempt(request):    
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        login(request, user)
        print('Login Success')
        response = redirect('home')
        response.set_cookie('cookie_username', username)
        return response
    else:
        print('Login Error')
        return redirect('login')


def userLogout(request):
    try:
        logout(request)
        print('Logout Success')
        return redirect('index')
    except:
        print('Logout consist error')

def index(request):
    return render(request,'index.html')

def home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        records_dict = record.objects.all()
        paginator = Paginator(records_dict, 5)
        page = request.GET.get('page',1)
        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
    
        cookie_username = request.COOKIES['cookie_username']
        date = " Today is : {} {}, {} ".format(x.strftime('%d'),x.strftime('%B'),x.strftime('%Y'))
        return render(request, 'home.html', {'date':date , 'posts':posts, 'page':page, 'cookie_username':cookie_username})

def add(request):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            name = request.POST['name']
            address = request.POST['address']
            phone = request.POST['phone']
            dob = request.POST['dob']
            photo = request.FILES['photo']

            print(photo)
            if name=='' or name==None and address=='' or address==None and phone=='' or phone==None and dob=='' or dob==None:
                error = "Field can't be empty"
                return render(request,'home.html', {'errorMsg':error})
            else:
                if photo == '' or photo == None:
                    save_object = record(Name=name, Address=address, Phone=phone, Dob=dob)
                    save_object.save()
                else:
                    handle_uploaded_file(photo)
                    save_object = record(Name=name, Address=address, Phone=phone, Dob=dob, Profile=photo)
                    save_object.save()
                return redirect('home')
    
        return render(request, 'add.html')

def edit(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        Record = record.objects.get(Uid=id)
        localDateFormat = Record.Dob.strftime("%m/%d/%Y")
        return render(request,'edit.html', {'editRecord':Record, 'localDateFormat':localDateFormat})

def update(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        updateRecord = record.objects.filter(Uid=id)
        if request.method == 'POST':
            updateRecord.delete()
            name = request.POST['name']
            address = request.POST['address']
            phone = request.POST['phone']
            dob = request.POST.get('dob')

            if name=='' or name==None:
                print('Name Field empty')
            elif address=='' or address==None:
                print('Address field empty')
            elif phone=='' or phone==None:
                print('Phone field empty')
            elif dob=='' or dob==None:
                print('Date of Birth field empty')
            else:
                save_object = record(Name=name, Address=address, Phone=phone, Dob=dob)
                save_object.save()
                return redirect('home')
        return render(request,'edit.html')

def delete(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        delrecord = record.objects.get(Uid=id)
        delrecord.delete()
        return redirect('home')


def details(request, id):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        detail = record.objects.filter(Uid=id)
        for i in detail:
            name = i.Name
            dob = i.Dob
            id = i.Uid
        print(id)
        print('Fetched DOB: ',dob)
        print(type(dob.year))
        byear = int(dob.strftime("%Y"))
        bmonth = int(dob.strftime("%m"))
        bdate = int(dob.strftime("%d"))
        calculateAge(day, month, year, bdate, bmonth, byear)
        print(calculated_date, calculated_month, calculated_year)

        form = uploadForm()
        return render(request,'details.html', {'NAME':name, 'detail':detail, 'year': calculated_year , 'month': calculated_month , 'day': calculated_date,'id':id, 'form':form})

def profile(request,id):
    if not request.user.is_authenticated:
        return redirect('login')
    else:
        if request.method == 'POST':
            pp = uploadForm(request.POST, request.FILES)
            if pp.is_valid():
                a = record.objects.get(Uid=id)
                a.Profile = pp.cleaned_data['Profile']
                a.save()
                print(a.Profile)
                print('Success')
# Uploading image by updating Models Field
                handle_uploaded_file(request.FILES['Profile'])
                return redirect('home')
            else:
                print('Invalid')
        else:
            print('Not a POST METHOD')
        return render(request,'details.html')


def handle_uploaded_file(f):
    with open('static/upload/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

# Function to calculate age, month and day

def calculateAge(current_date, current_month, current_year, birth_date, birth_month, birth_year):
    month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31 ]
    # if birth date is greater then current birth_month 
    # then donot count this month and add 30 to the date so 
    # as to subtract the date and get the remaining days 
    if (birth_date>current_date):
        current_month = current_month - 1
        current_date = current_date + month[birth_month-1]

    # if birth month exceeds current month, then 
    # donot count this year and add 12 to the 
    # month so that we can subtract and find out 
    # the difference  
    if (birth_month>current_month):
        current_year = current_year - 1
        current_month = current_month + 12
    
    global calculated_date, calculated_month, calculated_year

    # calculate date, month, year 
    calculated_date = int(current_date - birth_date)
    calculated_month = int(current_month - birth_month)
    calculated_year = int(current_year - birth_year)
    
    # print present age 
    print("Present Age")
    print("Years:", calculated_year, "Months:",calculated_month, "Days:", calculated_date) 




# used to find age only
def calculate_age(byear, bmonth, bdate):
    
    print(type(day),type(month),type(year))
    print(type(bdate),type(bmonth),type(byear))

    age = year - byear - ((month, day) < (bmonth, bdate))
    return age