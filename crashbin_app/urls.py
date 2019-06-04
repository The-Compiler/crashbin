from django.urls import path, include

from crashbin_app.views import (
    misc_views,
    report_views,
    setting_views,
    bin_views,
    label_views,
)

urlpatterns = [
    path("", misc_views.home, name="home"),
    path("search/", misc_views.search_dispatch, name="search_dispatch"),
    path("api/", include("crashbin_app.api.urls")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("reports", report_views.report_list, name="report_list"),
    path("report/<int:pk>/", report_views.report_detail, name="report_detail"),
    path("report/<int:pk>/reply", report_views.report_reply, name="report_reply"),
    path(
        "report/<int:pk>/settings/<str:setting>",
        setting_views.settings,
        name="report_settings",
    ),
    path("bins", bin_views.bin_list, name="bin_list"),
    path("bin/new/", bin_views.bin_new_edit, name="bin_new_edit"),
    path("bin/<int:pk>/", bin_views.bin_detail, name="bin_detail"),
    path("bin/<int:pk>/edit", bin_views.bin_new_edit, name="bin_new_edit"),
    path("bin/<int:pk>/subscribe", bin_views.bin_subscribe, name="bin_subscribe"),
    path(
        "bin/<int:pk>/settings/<str:setting>",
        setting_views.settings,
        name="bin_settings",
    ),
    path("labels", label_views.label_list, name="label_list"),
    path("label/new/", label_views.label_new_edit, name="label_new_edit"),
    path("label/<int:pk>/edit", label_views.label_new_edit, name="label_new_edit"),
]
