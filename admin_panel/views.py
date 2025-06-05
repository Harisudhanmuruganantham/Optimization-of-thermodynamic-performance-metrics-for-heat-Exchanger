from django.shortcuts import render,HttpResponse,redirect
from .models import Brine
from django.core.mail import send_mail
import random

from django.contrib import messages
from .models import ResidentialDetails
from reportlab.lib.colors import red, black
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse
from django.core.files.base import ContentFile


def home(request):
    return render(request,'home/home.html')

def admin_login(request):
    admin_page={"admin@gmail.com":"brine"}
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            if admin_page.get(email) == password:
                messages.info(request, "Admin Login Successful")
                return render(request, "admins/admin_home.html")
            else:
                return HttpResponse("Invalid email address or password, please check again!")
        except Exception as e:
            return HttpResponse(f"Error: {e}")


    return render(request,"admins/login.html")





def pipe_transfer_details(request):
    data=Brine.objects.filter(employee_module='Pipe Transfer')
    return render(request,'pipe_transfer/manage_log1.html',{'data':data})

def heat_exchange_details(request):
    data=Brine.objects.filter(employee_module='Heat Exchange')
    return render(request,'heat_exchange/manage_log2.html',{'data':data})
def brine_intake_details(request):
    data=Brine.objects.filter(employee_module='Brine Intake')
    return render(request,'brine_intake/manage_log3.html',{'data':data})

def heat_testing_details(request):
    data=Brine.objects.filter(employee_module='Heat Testing')
    return render(request,'heat_testing/manage_log4.html',{'data':data})
def admin_home(request):
    return render(request,'admins/admin_home.html')


def generate_client_id():
    characters=random.randint(1000, 9999)
    return characters
def approve(request, id):
    try:
        client = Brine.objects.get(id=id)
        d= random.randint(10000,99999)
        client.password = d


        subject = f"{client. employee_module}:your username and your password"
        plain_message = f"Hi,\n\nThank you for using this web application,\n\n Your username is {client.email} and Your password is: {client.password}.\n\nSo kindly use this username and  password while login into the portal of {client.employee_module} process.\n\nThank you"

        send_mail(subject, plain_message, 'vetrim.surya@gmail.com', [client.email], fail_silently=False)

        r= random.randint(1000,9999)
        client.client_id=f"BH:{r}"

        client.approve = True
        client.save()
        messages.info(request,f"{client.client_id}: Registration Approved Successfully")
        return redirect('/admin_home/')
    except Exception as e:
        print(f"An error occurred while sending email: {e}")
        return redirect('/admin_home/')

def rejection(request,id):
    try:
        client = Brine.objects.get(id=id)



        # Example of sending an email on rejection
        subject = 'Rejection Notification'
        plain_message = f"Hi {client.name},\n\nYour request for {client.employee_module} has been rejected.\n\n Sorry we could not move forward your {client.employee_module}\n\nThank you."
        send_mail(subject, plain_message, 'sender@example.com', [client.email], fail_silently=False)

        # Update client status or other fields related to rejection
        client.reject = True  # Assuming 'reject' is a field in your Brine model
        client.save()
        messages.info(request,"Registration rejected")

        return redirect('/admin_home/')  # Redirect to the admin page after rejection
    except Exception as e:
        # Print the exception for debugging purposes
        print(f"An error occurred while sending rejection email: {e}")
        return redirect('/admin_home/') # Handle error appropriately

def admin_logout(request):
    try:
        messages.info(request, "Admin Logout Successful")
        return redirect("/")
    except Exception as e:
        print(f"Error during logout: {e}")
        return redirect("/admin_home/")

def admin_requirements(request):
    if request.method == "POST":
        Building_type = request.POST["building_type"]
        number_of_rooms = request.POST["number_of_rooms"]
        area = request.POST["area"]
        building_temp=request.POST["building_temp"]
        water_body = request.POST["water_body"]
        distance_to_water_body_m = request.POST["distance_to_water_body_m"]
        water_body_temperature = request.POST["water_body_temperature"]
        building_material=request.POST["building_material"]
        obj = ResidentialDetails(Building_type=Building_type, number_of_rooms=number_of_rooms, area=area,temperature= building_temp,water_body=water_body,distance_to_water_body_m=distance_to_water_body_m,water_body_temperature=water_body_temperature,building_material=building_material)

        B= random.randint(1000, 9999)
        obj.Br_id = f"BR:{B}"
        obj.save()
        messages.info(request, f"{obj.Br_id}:Requirements Uploaded Successful")
        return render(request, 'admins/admin_home.html')
    return render(request, 'admins/requirements.html')

def admin_Manage_status(request):
    data=ResidentialDetails.objects.all()
    return render(request,'admins/manage_status.html',{"data":data})

def pt_report(request):
    data = ResidentialDetails.objects.filter(ptdone=True)
    return render(request, 'admins/pt_report.html', {"data": data})


def he_report(request):
    data = ResidentialDetails.objects.filter(hedone=True)
    return render(request, 'admins/he_report.html', {"data": data})
def bi_report(request):
    data = ResidentialDetails.objects.filter(bidone=True)
    return render(request, 'admins/bi_report.html', {"data": data})

def ht_report(request):
    data = ResidentialDetails.objects.filter(htdone=True)
    return render(request, 'admins/ht_report.html', {"data": data})

# def pdf(request):
#     data = ResidentialDetails.objects.all()
#     return render(request, 'admins/generate_pdf.html', {"data": data})






def generate_pdf(request, id):
    # Retrieve ResidentialDetails object or return 404 if not found
    user =ResidentialDetails.objects.get(id=id)

    title = "BRINE SOLUTION HEAT EXCHANGE ANALYSIS"

    # Data to be displayed in the PDF
    list_data = [
        f"Project ID: {user.Br_id}",
        "REQUIREMENTS",
        f"Building Type: {user.Building_type}",
        f"Number of rooms: {user.number_of_rooms}",
        f"Area: {user.area}",
        f"Temperature: {user.temperature}",
        f"Water Body: {user.water_body}",
        f"Distance To Waterbody: {user.distance_to_water_body_m}",
        f"Water Body Temperature: {user.water_body_temperature}",
        f"Building Material: {user.building_material}",

        "PIPE TRANSFER ANALYZE",
        f"Material: {user.material}",
        f"Diameter (mm): {user.diameter_mm}",
        f"Length (m): {user.length_m}",
        f"Insulation Thickness (mm): {user.insulation_thickness_mm}",
        f"Pressure (Pa): {user.pressure_rating_pa}",
        f"Heat Transfer Coefficient (W/m²K): {user.heat_transfer_coefficient_w_m2k}",

        "HEAT EXCHANGE ANALYZE",
        f"Q Primary: {user.Q_primary}",
        f"Q Secondary: {user.Q_secondary}",

        "BRINE INTAKE ANALYZE",
        f"Brine Solution: {user.brine_solution}",
        f"Thermal Conductivity (W/(m·K)): {user.Thermal_Conductivity}",
        f"Density (kg/m³): {user.Density}",

        "HEAT TESTING ANALYZE",
        f"Final Temperature: {user.final_temperature}",
    ]

    buffer = BytesIO()
    # Create a canvas object
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    # Set the title
    c.setFont("Helvetica-Bold", 16)
    text_width = c.stringWidth(title)
    c.setFillColor(red)
    x_position = (width - text_width) / 2  # Center the title horizontally
    c.drawString(x_position, height - 80, title)  # Adjusted vertical position for title

    # Set the content
    c.setFont("Helvetica", 12)
    y_position = height - 130  # Adjusted starting vertical position
    left_margin = 40  # Margin from the left edge
    line_spacing = 20  # Space between lines


    for line in list_data:
        if line.startswith("Project ID:"):
            c.setFont("Helvetica-Bold", 12)  # Set font to bold
            c.setFillColor(black)  # Set color to black
            line_spacing = 30

        elif any(section in line for section in
                 ["REQUIREMENTS", "PIPE TRANSFER ANALYZE", "HEAT EXCHANGE ANALYZE", "BRINE INTAKE ANALYZE",
                  "HEAT TESTING ANALYZE"]):
            c.setFont("Helvetica-Bold", 12)  # Set font to bold for section headers
            c.setFillColor(red)

            line_spacing = 15# Set color to red for section headers
        else:
            c.setFont("Helvetica", 10)  # Set font back to normal
            c.setFillColor(black)  # Set color to black
            line_spacing = 20
            top_margin = 20

        c.drawString(left_margin, y_position, line)
        y_position -= line_spacing
        # Move to the next line

    c.save()
    pdf_data = buffer.getvalue()
    buffer.close()

    # Prepare HTTP response with PDF data
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{title}_{user.Br_id}.pdf"'
    response.write(pdf_data)

    # Save PDF file to the model field
    user.f_report.save(f"{title}_{user.Br_id}.pdf", ContentFile(pdf_data))
    user.fview = True
    user.save()

    # Redirect after generating PDF
    return redirect('/admin_Manage_status/')
