from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView,DetailView                             
from django.views.generic.edit import UpdateView, CreateView
from .models import Meeting, Attendance, Funeral, FuneralAttendance

# Create your views here.

class MeetingList(ListView):
    model = Meeting
    context_object_name = 'meetings'
    template_name = 'events/meeting_list.html'
    
    ordering = ['-date',]
    
class FuneralList(ListView):
    model = Funeral
    context_object_name = 'funerals'
    template_name = 'events/funerals.html'


class MeetingDetail(DetailView):
    model = Meeting
    context_object_name = 'meeting'
    template_name = 'events/meeting_detail.html'

class MeetingCreateView(CreateView):
    model = Meeting
    success_url = reverse_lazy('events:meetings')
    fields = ('date','meeting_type','host','alt_venue')
    template_name = 'events/meeting_create.html'

class AttendanceListView(ListView):
    model = Attendance 
    context_object_name = 'register'
    template_name = 'events/meeting_attendance.html'
    
    def get_context_data(self,*args, **kwargs):
        context = super(AttendanceListView, self).get_context_data(*args,**kwargs)
        context['absent'] = Attendance.objects.filter(is_present='False')
        context['present'] = Attendance.objects.filter(is_present='True')
        return context
        
        # context['qmeeting'] = Attendance.objects.filter(meeting_type='Quarterly Meeting')
        
