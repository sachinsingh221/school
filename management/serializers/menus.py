from rest_framework import serializers
from management.models.menu import Menus, Xref_Groups_Menus

class SubMenusSerializer(serializers.ModelSerializer):
    key = serializers.CharField()
    label = serializers.CharField(source='title')
    leftIcon = serializers.CharField(source='icon')
    class Meta:
        model = Menus
        fields = ['id','key', 'label', 'leftIcon']

class MenusSerializer(serializers.ModelSerializer):
    label = serializers.CharField(source='title')
    leftIcon = serializers.CharField(source='icon')
    children = serializers.SerializerMethodField()
    class Meta:
        model = Menus
        fields = ['id','key', 'label', 'leftIcon', 'children']
    
    def get_children(self, parent):
        group = self.context.get("group")
        if(group):
            sub_menu = group.menu.filter(parent=parent).order_by('serial_number')
        else:
            sub_menu = Menus.objects.filter(parent=parent)
        serailizer = SubMenusSerializer(sub_menu, many=True)
        return serailizer.data
