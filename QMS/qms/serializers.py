from rest_framework import serializers
from .models import User, ShopStrength, Coach, Inspection, Defect, Attendance, Feedback

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'first_name', 'last_name', 'email']

class ShopStrengthSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopStrength
        fields = '__all__'

class CoachSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coach
        fields = '__all__'

class DefectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Defect
        fields = '__all__'

class InspectionSerializer(serializers.ModelSerializer):
    defects = DefectSerializer(many=True, read_only=True)

    class Meta:
        model = Inspection
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'
