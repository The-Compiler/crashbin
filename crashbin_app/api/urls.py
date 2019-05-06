from django.urls import path
from crashbin_app.api import views


urlpatterns = [
    path('report/new/', views.ReportNew.as_view()),
]
