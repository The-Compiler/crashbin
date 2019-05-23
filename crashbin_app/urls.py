from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('search/', views.search_dispatch, name='search_dispatch'),
    path('api/', include('crashbin_app.api.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    path('reports', views.report_list, name='report_list'),
    path('report/<int:pk>/', views.report_detail, name='report_detail'),
    path('report/<int:pk>/reply', views.report_reply, name='report_reply'),
    path('report/<int:pk>/settings/<str:setting>', views.settings, name='report_settings'),

    path('bins', views.bin_list, name='bin_list'),
    path('bin/new/', views.bin_new_edit, name='bin_new_edit'),
    path('bin/<int:pk>/', views.bin_detail, name='bin_detail'),
    path('bin/<int:pk>/edit', views.bin_new_edit, name='bin_new_edit'),
    path('bin/<int:pk>/subscribe', views.bin_subscribe, name='bin_subscribe'),
    path('bin/<int:pk>/settings/<str:setting>', views.settings, name='bin_settings'),

    path('labels', views.label_list, name='label_list'),
    path('label/new/', views.label_new_edit, name='label_new_edit'),
    path('label/<int:pk>/edit', views.label_new_edit, name='label_new_edit'),
]
