from django.urls import path, include
from rest_framework import routers
from crashbin_app.api import views

router = routers.DefaultRouter()
router.register(r'reports', views.ReportViewSet, basename='api-report')
router.register(r'bins', views.BinViewSet, basename='api-bin')

urlpatterns = [
    path('', include(router.urls)),
    path('report/new/', views.ReportNew.as_view())
]
