"""CHATBOT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf.urls.static import static
from appbase import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin-app/',include("appadmins.urls")),
    path('client-app/',include("appclient.urls")),
    path("",views.index,name="index"),
    path("sign-in/",views.login,name="sign-in"),
    path("sign-up/",views.register,name="sign-up"),
    path("logout/",views.logout,name="logout"),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
