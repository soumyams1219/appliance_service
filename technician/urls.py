from django.urls import path,include
from . import views
app_name = 'technician'
urlpatterns = [
    path('',views.home,name='home'),
    path('finish-request/<int:id>/',views.finish_request,name='finish-request'),
]