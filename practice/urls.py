"""practice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from practice_app import views

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login', views.userLogin, name='login'),
    path('loginAttempt', views.loginAttempt, name='loginAttempt'),
    path('logout', views.userLogout, name='logout'),
    path('home', views.home, name='home'),
    path('', views.index, name='index'),
    path('add', views.add, name='add'),
    path('edit/<int:id>', views.edit, name='edit'),
    path('update/<int:id>', views.update, name='update'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('details/<int:id>', views.details, name='details'),
#    path('details/<str:name>', views.details, name='details'),
    path('details/profile/<int:id>', views.profile, name='profile'),
    path('oauth/', include('social_django.urls', namespace="social")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
