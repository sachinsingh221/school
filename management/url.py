from django.urls import path
from management.views.management import (ManagementUserLoginAPIView,
                                         ManagementUserListApiView, ManagementUserRetrieveApiView, ManagementUserRegistrationAPIView,
                                         ManagementUserPasswordResetApiView)
from management.views.group import GroupListApiView
from management.views.group import GroupRetrieveApiView, GroupAPIView
from management.views.menu import MenuRetriveApiView, MenuListApiView

urlpatterns = [
    path('management/login', ManagementUserLoginAPIView.as_view()),
    path('management/register', ManagementUserRegistrationAPIView.as_view()),
    path('management/users', ManagementUserListApiView.as_view()),
    path('management/users/<int:pk>', ManagementUserRetrieveApiView.as_view()),
    path('management/user/password-reset',
         ManagementUserPasswordResetApiView.as_view()),
    path('management/group/create', GroupAPIView.as_view()),
    path('management/groups', GroupListApiView.as_view()),
    path('management/groups/<int:pk>', GroupRetrieveApiView.as_view()),
    path('management/menus', MenuListApiView.as_view()),
    path('management/menus/<int:pk>', MenuRetriveApiView.as_view()),
]
