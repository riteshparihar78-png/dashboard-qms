from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, ShopStrengthViewSet, CoachViewSet, InspectionViewSet,
    DefectViewSet, AttendanceViewSet, FeedbackViewSet, 
    backup_csv, login_view, logout_view, dashboard_summary
)

# API Router
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'shopstrength', ShopStrengthViewSet)
router.register(r'coaches', CoachViewSet)
router.register(r'inspections', InspectionViewSet)
router.register(r'defects', DefectViewSet)
router.register(r'attendance', AttendanceViewSet)
router.register(r'feedback', FeedbackViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/login/', login_view, name='login'),
    path('auth/logout/', logout_view, name='logout'),
    path('backup/', backup_csv, name='backup'),
    path('dashboard/summary/', dashboard_summary, name='dashboard_summary'),
]
