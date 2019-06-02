from django.urls import path, include

from crashbin_app.views import misc_view, report_view, setting_view, bin_view, label_view

urlpatterns = [
    path('', misc_view.home, name='home'),
    path('search/', misc_view.search_dispatch, name='search_dispatch'),
    path('api/', include('crashbin_app.api.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    path('reports', report_view.report_list, name='report_list'),
    path('report/<int:pk>/', report_view.report_detail, name='report_detail'),
    path('report/<int:pk>/reply', report_view.report_reply, name='report_reply'),
    path('report/<int:pk>/settings/<str:setting>', setting_view.settings, name='report_settings'),

    path('bins', bin_view.bin_list, name='bin_list'),
    path('bin/new/', bin_view.bin_new_edit, name='bin_new_edit'),
    path('bin/<int:pk>/', bin_view.bin_detail, name='bin_detail'),
    path('bin/<int:pk>/edit', bin_view.bin_new_edit, name='bin_new_edit'),
    path('bin/<int:pk>/subscribe', bin_view.bin_subscribe, name='bin_subscribe'),
    path('bin/<int:pk>/settings/<str:setting>', setting_view.settings, name='bin_settings'),

    path('labels', label_view.label_list, name='label_list'),
    path('label/new/', label_view.label_new_edit, name='label_new_edit'),
    path('label/<int:pk>/edit', label_view.label_new_edit, name='label_new_edit'),
]
