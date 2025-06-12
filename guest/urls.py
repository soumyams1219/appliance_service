from django.urls import path,include
from . import views
from .views import *
app_name = 'guest'
urlpatterns = [
    # path('',views.index,name='index'),
    # path('login',views.login_view,name='login'),
    # path('verify-otp',views.verify_otp,name='verify-otp'),
    # path('register',views.register,name='register'),
    # path('logout/',views.logout_view,name='logout'),
    # path('user/',include('user.urls')),
    # path('administrator/',include('administrator.urls')),
    # path('role-creation',RoleListCreationAPIView.as_view(),name='role-creation'),
    # path('role-list',RoleListAPIView.as_view(),name='role-list'),
    # path('role/<int:pk>/',RoleRetrieveAPIView.as_view(),name='role-retrieve'),
    # path('role-update/<int:pk>/',RoleUpdateAPIView.as_view(),name='role-update'),
    # path('role-delete/<int:pk>/',RoleDeleteAPIView.as_view(),name='role-delete'),
    path('register/',RegisterAPIView.as_view(),name='register'),
    path('verify_otp/',VerifyotpAPIView.as_view(),name='verify_otp'),
    path('login/',LoginAPIView.as_view(),name='login'),
    path('logout/',LogoutAPIView.as_view(),name='logout'),
]