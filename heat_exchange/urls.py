from django.urls import path
from . import views


urlpatterns = [
    path('he_register/',views.he_register,name="he_register"),
    path('he_login/',views.he_login,name="he_login"),
    path('he_home/', views.he_home, name="he_home"),
    path('he_requirements/', views.he_requirements, name="he_requirements"),
    path('he_analyze/', views.he_analyze, name="he_analyze"),
    path('heat_exchange_analysis/<int:id>/', views.heat_exchange_analysis, name="heat_exchange_analysis"),
    path('heat_report/', views.heat_report, name="heat_report"),
    path('heat_logout/', views.heat_logout, name="heat_logout"),

    ]