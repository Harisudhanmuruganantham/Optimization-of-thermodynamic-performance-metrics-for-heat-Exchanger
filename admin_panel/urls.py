from django.urls import path
from . import views


urlpatterns = [
    path('',views.home,name="home"),
    path('admin_login/',views.admin_login,name="admin_login"),
    path('admin_logout/', views.admin_logout, name="admin_logout"),
    path('pipe_transfer_details/',views.pipe_transfer_details,name="pipe_transfer_details"),
    path('heat_exchange_details/',views.heat_exchange_details,name="heat_exchange_details"),
    path('brine_intake_details/', views.brine_intake_details, name="brine_intake_details"),
    path('heat_testing_details/', views.heat_testing_details, name="heat_testing_details"),

    path('admin_home/',views.admin_home,name='admin_home'),
    path('approve/<int:id>/', views.approve),
    path('rejection/<int:id>/',views.rejection),
    path('admin_requirements/', views.admin_requirements,name="admin_requirements"),
    path('admin_Manage_status/', views.admin_Manage_status,name="admin_Manage_status"),
    path('pt_report/', views.pt_report,name="pt_report"),
    path('he_report/', views.he_report,name="he_report"),
    path('bi_report/', views.bi_report,name="bi_report"),
    path('ht_report/', views.ht_report,name="ht_report"),
    path('generate_pdf/<int:id>/', views.generate_pdf,name="generate_pdf"),
    # path('pdf/', views.pdf, name="pdf"),




    ]