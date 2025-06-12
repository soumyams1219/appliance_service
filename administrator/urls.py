# from django.urls import path,include
# from . import views
app_name = 'administrator'

# urlpatterns = [
#     path('',views.home,name='home'),
#     path('view-requests',views.view_requests,name='view-requests'),
#     path('add-issues',views.add_issues,name='add-issues'),
#     path('edit_product',views.edit_product,name='edit_product'),
#     path('edit_product/<int:id>/',views.edit_product,name='edit_product'),
#     path('delete_product/<int:id>/',views.delete_product,name='delete_product'),
#     path('edit_issue',views.edit_issue,name='edit_issue'),
#     path('edit_issue/<int:id>/',views.edit_issue,name='edit_issue'),
#     path('delete_issue/<int:id>/',views.delete_issue,name='delete_issue'),
#     path('add-technician',views.add_technician,name='add-technician'),
#     path('edit-technician', views.edit_technician, name='edit-technician'),
#     path('edit-technician/<int:id>/', views.edit_technician, name='edit-technician'),
#     path('delete-technician/<int:id>/',views.delete_technician,name='delete-technician'),
#     path('reject-request/<int:id>/',views.reject_request,name='reject-request'),
#     path('accept-request',views.accept_request,name='accept-request'),
#     path('accept-request/<int:id>/',views.accept_request,name='accept-request'),
#     path('schedule-request',views.schedule_request,name='schedule-request'),
#     path('view-all-requests',views.view_all_requests,name='view-all-requests'),
# ]
from django.urls import path
from .views import *

urlpatterns = [
    path('product/',ProductCreateLIstAPIView.as_view(),name='product'),
    path('product/<int:pk>/',ProductRetrieveUpdateDeleteAPIView.as_view(),name='product-details'),
    path('issue/',IssueCreateListAPIView.as_view(),name='issue'),
    path('issue/<int:pk>/',IssueRetrieveUpdateDeleteAPIView.as_view(),name='issue-details'),
    path('technicians/',TechnicianCreateListAPIView.as_view(),name='technician-createlist'),
    path('technicians/<int:pk>/',TechnicianRetrieveUpdateDelete.as_view(),name='technician-details'),
    path('service/',ServiceListAPIView.as_view(),name='service-pending'),
    path('service/all/',ServiceListAllAPIView.as_view(),name='service-all'),
    path('service/reject/<int:pk>/',ServiceRejectAPIView.as_view(),name='service-reject'),
    path('service/accept/<int:pk>/',ServiceAcceptAPIView.as_view(),name='service-accept'),
    path('service/schedule/<int:pk>/',ServiceScheduleAPIView.as_view(),name='service-schedule'),
]