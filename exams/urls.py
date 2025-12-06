from django.urls import path
from . import views

urlpatterns = [
    path('student/login/', views.student_login, name='student_login'),
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/records/', views.get_all_records, name='get_all_records'),
    path('admin/records/<int:record_id>/', views.get_record, name='get_record'),
    path('admin/records/create/', views.create_record, name='create_record'),
    path('admin/records/<int:record_id>/update/', views.update_record, name='update_record'),
    path('admin/records/<int:record_id>/delete/', views.delete_record, name='delete_record'),
]
