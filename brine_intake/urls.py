from django.urls import path
from . import views


urlpatterns = [
    path('bi_register/',views.bi_register,name="bi_register"),
    path('bi_login/',views.bi_login,name="bi_login"),
    path('he_reports/',views.he_reports,name="he_reports"),
    path('bi_home/', views.bi_home, name="bi_home"),
    path('bi_analyze/', views.bi_analyze, name="bi_analyze"),
    path('calculate_htc/<int:id>/', views.calculate_htc, name="calculate_htc"),
    path('bi_reports/', views.bi_reports, name="bi_reports"),

    path('brine_logout/', views.brine_logout, name="brine_logout"),

    ]