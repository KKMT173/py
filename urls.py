"""
URL configuration for WebsmartunityQR project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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

from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('M_login/', views.M_login_view, name='M_login'),
    path('WebsmartunityQR/', views.WebsmartunityQR, name='WebsmartunityQR'),
    path('generate_qr_code/', views.generate_qr_code, name='generate_qr_code'),
    path('adduser/', views.add_user, name='adduser'),
    path('userlist/', views.user_list_view, name='userlist'),
    path('userdelete/<int:user_id>/',views.userdelete, name='userdelete'),
    path('useredit/<int:user_id>/',views.edit_user_view, name='useredit'),
    path('logout/', views.logout_view, name='logout_view'),
    path('M_logout/', views.M_logout_view, name='M_logout_view'),
    path('get_checkboxes/<int:check_list_type_id>/', views.get_checkboxes, name='get_checkboxes'),
    path('checklist_form/<int:id>/', views.checklist_form, name='checklist_form'),
    path('M_checklist_form/<int:id>/', views.M_checklist_form, name='M_checklist_form'),
    path('listchecklist/', views.check_list_view, name='check_list_view'),
    path('checklist_report/<int:id>/', views.checklist_report, name='checklist_report'),
    path('M_checklist_report/<int:id>/', views.m_checklist_report, name='M_checklist_report'),
    path('M_back_checklist_form/<int:id>/', views.M_back_checklist_form, name='M_back_checklist_form'),
    path('check_action/', views.check_action_view, name='check_action'),
    path('check_action2/', views.check_action_view2, name='check_action2'),
    path('re_check_action/', views.re_check_action_view, name='re_check_action'),
    # path('unity_checklist/<int:checklist_id>/', views.unity_checklist, name='unity_checklist'),
    # path('process_checklist/', views.process_checklist, name='process_checklist'),
    # path('master/', views.master, name='master'),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)