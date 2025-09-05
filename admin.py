from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, ShopStrength, Coach, Inspection, Defect, Attendance, Feedback

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')

    fieldsets = BaseUserAdmin.fieldsets + (
        ('Role Information', {'fields': ('role',)}),
    )

@admin.register(ShopStrength)
class ShopStrengthAdmin(admin.ModelAdmin):
    list_display = ('shop_name', 'strength', 'updated_at')
    search_fields = ('shop_name',)

@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('sno', 'coach_type', 'coach_number', 'created_at')
    search_fields = ('coach_number', 'coach_type')
    list_filter = ('coach_type',)

class DefectInline(admin.TabularInline):
    model = Defect
    extra = 1

@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    list_display = ('coach', 'shop', 'inspector_name', 'qci_date')
    list_filter = ('shop', 'qci_date')
    search_fields = ('coach__coach_number', 'inspector_name')
    inlines = [DefectInline]

@admin.register(Defect)
class DefectAdmin(admin.ModelAdmin):
    list_display = ('inspection', 'defect_type', 'count')
    list_filter = ('defect_type',)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('date', 'shop', 'present', 'absent', 'percent')
    list_filter = ('shop', 'date')

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'feedback_type', 'date')
    list_filter = ('feedback_type', 'date')
    readonly_fields = ('date',)
