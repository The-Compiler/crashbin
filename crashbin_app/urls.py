from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reports', views.report_list, name='report_list'),
    path('report/<int:pk>/', views.report_detail, name='report_detail'),
]
