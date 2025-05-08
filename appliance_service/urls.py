"""
URL configuration for appliance_service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.conf import settings
# importing static module
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('guest.urls')),
    path('user/',include('user.urls',namespace='user')),
    path('administrator/',include('administrator.urls',namespace='administrator')),
    path('technician/',include('technician.urls',namespace='technician')),
]
# setting media and static root in the context of
# development server
"""if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL)
    document_root = settings.MEDIA_ROOT
    urlpatterns += static(settings.STATIC_URL)
    document_root = settings.STATIC_ROOT"""

if settings.DEBUG:  
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

