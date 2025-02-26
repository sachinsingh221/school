from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from management.models.admin_auth import AdminAuth
from management.serializers.management import (ManagementUserLoginSerializer,
                                               ManagementUserListSerializer, ManagementUserRegistrationSerializer,
                                               ManagementUserRetrieveUpdateDynamicSerializer, ManagementUserPasswordResetSerializer)
from management.filters.management import ManagementUsersFilter
from school_api.enums import ResponseStatus
from management.authentications.management_jwt import ManagementJWT
from management.paginations.management import ManagementUsersPagination
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from django.utils import timezone
import os
from xml.dom import minidom
import datetime
# from ..renderers.consumer import consumerJSONRenderer


class ManagementUserLoginAPIView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = ManagementUserLoginSerializer
    #renderer_classes = (CustomerJSONRenderer,)

    def post(self, request):
        success, error, data, status = [], [], [], ResponseStatus.ERROR
        #user = request.data.get('user', {})

        # Notice here that we do not call `serializer.save()` like we did for
        # the registration endpoint. This is because we don't  have
        # anything to save. Instead, the `validate` method on our serializer
        # handles everything we need.
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.data
        success.append('login sucessfully')
        status = ResponseStatus.SUCCESS
        return Response({
            'status': status,
            'error': error,
            'success': success,
            'data': data
        })

class ManagementUserRegistrationAPIView(APIView):
    """Allow any user (authenticated or not) to hit this endpoint."""

    serializer_class = ManagementUserRegistrationSerializer
    permission_classes = (AllowAny,)
    #renderer_classes = (consumerJSONRenderer,)

    def post(self, request):
        success_array, error_array, data, status = [], [], [], ResponseStatus.ERROR
        #user = request.data.get('user', {})

        # The create serializer, validate serializer, save serializer pattern
        # below is common and you will see it a lot throughout this course and
        # your own work later on. Get familiar with it.
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status = ResponseStatus.SUCCESS
        if request.data.get('id'):
            success_array.append('user is updated succesfully')
        else:
            success_array.append('user is created succesfully')

        return Response({
            'status': status,
            'error': error_array,
            'success': success_array,
            'data': data
        })


class ManagementUserListApiView(generics.ListAPIView):
    queryset = AdminAuth.objects.all()
    serializer_class = ManagementUserListSerializer
    # permission_classes = [IsAuthenticated,]
    authentication_classes = [ManagementJWT]
    pagination_class = ManagementUsersPagination
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_class = ManagementUsersFilter
    ordering_fields = ['first_name']
    ordering = ['-created_at']

    def get(self, request):

        success_array = []
        error_array = []
        data = []
        status = ResponseStatus.ERROR

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            result = self.get_paginated_response(serializer.data)
            data = result.data
            status = ResponseStatus.SUCCESS
        else:
            serializer = self.get_serializer(queryset, many=True)
            data = serializer.data
            status = ResponseStatus.SUCCESS

        return Response({
            'status': status,
            'error': error_array,
            'success': success_array,
            'data': data
        })


class ManagementUserRetrieveApiView(generics.RetrieveUpdateAPIView):
    queryset = AdminAuth.objects.all()
    serializer_class = ManagementUserRetrieveUpdateDynamicSerializer
    # permission_classes = [IsAuthenticated,]
    authentication_classes = [ManagementJWT]

    def retrieve(self, request, *args, **kwargs):

        success_array, error_array, data, status, instance = [], [], [], ResponseStatus.ERROR, self.get_object()
        serializer = self.get_serializer(instance=instance)
        data = serializer.data
        status = ResponseStatus.SUCCESS

        return Response({
            'status': status,
            'error': error_array,
            'success': success_array,
            'data': data
        })

    def update(self, request, *args, **kwargs):

        success_array = []
        error_array = []
        data = []
        status = ResponseStatus.ERROR

        serializer_data = request.data

        # Here is that serialize, validate, save pattern we talked about
        # before.
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        data = serializer.data

        return Response({
            'status': status,
            'error': error_array,
            'success': success_array,
            'data': data
        })


class ManagementUserPasswordResetApiView(APIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ManagementUserPasswordResetSerializer
    model = AdminAuth
    # permission_classes = [IsAuthenticated]
    authentication_classes = [ManagementJWT]

    def post(self, request, *args, **kwargs):

        success = []
        error = []
        data = []
        status = ResponseStatus.ERROR

        instance = self.model.objects.get_or_none(id=request.data.get('id'))
        serializer = self.serializer_class(
            instance=instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        status = ResponseStatus.SUCCESS
        success.append(f'password is updated for user {instance.email}')

        return Response({
            'status': status,
            'error': error,
            'success': success,
            'data': data
        })

