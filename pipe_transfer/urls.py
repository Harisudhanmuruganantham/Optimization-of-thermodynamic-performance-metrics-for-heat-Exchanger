from django.urls import path
from . import views


urlpatterns = [
    path('pt_register/',views.pt_register,name="pt_register"),
    path('pt_login/',views.pt_login,name="pt_login"),
    path('pt_home/',views.pt_home,name="pt_home"),
    path('pipe_Manage_status/',views.pipe_Manage_status,name="pipe_Manage_status"),
    path('pt_requirements/', views.pt_requirements, name="pt_requirements"),

    path('calculate_pipes/<int:id>/', views.calculate_pipes, name="calculate_pipes"),
    path('pipe_report/', views.pipe_report, name="pipe_report"),
    path('pipe_logout/', views.pipe_logout, name="pipe_logout"),
]