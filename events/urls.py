from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('meeting_list/',views.MeetingList.as_view(), name='meetings'),
    path('meeting_detail/<int:pk>/',views.MeetingDetail.as_view(), name='meeting'),
    path('meeting_create/',views.MeetingCreateView.as_view(), name='meeting_create'),
    # path('meeting_update/',views.MeetingUpdate.as_view(), name='meeting_update'),   
    path('attendance/<int:pk>/',views.AttendanceListView.as_view(), name='attendance'),
    path('funerals/',views.FuneralList.as_view(), name='funerals'),
]