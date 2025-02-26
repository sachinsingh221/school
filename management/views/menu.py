from school_api.enums import ResponseStatus
from rest_framework.response import Response
from rest_framework import generics
from management.authentications.management_jwt import ManagementJWT
from management.models.menu import Menus
from management.serializers.menus import MenusSerializer


class MenuListApiView(generics.ListAPIView):
  
    serializer_class = MenusSerializer
    # permission_classes = [IsAuthenticated,]
    authentication_classes = [ManagementJWT]
    pagination_class = None

    def get_queryset(self):
        return Menus.objects.filter(parent=None)
        
    def get(self, request):

        success_array = []
        error_array = []
        data = []
        status = ResponseStatus.ERROR

        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data
        status = ResponseStatus.SUCCESS
        

        return Response({
        'status': status,
        'error': error_array,
        'success': success_array,
        'data': data
        })

class MenuRetriveApiView(generics.RetrieveAPIView):
    queryset = Menus.objects.all() 
    serializer_class = MenusSerializer
    authentication_classes = [ManagementJWT]
    
    # def get_serializer_context(self):
    #     context = super(MenuRetriveApiView, self).get_serializer_context()
    #     context.update({"menu": self.get_object()})
    #     return context

    def retrieve(self, request, *args, **kwargs):

        success_array = []
        error_array = []
        data = []
        status = ResponseStatus.ERROR

        menu = self.get_object()

        # parent_menu = menu.menu.filter(parent=None)
        serializer = self.get_serializer(menu)
        data = serializer.data  
        status = ResponseStatus.SUCCESS
        

        return Response({
        'status': status,
        'error': error_array,
        'success': success_array,
        'data': data
        })
