from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('reports', views.report_list, name='report_list'),
    path('report/<int:pk>/', views.report_detail, name='report_detail'),
    path('report/<int:pk>/reply', views.report_reply, name='report_reply'),
    path('bins', views.bin_list, name='bin_list'),
    path('bin/new/', views.bin_new, name='bin_new'),
    path('bin/<int:pk>/', views.bin_detail, name='bin_detail'),
    path('api/', include('crashbin_app.api.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
]
