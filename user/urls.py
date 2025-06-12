from django.urls import path,include
from . import views
from .views import *
app_name = 'user'
urlpatterns = [
    # path('',views.home,name='home'),
    # path('view-requests',views.view_requests,name='view-requests'),
    # path('track-status',views.track_status,name='track-status'),
    # path('request-creation',servicerequestCreationAPIView.as_view(),name='request-creation')
    path('service/list/',ServiceListAPIView.as_view(),name='service-list'),
    path('service/create/', ServiceCreateAPIView.as_view(), name='service-create'),
]