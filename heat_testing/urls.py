from django.urls import path
from . import views


urlpatterns = [
    path('ht_register/',views.ht_register,name="ht_register"),
    path('ht_login/',views.ht_login,name="ht_login"),
    path('ht_home/',views.ht_home,name="ht_home"),
    path('Pt_reports/',views.Pt_reports,name="Pt_reports"),
    path('He_reports/',views.He_reports,name="He_reports"),
    path('Bi_reports/',views.Bi_reports,name="Bi_reports"),
    path('ht_analyze/',views.ht_analyze,name="ht_analyze"),
    path('HT_report/',views.Ht_report,name="Ht_report"),

    path('calculate_final_temperature/<int:id>/',views.calculate_final_temperature,name="calculate_final_temperature"),
    path('ht_logout/',views.ht_logout,name="ht_logout"),


    ]