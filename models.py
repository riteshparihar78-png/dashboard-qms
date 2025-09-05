from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """Custom User with role-based access"""
    ROLE_CHOICES = [
        ('RITES_ADMIN', 'RITES Admin'),
        ('RITES_QM', 'RITES Quality Manager'),
        ('MCF_ADMIN', 'MCF Admin'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='RITES_QM')

    def __str__(self):
        return f"{self.username} ({self.role})"

class ShopStrength(models.Model):
    """Shop manpower strength tracking"""
    shop_name = models.CharField(max_length=50, unique=True)
    strength = models.IntegerField()
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.shop_name} - {self.strength}"

class Coach(models.Model):
    """Railway coach details"""
    sno = models.IntegerField(unique=True)
    coach_type = models.CharField(max_length=100)
    coach_number = models.CharField(max_length=100)  # FIXED: was models.Char
    bogie_no1 = models.CharField(max_length=50, blank=True)
    bogie_no2 = models.CharField(max_length=50, blank=True)
    wheelset_no1 = models.CharField(max_length=50, blank=True)
    wheelset_no2 = models.CharField(max_length=50, blank=True)
    wheelset_no3 = models.CharField(max_length=50, blank=True)
    wheelset_no4 = models.CharField(max_length=50, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sno} - {self.coach_type} {self.coach_number}"

class Inspection(models.Model):
    """Quality control inspections"""
    SHOP_CHOICES = [
        ('Shell', 'Shell'),
        ('Bogie', 'Bogie'),
        ('Wheel', 'Wheel'),
        ('Paint', 'Paint'),
        ('Furnishing', 'Furnishing'),
        ('Electrical', 'Electrical'),
    ]

    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    shop = models.CharField(max_length=50, choices=SHOP_CHOICES)
    inspector_name = models.CharField(max_length=100)
    qci_date = models.DateField()
    cross_date = models.DateField(null=True, blank=True)
    accepted_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(blank=True)

    def __str__(self):
        return f"{self.coach} - {self.shop} ({self.qci_date})"

class Defect(models.Model):
    """Defect tracking for inspections"""
    DEFECT_CHOICES = [
        ('Welding Defect', 'Welding Defect'),
        ('Mismatch', 'Mismatch'),
        ('Fitment Issue', 'Fitment Issue'),
        ('Dimensional Deviation', 'Dimensional Deviation'),
        ('Material Defect', 'Material Defect'),
        ('Surface Finish Issue', 'Surface Finish Issue'),
        ('Paint Defect', 'Paint Defect'),
        ('Electrical Defect', 'Electrical Defect'),
        ('Functional Test Failure', 'Functional Test Failure'),
        ('Others', 'Others'),
    ]

    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE, related_name='defects')
    defect_type = models.CharField(max_length=100, choices=DEFECT_CHOICES)
    count = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.defect_type} ({self.count})"

class Attendance(models.Model):
    """Shop attendance tracking"""
    date = models.DateField()
    shop = models.CharField(max_length=50)
    present = models.IntegerField()
    absent = models.IntegerField()
    percent = models.FloatField()

    def __str__(self):
        return f"{self.shop} - {self.date}: {self.present}/{self.present + self.absent}"

class Feedback(models.Model):
    """User feedback system"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    feedback_type = models.CharField(max_length=50)
    text = models.TextField()

    def __str__(self):
        return f"Feedback by {self.user} on {self.date}"
