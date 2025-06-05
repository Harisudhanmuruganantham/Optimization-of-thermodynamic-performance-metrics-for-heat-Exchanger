

# Create your views here.
from django.shortcuts import render,redirect
from admin_panel.models import Brine
from django.contrib import messages
from admin_panel.models import ResidentialDetails
# Create your views here.


# Create your views here.
def ht_register(request):
    if request.method == "POST":
        username = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        employee_module = request.POST.get("module")

        # Check if the email address ends with @gmail.com
        if not email.endswith('@gmail.com'):
            messages.error(request, "Only Gmail addresses are allowed.")
            return render(request, 'heat_testing/register.html')

        # Check if the email is unique
        if Brine.objects.filter(email=email).exists():
            messages.error(request, "This email address is already registered.")
            return render(request, 'heat_testing/register.html')

        # Save the new registration
        obj = Brine(name=username, email=email, phone_number=phone, employee_module=employee_module)
        obj.save()
        messages.info(request, "HeatTesting Registration Successful")
        return render(request, 'heat_testing/login.html')

    return render(request, 'heat_testing/register.html')

def ht_login(request):
    try:
        if request.method == "POST":
            print(1)
            email = request.POST.get('email')
            password = request.POST.get('password')
            print(2)
            users = Brine.objects.get(email=email, password=password)
            if users:
                messages.info(request, "HeatTesting Login Successful")
                print(5)
                return redirect('/ht_home/')
            return render(request, 'heat_testing/login.html')


        return render(request, 'heat_testing/login.html')
    except:

        return redirect('/ht_login/')

def ht_home(request):
    return render(request,'heat_testing/ht_home.html')

def Pt_reports(request):
    data = ResidentialDetails.objects.all()
    return render(request, 'heat_testing/reports.html', {"data": data})
def He_reports(request):
    data = ResidentialDetails.objects.all()
    return render(request, 'heat_testing/he_reports.html', {"data": data})

def Bi_reports(request):
    data = ResidentialDetails.objects.all()
    return render(request, 'heat_testing/bi_reports.html', {"data": data})

def ht_analyze(request):
    data = ResidentialDetails.objects.all()
    return render(request, 'heat_testing/ht_analyze.html', {"data": data})


def calculate_final_temperature(request,id):

    building = ResidentialDetails.objects.get(id=id)
    if building.building_material=='Concrete':
        c=1470
    elif building.building_material == 'Bricks':
        c = 1120
    elif building.building_material == 'Wood':
        c = 1760
    elif building.building_material == 'Glass':
        c=840

    Qs = building.Q_secondary
    print(Qs)
    Ti = building.temperature
    print(Ti)
    print(c)
    Tf = Ti + (Qs /c)
    print(Tf)
    building.final_temperature= round(Tf)
    building.htdone=True

    building.save()
    messages.info(request, f"{building.Br_id}:HeatTesting Analyzed Successful")
    return redirect('/ht_analyze/')


def Ht_report(request):
    data = ResidentialDetails.objects.filter(htdone=True)
    return render(request, 'heat_testing/final_report.html', {"data": data})




def ht_logout(request):
    messages.info(request, "HeatTesting Logout Successful")
    return render(request, 'home/home.html')
