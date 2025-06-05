from django.shortcuts import render,redirect
from admin_panel.models import Brine
from django.contrib import messages

from admin_panel.models import ResidentialDetails
# Create your views here.
def pt_register(request):
    if request.method == "POST":
        username = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        employee_module = request.POST.get("module")

        # Check if the email address is a valid Gmail address
        if not email.endswith('@gmail.com'):
            messages.error(request, "Only Gmail addresses are allowed.")
            return render(request, 'pipe_transfer/register.html')

        # Check if the email is unique
        if Brine.objects.filter(email=email).exists():
            messages.error(request, "This email address is already registered.")
            return render(request, 'pipe_transfer/register.html')

        # Save the new registration
        obj = Brine(name=username, email=email, phone_number=phone, employee_module=employee_module)
        obj.save()
        messages.info(request, "PipeTransfer Registration  Successful")
        return render(request, 'pipe_transfer/login.html')

    return render(request, 'pipe_transfer/register.html')



def pt_login(request):
    try:
        if request.method == "POST":
            print(1)
            email = request.POST.get('email')
            password = request.POST.get('password')
            print(2)
            users = Brine.objects.get(email=email, password=password)
            if users:
                messages.info(request, "PipeTransfer Login  Successful")
                print(5)
                return render(request, 'pipe_transfer/pt_home.html')
            return render(request, 'pipe_transfer/login.html')


        return render(request, 'pipe_transfer/login.html')



    except:

        return redirect('/pt_login/')


def pipe_Manage_status(request):

    data=ResidentialDetails.objects.all()
    return render(request,'pipe_transfer/admin_requirements.html',{"data":data})
def pt_home(request):
    return render(request, 'pipe_transfer/pt_home.html')

def pt_requirements(request):
    data=ResidentialDetails.objects.all()
    return render(request, 'pipe_transfer/pipe_requirements.html', {"data": data})



def calculate_pipes(request, id):
    building = ResidentialDetails.objects.get(id=id)
    if building.water_body_temperature < 10:
        building.material = "steel"
        building.diameter_mm = 250
        building.insulation_type = "brine"
        building.insulation_thickness_mm = 25
        building.pressure_rating_pa = 1000
        building.heat_transfer_coefficient_w_m2k = 200


    elif building.water_body_temperature >= 10 and building.water_body_temperature <= 25:

        building.material = "stainless steel"
        building.diameter_mm = 300
        building.insulation_type = "brine"
        building.insulation_thickness_mm = 30
        building.pressure_rating_pa = 1500
        building.heat_transfer_coefficient_w_m2k = 250
    else:
        building.material = "copper"
        building.diameter_mm = 250
        building.insulation_type = "brine"
        building.insulation_thickness_mm = 20
        building.pressure_rating_pa = 1200
        building.heat_transfer_coefficient_w_m2k = 220

    required_length = building.distance_to_water_body_m * building.area / 100  # Example calculation
    building.length_m = required_length
    building.ptdone = True
    building.status="Pipe Transfer Done"
    building.save()
    messages.info(request, f"{building.Br_id}:PipeTransfer Analyzed Successful")
    return redirect('/pt_requirements/')

def pipe_report(request):
    data= ResidentialDetails.objects.filter(ptdone=True)
    return render(request,'pipe_transfer/pipe_report.html',{"data": data})
def pipe_logout(request):
    messages.info(request, "PipeTransfer Logout Successful")
    return render(request,'home/home.html')