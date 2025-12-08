from django.db import models
from django.core.validators import RegexValidator


class ExamRecord(models.Model):
    """Model for storing exam records with all required fields."""
    
    record = models.AutoField(primary_key=True, db_column='Record')
    register_no = models.CharField(
        max_length=50,
        db_column='RegisterNo',
        validators=[RegexValidator(regex=r'^[A-Z0-9]+$', message='Register number must be alphanumeric')],
        help_text='Student registration number'
    )
    student_name = models.CharField(
        max_length=200,
        db_column='StudentName',
        help_text='Full name of the student'
    )
    course_code = models.CharField(
        max_length=20,
        db_column='Coursecode',
        help_text='Course code identifier'
    )
    course_title = models.CharField(
        max_length=200,
        db_column='CourseTitle',
        help_text='Full title of the course'
    )
    exam_date = models.DateField(
        db_column='ExamDate',
        help_text='Date of the examination'
    )
    exam_session = models.CharField(
        max_length=50,
        db_column='ExamSession',
        help_text='Session of the exam (e.g., Morning, Afternoon)'
    )
    exam_hall_number = models.CharField(
        max_length=20,
        db_column='ExamHallNumber',
        help_text='Hall number where exam is conducted'
    )
    exam_seat_number = models.CharField(
        max_length=20,
        db_column='ExamSeatNumber',
        help_text='Seat number assigned to the student'
    )
    date_of_birth = models.DateField(
        db_column='DateOfBirth',
        null=True,
        blank=True,
        help_text='Date of birth for authentication'
    )

    class Meta:
        db_table = 'ExamRecord'
        verbose_name = 'Exam Record'
        verbose_name_plural = 'Exam Records'
        indexes = [
            models.Index(fields=['register_no'], name='idx_register_no'),
            models.Index(fields=['exam_date'], name='idx_exam_date'),
        ]

    def __str__(self):
        return f"{self.register_no} - {self.student_name} - {self.course_code}"


class SystemConfig(models.Model):
    live_enabled = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # enforce a single-row singleton by always using pk=1
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_solo(cls):
        # returns the singleton instance, creating it if necessary
        obj, created = cls.objects.get_or_create(pk=1, defaults={'live_enabled': False})
        return obj

    def __str__(self):
        return f"Live Mode: {'ON' if self.live_enabled else 'OFF'}"

    class Meta:
        verbose_name = "System Configuration"
        verbose_name_plural = "System Configuration"
