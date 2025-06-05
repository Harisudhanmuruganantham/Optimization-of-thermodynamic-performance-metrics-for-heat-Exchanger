from django.shortcuts import render,redirect
from admin_panel.models import Brine
from django.contrib import messages
from admin_panel.models import ResidentialDetails
import pandas as pd
# Create your views here.


# Create your views here.
def bi_register(request):
    if request.method == "POST":
        username = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        employee_module = request.POST.get("module")

        # Check if the email address ends with @gmail.com
        if not email.endswith('@gmail.com'):
            messages.error(request, "Only Gmail addresses are allowed.")
            return render(request, 'brine_intake/register.html')

        # Check if the email is unique
        if Brine.objects.filter(email=email).exists():
            messages.error(request, "This email address is already registered.")
            return render(request, 'brine_intake/register.html')

        # Save the new registration
        obj = Brine(name=username, email=email, phone_number=phone, employee_module=employee_module)
        obj.save()
        messages.info(request, "BrineIntake Registration Successful")
        return render(request, 'brine_intake/login.html')

    return render(request, 'brine_intake/register.html')



def bi_login(request):
    try:
        if request.method == "POST":
            print(1)
            email = request.POST.get('email')
            password = request.POST.get('password')
            print(2)
            users = Brine.objects.get(email=email, password=password)
            if users:
                messages.info(request, "BrineIntake Login Successful")
                print(5)
                return render(request, 'brine_intake/bi_home.html')
            return render(request, 'brine_intake/login.html')


        return render(request, 'brine_intake/login.html')
    except:

        return redirect('/bi_login/')

def bi_home(request):
    return render(request,'brine_intake/bi_home.html')

def he_reports(request):
    data=ResidentialDetails.objects.all()
    return render(request,'brine_intake/heat_report.html',{'data':data})

def brine_logout(request):
    messages.info(request, "BrineIntake Logout Successful")
    return render(request,'home/home.html')

def bi_analyze(request):
    data = ResidentialDetails.objects.all()
    return render(request, 'brine_intake/bi_analyze.html', {"data": data})

# def calculate_htc(request, id):
#     try:
#         data = ResidentialDetails.objects.get(id=id)
#     except ResidentialDetails.DoesNotExist:
#
#         return redirect('/bi_analyze/')
#
#     file_path = 'D:\PROJECTS\Heat_Exchange\heat_exchange_project\dataset\data_set.csv'
#
#     try:
#         df = pd.read_csv(file_path, encoding='iso-8859-1')
#     except UnicodeDecodeError as e:
#         print(f"Error reading CSV file: {str(e)}")
#         return redirect('/bi_analyze/')
#
#     max_htc = -float('inf')
#     best_brine_solution = None
#
#     for index, row in df.iterrows():
#         try:
#             thermal_conductivity_avg = sum(map(float, row['Thermal Conductivity (W/(m·K))'].split('-'))) / 2
#             density_avg = sum(map(float, row['Density (kg/m³)'].split('-'))) / 2
#
#             HTC = data.Q_primary / (data.A_primary * data.delta_T_primary)
#
#             result = {
#                 'brine_solution': row['Brine Solution'],
#                 'theoretical_htc': round(HTC, 2),
#                 'thermal_conductivity_range': row['Thermal Conductivity (W/(m·K))'],
#                 'density_range': row['Density (kg/m³)'],
#             }
#
#
#             if HTC > max_htc:
#                 max_htc = HTC
#
#                 data.brine_solution = row['Brine Solution']
#                 data.HTC=max_htc
#                 data.Thermal_Conductivity=thermal_conductivity_avg
#                 data.Density=density_avg
#                 data.bidone = True
#                 data.status = "Heat Exchange Is Done"
#
#                 data.save()
#                 return redirect('/bi_analyze/')
#
#         except Exception as e:
#             # Handle any specific row processing errors here
#             print(f"Error processing row {index}: {str(e)}")
#             continue  # Move to the next row if there's an error
#
#
#     if best_brine_solution:
#
#         print(f"The best brine solution is: {best_brine_solution} with maximum HTC of {max_htc}")
#     return redirect('/bi_analyze/')

# def calculate_htc(request, id):
#     try:
#         data = ResidentialDetails.objects.get(id=id)
#     except ResidentialDetails.DoesNotExist:
#         return redirect('/bi_analyze/')  # Redirect if ResidentialDetails object does not exist
#
#     file_path = 'D:/PROJECTS/Heat_Exchange/heat_exchange_project/dataset/data_set.csv'
#
#     try:
#         df = pd.read_csv(file_path, encoding='iso-8859-1')
#     except UnicodeDecodeError as e:
#         print(f"Error reading CSV file: {str(e)}")
#         return redirect('/bi_analyze/')
#
#     max_htc = -float('inf')
#     best_brine_solution = None
#     water_temperature = 25.0  # Assume water temperature is constant at 25.0°C
#
#     for index, row in df.iterrows():
#         try:
#             # Extract average values from ranges (assuming format like "0.6 - 0.8")
#             thermal_conductivity_avg = sum(map(float, row['Thermal Conductivity (W/(m·K))'].split('-'))) / 2
#             density_avg = sum(map(float, row['Density (kg/m³)'].split('-'))) / 2
#
#             # Calculate brine temperature assuming a difference of 1.0°C from water temperature
#             brine_temperature = water_temperature + 1.0
#
#             # Calculate HTC using the adjusted formula
#             HTC = thermal_conductivity_avg * (data.Q_primary * (brine_temperature - water_temperature))
#
#             # Update data if current solution has higher HTC
#             if HTC > max_htc:
#                 max_htc = HTC
#                 best_brine_solution = {
#                     'brine_solution': row['Brine Solution'],
#                     'theoretical_htc': round(HTC, 2),
#                     'thermal_conductivity_range': row['Thermal Conductivity (W/(m·K))'],
#                     'density_range': row['Density (kg/m³)'],
#                 }
#
#         except Exception as e:
#             # Handle any specific row processing errors here
#             print(f"Error processing row {index}: {str(e)}")
#             continue  # Move to the next row if there's an error
#
#     if best_brine_solution:
#         # Update ResidentialDetails object with the best solution found
#         data.brine_solution = best_brine_solution['brine_solution']
#         data.HTC = best_brine_solution['theoretical_htc']
#         data.Thermal_Conductivity = thermal_conductivity_avg
#         data.Density = density_avg
#         data.bidone = True
#         data.status = "Brine Intake Is Done"
#         data.save()  # Save the updated object to the database
#         messages.info(request, f"{data.Br_id}:BrineIntake Analyzed Successful")
#
#     return redirect('/bi_analyze/')
def calculate_htc(request, id):
    try:
        # Retrieve the ResidentialDetails object
        data = ResidentialDetails.objects.get(id=id)
    except ResidentialDetails.DoesNotExist:
        return redirect('/bi_analyze/')  # Redirect if ResidentialDetails object does not exist

    # Path to the CSV file
    file_path = 'D:/project/Heat_Exchange/Heat_Exchange/heat_exchange_project/dataset/data_set.csv'

    try:
        # Read the CSV file
        df = pd.read_csv(file_path, encoding='iso-8859-1')
    except UnicodeDecodeError as e:
        print(f"Error reading CSV file: {e}")
        return redirect('/bi_analyze/')

    # Ensure DataFrame is not empty
    if df.empty:
        print("CSV file is empty.")
        return redirect('/bi_analyze/')

    max_htc = -float('inf')
    best_brine_solution = None
    water_temperature = data. water_body_temperature  # Use the water body temperature from the ResidentialDetails object

    for index, row in df.iterrows():
        try:
            # Extract average values from ranges (format: "0.6 - 0.8")
            thermal_conductivity_values = list(map(float, row['Thermal Conductivity (W/(m·K))'].split('-')))
            density_values = list(map(float, row['Density (kg/m³)'].split('-')))

            if len(thermal_conductivity_values) != 2 or len(density_values) != 2:
                print(f"Invalid range format in row {index}")
                continue

            thermal_conductivity_avg = sum(thermal_conductivity_values) / 2
            density_avg = sum(density_values) / 2


            brine_temperature = water_temperature + 1.0

            # Calculate HTC (simple example formula, modify as needed)
            # HTC = (thermal_conductivity * (brine_temperature - water_temperature)) / density
            HTC = thermal_conductivity_avg * (data.Q_primary * (brine_temperature - water_temperature)) / density_avg

            # Update the best brine solution if this one has a higher HTC
            if HTC > max_htc:
                max_htc = HTC
                best_brine_solution = {
                    'brine_solution': row['Brine Solution'],
                    'theoretical_htc': round(HTC, 2),
                    'thermal_conductivity_range': row['Thermal Conductivity (W/(m·K))'],
                    'density_range': row['Density (kg/m³)'],
                    'thermal_conductivity_avg': thermal_conductivity_avg,
                    'density_avg': density_avg
                }

        except ValueError as e:
            print(f"Error processing row {index}: {e}")
            continue
        except Exception as e:
            print(f"Unexpected error processing row {index}: {e}")
            continue

    if best_brine_solution:
        # Update the ResidentialDetails object with the best solution found
        data.brine_solution = best_brine_solution['brine_solution']
        data.HTC = best_brine_solution['theoretical_htc']
        data.Thermal_Conductivity = best_brine_solution['thermal_conductivity_avg']
        data.Density = best_brine_solution['density_avg']
        data.bidone = True
        data.status = "Brine Intake Is Done"
        data.save()  # Save the updated object to the database
        messages.info(request, f"{data.Br_id}: Brine Intake Analyzed Successful")

    return redirect('/bi_analyze/')

def bi_reports(request):
    data = ResidentialDetails.objects.filter(bidone=True)
    return render(request,'brine_intake/bi_report.html',{"data": data})


