from management.models.admin_auth import Groups
from management.models.menu import Menus
from management.serializers.group import (GroupListSerializer,GroupRetrieveSerializer)
from school_api.enums import ResponseStatus
from management.authentications.management_jwt import ManagementJWT
from rest_framework.response import Response
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from management.filters.management import ManagementGroupsFilter
from management.serializers.group import GroupSerializer
from rest_framework.views import APIView


class GroupAPIView(APIView):
    serializer_class = GroupSerializer
    def post(self, request):

        success_array = []
        error_array = []
        data = []
        status = ResponseStatus.ERROR
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        status = ResponseStatus.SUCCESS
        data = serializer.data
        if request.data.get('id'):
            success_array.append('group is updated succesfully')
        else:
            success_array.append('group is created succesfully')
         
        return Response({
        'status': status,
        'error': error_array,
        'success': success_array,
        'data': data
        })

class GroupListApiView(generics.ListAPIView):
    queryset = Groups.objects.all()
    serializer_class = GroupListSerializer
    # permission_classes = [IsAuthenticated,]
    authentication_classes = [ManagementJWT]
    pagination_class = None
    filter_backends = [DjangoFilterBackend,OrderingFilter]
    filter_class = ManagementGroupsFilter
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

class GroupRetrieveApiView(generics.RetrieveAPIView):
    queryset = Groups.objects.all()
    serializer_class = GroupRetrieveSerializer
    # permission_classes = [IsAuthenticated,]
    authentication_classes = [ManagementJWT]

    def retrieve(self, request, *args, **kwargs):
        success_array = []
        error_array = []
        data = []
        status = ResponseStatus.ERROR

        group = self.get_object()
        serializer = self.get_serializer(group)
        data = serializer.data
        status = ResponseStatus.SUCCESS
        

        return Response({
        'status': status,
        'error': error_array,
        'success': success_array,
        'data': data
        })

        