from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
import csv
import json

from .models import User, ShopStrength, Coach, Inspection, Defect, Attendance, Feedback
from .serializers import (
    UserSerializer, ShopStrengthSerializer, CoachSerializer,
    InspectionSerializer, DefectSerializer, AttendanceSerializer,
    FeedbackSerializer
)

# Custom permission class for role-based access
class RoleBasedPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        # RITES Admin has full access
        if request.user.role == 'RITES_ADMIN':
            return True

        # RITES Quality Manager can view and modify data
        if request.user.role == 'RITES_QM':
            return request.method in ['GET', 'POST', 'PUT', 'PATCH']

        # MCF Admin can only view
        if request.user.role == 'MCF_ADMIN':
            return request.method == 'GET'

        return False

# ViewSets
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class ShopStrengthViewSet(viewsets.ModelViewSet):
    queryset = ShopStrength.objects.all()
    serializer_class = ShopStrengthSerializer
    permission_classes = [RoleBasedPermission]

class CoachViewSet(viewsets.ModelViewSet):
    queryset = Coach.objects.all()
    serializer_class = CoachSerializer
    permission_classes = [RoleBasedPermission]

class InspectionViewSet(viewsets.ModelViewSet):
    queryset = Inspection.objects.all()
    serializer_class = InspectionSerializer
    permission_classes = [RoleBasedPermission]

class DefectViewSet(viewsets.ModelViewSet):
    queryset = Defect.objects.all()
    serializer_class = DefectSerializer
    permission_classes = [RoleBasedPermission]

class AttendanceViewSet(viewsets.ModelViewSet):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer
    permission_classes = [RoleBasedPermission]

class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Authentication views
@api_view(['POST'])
def login_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return Response({
                'success': True,
                'user': UserSerializer(user).data,
                'message': 'Login successful'
            })
        else:
            return Response({
                'success': False,
                'message': 'Invalid credentials'
            }, status=400)
    except Exception as e:
        return Response({
            'success': False,
            'message': str(e)
        }, status=500)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({
        'success': True,
        'message': 'Logout successful'
    })

# Backup endpoint
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def backup_csv(request):
    # Only allow admins to download backups
    if request.user.role not in ['RITES_ADMIN', 'MCF_ADMIN']:
        return Response({'error': 'Permission denied'}, status=403)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="qms_backup.csv"'

    writer = csv.writer(response)
    writer.writerow(['S.No', 'Coach Type', 'Coach Number', 'Created At'])

    for coach in Coach.objects.all():
        writer.writerow([coach.sno, coach.coach_type, coach.coach_number, coach.created_at])

    return response

# Dashboard summary
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def dashboard_summary(request):
    try:
        data = {
            'total_coaches': Coach.objects.count(),
            'total_inspections': Inspection.objects.count(),
            'total_defects': Defect.objects.count(),
            'pending_inspections': Inspection.objects.filter(accepted_date__isnull=True).count(),
        }
        return Response(data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)
