from django.urls import path
from groups.models import Group,GroupMember
from groups.views import CreateGroup,ListGroup,SingleGroup,JoinGroup,LeaveGroup
app_name = 'groups'

urlpatterns = [
    path('create/',CreateGroup.as_view(),name='create'),
    path('',ListGroup.as_view(),name='all'),
    path('posts/in/<slug>/',SingleGroup.as_view(),name='single'),
    path("join/<slug>/",JoinGroup.as_view(),name="join"),
    path("leave/<slug>/",LeaveGroup.as_view(),name="leave"),
]
