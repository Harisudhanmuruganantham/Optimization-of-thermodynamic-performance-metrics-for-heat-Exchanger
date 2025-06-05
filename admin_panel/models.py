from django.db import models

# Create your models here.
class Brine(models.Model):
    client_id=models.CharField(max_length=200,null=True)
    name=models.CharField(max_length=100)
    email=models.EmailField(unique=True,max_length=200,null=True)
    password=models.CharField(max_length=200,null=True)
    phone_number=models.PositiveBigIntegerField()
    employee_module=models.CharField(max_length=100)
    approve=models.BooleanField(null=True,default=0)
    reject = models.BooleanField(null=True, default=0)

class ResidentialDetails(models.Model):
    Br_id=models.CharField(max_length=200,null=True)
    Building_type = models.CharField(max_length=100)
    number_of_rooms = models.IntegerField()
    area = models.FloatField()  # in square meters
    temperature = models.FloatField(null=True)
    water_body = models.CharField(max_length=100)
    distance_to_water_body_m = models.FloatField()  # in kilometers
    water_body_temperature = models.FloatField()  # in Celsius
    temperature=models.FloatField(null=True)
    building_material=models.CharField(max_length=100,null=True)
    status=models.CharField(max_length=100,default="pending")





    #Pipe Transfer Analysis
    material = models.CharField(max_length=100,null=True)
    diameter_mm = models.FloatField(null=True)
    length_m = models.FloatField(null=True)
    insulation_type = models.CharField(max_length=100, null=True)
    insulation_thickness_mm = models.FloatField(null=True)
    pressure_rating_pa = models.FloatField(null=True)
    heat_transfer_coefficient_w_m2k = models.FloatField(null=True)
    ptdone = models.BooleanField(default=False, null=True)
    hedone = models.BooleanField(default=False, null=True)
    bidone= models.BooleanField(default=False, null=True)
    htdone = models.BooleanField(default=False, null=True)
    fview = models.BooleanField(default=False, null=True)



    #heat exchange analysis

    Q_primary=models.FloatField(null=True)

    Q_secondary=models.FloatField(null=True)

    #brine intake
    brine_solution=models.CharField(max_length=100,null=True)
    HTC=models.FloatField(null=True)
    Thermal_Conductivity=models.FloatField(null=True)
    Density=models.FloatField(null=True)

    #heat testing
    final_temperature = models.FloatField(null=True)
    f_report = models.FileField(upload_to='pdf_reports/', null=True, blank=True)




