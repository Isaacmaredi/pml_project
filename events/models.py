from django.db import models
from django.db import models
from django.contrib.auth.models import User
from pmlprofile.models import Profile, Beneficiary
from datetime import datetime, date
from django.urls import  reverse

class Meeting(models.Model):
    date = models.DateField()
    
    MEETINGS = [
        ('Quartely Meeting','Quartely Meeting'),
        ('Special Meeting','Special Meeting'),
        ('Year-end Function','Year-end Function'),
        ('Extraordinary Meeting','Extraordinary Meeting'),  
    ]
    meeting_type = models.CharField(max_length=200, choices=MEETINGS)
    host = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    alt_venue = models.CharField(max_length=300,blank=True, null=True)
    
    def __str__(self):
        return f'{self.meeting_type} held on {self.date}'

class Funeral(models.Model):
    date = models.DateField()
    bereaved_member = models.ForeignKey(Profile, on_delete=models.CASCADE)
    DECEASED_TYPE = [
        ('Member','Member') ,
        ('Beneficiary','Beneficiary'),
    ]
    deceased_type = models.CharField(max_length=100, choices=DECEASED_TYPE)
    deceased_member = models.OneToOneField(User,on_delete=models.CASCADE, null=True, blank=True)
    deceased_beneficiary = models.OneToOneField(Beneficiary, on_delete=models.CASCADE, null=True,blank=True)
    # deceased_member = models.OneToOneField(Profile, on_delete=models.CASCADE, null=True, blank=True)
    venue = models.CharField(max_length=200)
    
    def __str__(self):
        return f'{self.date} at {self.venue}' 

class FuneralAttendance(models.Model):
    funeral = models.ForeignKey(Funeral, on_delete=models.CASCADE, related_name='attendances')
    member= models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='members')
    is_present = models.BooleanField(default=True)
    ABSENCE = [
        ('Family Commitment','Family Commitment'),
        ('Ill-Health','Ill-Health'),
        ('Work Commitment','Work Commitment'),
        ('Funeral Attendance','Funeral Attendance'),
    ]
    absence_reason = models.CharField(choices=ABSENCE, max_length=300, null=True, blank=True)
    
    def __str__(self):
        return f'Attendace of {self.funeral}\'s funeral - Member: {self.member} - Present: {self.is_present}'
    
class Attendance(models.Model):
    meeting = models.ForeignKey(Meeting, on_delete=models.CASCADE, related_name='attendances')
    member= models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='member')
    is_present = models.BooleanField(default=True)
    ABSENCE = [
        ('Family Commitment','Family Commitment'),
        ('Ill-Health','Ill-Health'),
        ('Work Commitment','Work Commitment'),
        ('Funeral Attendance','Funeral Attendance'),
    ]
    absence_reason = models.CharField(choices=ABSENCE, max_length=300, null=True, blank=True)
    
    def __str__(self):
        return f'{self.meeting} Member: {self.member} - Present: {self.is_present}'