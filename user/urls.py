from django.urls import path,include
from . import views
app_name = 'user'
urlpatterns = [
    path('',views.home,name='home'),
    path('view-requests',views.view_requests,name='view-requests'),
    path('track-status',views.track_status,name='track-status'),
]