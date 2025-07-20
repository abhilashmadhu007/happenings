"""
URL configuration for nightClub project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from nightapp import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('user_reg/',views.user_reg,name='user_reg'),
    path('club_reg/',views.club_reg,name='club_reg'),
    path('login/',views.user_login,name='login'),
    path('adminhome/',views.adminhome,name='adminhome'),
    path('userhome/',views.userhome,name='userhome'),
    path('clubhome/',views.clubhome,name='clubhome'),
    path('user_profile_update/',views.user_profile_update,name='user_profile_update'),
    path('club_profile_update/',views.club_profile_update,name='club_profile_update'),
    path('club_add_event/',views.club_add_event,name='club_add_event'),
    path('events/', views.view_and_book_events, name='view_and_book_events'),
    path('payment/', views.payment, name='payment'),
    path('confirm_booking/', views.confirm_booking, name='confirm_booking'),
    path('booking_history/', views.booking_history, name='booking_history'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('admin_user_management/', views.admin_user_management, name='admin_user_management'),
    path('admin_club_management/', views.admin_club_management, name='admin_club_management'),
    path('admin_booking_review/', views.admin_booking_overview, name='admin_booking_overview'),
    path('user_logout/',views.user_logout, name='user_logout'),
]
