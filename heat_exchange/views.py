from django.http import HttpResponseServerError, HttpResponseNotFound
from django.shortcuts import render,redirect,HttpResponse
from admin_panel.models import Brine
from django.contrib import messages
from admin_panel.models import ResidentialDetails
import csv
import math
import pandas as pd
from sklearn.ensemble import BaggingRegressor
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
import pandas as pd
from django.conf import settings
from math import log
# from .forms import FilterForm




# Create your views here.
def he_register(request):
    if request.method == "POST":
        username = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        employee_module = request.POST.get("module")

        # Check if the email address is a valid Gmail address
        if not email.endswith('@gmail.com'):
            messages.error(request, "Only Gmail addresses are allowed.")
            return render(request, 'heat_exchange/register.html')

        # Check if the email is unique
        if Brine.objects.filter(email=email).exists():
            messages.error(request, "This email address is already registered.")
            return render(request, 'heat_exchange/register.html')

        # Save the new registration
        obj = Brine(name=username, email=email, phone_number=phone, employee_module=employee_module)
        obj.save()
        messages.info(request, "HeatExchange Registration Successful")
        return render(request, 'heat_exchange/login.html')

    return render(request, 'heat_exchange/register.html')

def he_login(request):
    try:
        if request.method == "POST":
            print(1)
            email = request.POST.get('email')
            password = request.POST.get('password')
            print(2)
            users = Brine.objects.get(email=email, password=password)
            if users:
                messages.info(request, "HeatExchange Login  Successful")
                print(5)
                return redirect('/he_home/')
                # return render(request, 'heat_exchange/he_home.html')


            return render(request, 'heat_exchange/login.html')


        return render(request, 'heat_exchange/login.html')
    except:

        return redirect('/he_login/')

def he_home(request):
    return render(request, 'heat_exchange/he_home.html')

def he_requirements(request):
    data=ResidentialDetails.objects.all()
    return render(request, 'heat_exchange/pipe_report.html', {"data": data})

def he_analyze(request):
    data = ResidentialDetails.objects.all()
    return render(request,'heat_exchange/he_analyze.html',{"data": data})





def heat_exchange_analysis(request, id):
    # Retrieve ResidentialDetails object using id
    building = ResidentialDetails.objects.get(id=id)

    # Assign values to variables
    d= building.diameter_mm
    l = building.length_m
    i = building.insulation_thickness_mm
    p = building.pressure_rating_pa
    h = building.heat_transfer_coefficient_w_m2k

    # Load the dataset
    dataset = pd.read_csv(r'D:/project/Heat_Exchange/Heat_Exchange/heat_exchange_project/dataset/heat_exchange.csv')

    # Use the data from the dataset
    X = dataset[['diameter_mm', 'length_m', 'insulation_thickness_mm', 'pressure_pa', 'heat_transfer_coefficient_w_m2k']]
    y_primary = dataset['Q_primary']
    y_secondary = dataset['Q_secondary']

    # Split the data into training and testing sets
    X_train, X_test, y_train_primary, y_test_primary = train_test_split(
        X, y_primary, test_size=0.2, random_state=42
    )
    _, _, y_train_secondary, y_test_secondary = train_test_split(
        X, y_secondary, test_size=0.2, random_state=42
    )

    # Train BaggingRegressor for Q_primary
    base_regressor_primary = DecisionTreeRegressor()
    bagging_regressor_primary = BaggingRegressor(base_regressor_primary, n_estimators=100, random_state=42)
    bagging_regressor_primary.fit(X_train, y_train_primary)

    # Train BaggingRegressor for Q_secondary
    base_regressor_secondary = DecisionTreeRegressor()
    bagging_regressor_secondary = BaggingRegressor(base_regressor_secondary, n_estimators=100, random_state=42)
    bagging_regressor_secondary.fit(X_train, y_train_secondary)

    # Create a DataFrame with input data for prediction
    input_data = pd.DataFrame([[d, l, i, p, h]],
        columns=['diameter_mm', 'length_m', 'insulation_thickness_mm', 'pressure_pa', 'heat_transfer_coefficient_w_m2k']
    )

    # Make predictions using the trained models
    prediction_primary = bagging_regressor_primary.predict(input_data)
    prediction_secondary = bagging_regressor_secondary.predict(input_data)

    # Update building object with predictions and other attributes
    building.Q_primary = prediction_primary[0]
    building.Q_secondary = prediction_secondary[0]
    building.hedone = True
    building.status = "Heat Exchange Is Done"
    building.save()

    # Redirect to a specific URL after processing
    messages.info(request, f"{building.Br_id}:Heat Exchange Analyzed  Successful")
    return redirect('/he_analyze/')


def heat_report(request):
    data = ResidentialDetails.objects.filter(hedone=True)
    return render(request, 'heat_exchange/heat_exchange_report.html', {"data": data})
def heat_logout(request):
    messages.info(request, "HeatExchange Logout Successful")
    return render(request,'home/home.html')