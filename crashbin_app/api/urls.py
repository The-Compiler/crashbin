from django.urls import path, include
from rest_framework import routers
from crashbin_app.api import views


router = routers.DefaultRouter()
router.register(r'reports', views.ReportViewSet)
router.register(r'bins', views.BinViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('report/new/', views.ReportNew.as_view())
]
