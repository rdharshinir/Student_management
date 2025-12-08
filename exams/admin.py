from django.contrib import admin
from .models import ExamRecord, SystemConfig


@admin.register(ExamRecord)
class ExamRecordAdmin(admin.ModelAdmin):
    list_display = ('record', 'register_no', 'student_name', 'course_code', 'course_title', 'exam_date', 'exam_session')
    list_filter = ('exam_date', 'exam_session', 'course_code')
    search_fields = ('register_no', 'student_name', 'course_code', 'course_title')
    readonly_fields = ('record',)
    ordering = ('-exam_date', 'register_no')


@admin.register(SystemConfig)
class SystemConfigAdmin(admin.ModelAdmin):
    list_display = ('id', 'live_enabled')
    readonly_fields = ('id',)
