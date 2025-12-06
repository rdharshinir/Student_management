from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
import json

from .models import ExamRecord


def admin_dashboard(request):
    """Admin dashboard page with CRUD operations."""
    if not request.user.is_authenticated:
        return redirect('login')
    
    if request.user.username != 'Kgkite':
        return JsonResponse({'error': 'Unauthorized access'}, status=403)
    
    return render(request, 'admin_dashboard.html')


@csrf_exempt
@require_http_methods(["POST"])
def student_login(request):
    """Handle student login with Register Number and Date of Birth."""
    try:
        data = json.loads(request.body)
        register_no = data.get('register_no', '').strip().upper()
        date_of_birth = data.get('date_of_birth', '')
        
        if not register_no or not date_of_birth:
            return JsonResponse({
                'success': False,
                'error': 'Register Number and Date of Birth are required'
            }, status=400)
        
        # Parse date of birth
        try:
            dob = datetime.strptime(date_of_birth, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid date format. Use YYYY-MM-DD'
            }, status=400)
        
        # Query database for matching record
        try:
            exam_record = ExamRecord.objects.get(
                register_no=register_no,
                date_of_birth=dob
            )
            
            # Return student data
            return JsonResponse({
                'success': True,
                'data': {
                    'record': exam_record.record,
                    'register_no': exam_record.register_no,
                    'student_name': exam_record.student_name,
                    'course_code': exam_record.course_code,
                    'course_title': exam_record.course_title,
                    'exam_date': exam_record.exam_date.strftime('%Y-%m-%d'),
                    'exam_session': exam_record.exam_session,
                    'exam_hall_number': exam_record.exam_hall_number,
                    'exam_seat_number': exam_record.exam_seat_number,
                }
            })
        except ExamRecord.DoesNotExist:
            return JsonResponse({
                'success': False,
                'error': 'No record found with the provided Register Number and Date of Birth'
            }, status=404)
        except ExamRecord.MultipleObjectsReturned:
            # If multiple records exist, return the first one
            exam_record = ExamRecord.objects.filter(
                register_no=register_no,
                date_of_birth=dob
            ).first()
            return JsonResponse({
                'success': True,
                'data': {
                    'record': exam_record.record,
                    'register_no': exam_record.register_no,
                    'student_name': exam_record.student_name,
                    'course_code': exam_record.course_code,
                    'course_title': exam_record.course_title,
                    'exam_date': exam_record.exam_date.strftime('%Y-%m-%d'),
                    'exam_session': exam_record.exam_session,
                    'exam_hall_number': exam_record.exam_hall_number,
                    'exam_seat_number': exam_record.exam_seat_number,
                }
            })
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def admin_login(request):
    """Handle admin login."""
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        password = data.get('password', '')
        
        if not username or not password:
            return JsonResponse({
                'success': False,
                'error': 'Username and password are required'
            }, status=400)
        
        # Authenticate user
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_active:
            login(request, user)
            return JsonResponse({
                'success': True,
                'message': 'Login successful',
                'redirect_url': '/api/admin/dashboard/'
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Invalid credentials'
            }, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def get_all_records(request):
    """Get all exam records (Admin only)."""
    if not request.user.is_authenticated or request.user.username != 'Kgkite':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    records = ExamRecord.objects.all().order_by('-exam_date', 'register_no')
    data = [{
        'record': r.record,
        'register_no': r.register_no,
        'student_name': r.student_name,
        'course_code': r.course_code,
        'course_title': r.course_title,
        'exam_date': r.exam_date.strftime('%Y-%m-%d'),
        'exam_session': r.exam_session,
        'exam_hall_number': r.exam_hall_number,
        'exam_seat_number': r.exam_seat_number,
        'date_of_birth': r.date_of_birth.strftime('%Y-%m-%d') if r.date_of_birth else None,
    } for r in records]
    
    return JsonResponse({'success': True, 'data': data})


@csrf_exempt
@require_http_methods(["GET"])
def get_record(request, record_id):
    """Get a single exam record by ID."""
    if not request.user.is_authenticated or request.user.username != 'Kgkite':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        record = ExamRecord.objects.get(record=record_id)
        return JsonResponse({
            'success': True,
            'data': {
                'record': record.record,
                'register_no': record.register_no,
                'student_name': record.student_name,
                'course_code': record.course_code,
                'course_title': record.course_title,
                'exam_date': record.exam_date.strftime('%Y-%m-%d'),
                'exam_session': record.exam_session,
                'exam_hall_number': record.exam_hall_number,
                'exam_seat_number': record.exam_seat_number,
                'date_of_birth': record.date_of_birth.strftime('%Y-%m-%d') if record.date_of_birth else None,
            }
        })
    except ExamRecord.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Record not found'}, status=404)


@csrf_exempt
@require_http_methods(["POST"])
def create_record(request):
    """Create a new exam record."""
    if not request.user.is_authenticated or request.user.username != 'Kgkite':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        data = json.loads(request.body)
        
        # Parse date fields
        exam_date = datetime.strptime(data['exam_date'], '%Y-%m-%d').date()
        date_of_birth = None
        if data.get('date_of_birth'):
            date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        
        record = ExamRecord.objects.create(
            register_no=data['register_no'].strip().upper(),
            student_name=data['student_name'],
            course_code=data['course_code'],
            course_title=data['course_title'],
            exam_date=exam_date,
            exam_session=data['exam_session'],
            exam_hall_number=data['exam_hall_number'],
            exam_seat_number=data['exam_seat_number'],
            date_of_birth=date_of_birth,
        )
        
        return JsonResponse({
            'success': True,
            'message': 'Record created successfully',
            'data': {
                'record': record.record,
                'register_no': record.register_no,
                'student_name': record.student_name,
            }
        }, status=201)
        
    except KeyError as e:
        return JsonResponse({
            'success': False,
            'error': f'Missing required field: {str(e)}'
        }, status=400)
    except ValueError as e:
        return JsonResponse({
            'success': False,
            'error': f'Invalid date format: {str(e)}'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["PUT"])
def update_record(request, record_id):
    """Update an existing exam record."""
    if not request.user.is_authenticated or request.user.username != 'Kgkite':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        record = ExamRecord.objects.get(record=record_id)
        data = json.loads(request.body)
        
        # Update fields if provided
        if 'register_no' in data:
            record.register_no = data['register_no'].strip().upper()
        if 'student_name' in data:
            record.student_name = data['student_name']
        if 'course_code' in data:
            record.course_code = data['course_code']
        if 'course_title' in data:
            record.course_title = data['course_title']
        if 'exam_date' in data:
            record.exam_date = datetime.strptime(data['exam_date'], '%Y-%m-%d').date()
        if 'exam_session' in data:
            record.exam_session = data['exam_session']
        if 'exam_hall_number' in data:
            record.exam_hall_number = data['exam_hall_number']
        if 'exam_seat_number' in data:
            record.exam_seat_number = data['exam_seat_number']
        if 'date_of_birth' in data:
            if data['date_of_birth']:
                record.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
            else:
                record.date_of_birth = None
        
        record.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Record updated successfully',
            'data': {
                'record': record.record,
                'register_no': record.register_no,
                'student_name': record.student_name,
            }
        })
        
    except ExamRecord.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Record not found'}, status=404)
    except ValueError as e:
        return JsonResponse({
            'success': False,
            'error': f'Invalid date format: {str(e)}'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_record(request, record_id):
    """Delete an exam record."""
    if not request.user.is_authenticated or request.user.username != 'Kgkite':
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    try:
        record = ExamRecord.objects.get(record=record_id)
        record.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Record deleted successfully'
        })
        
    except ExamRecord.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Record not found'}, status=404)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
