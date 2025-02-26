from rest_framework import serializers
from management.models.admin_auth import Groups
from management.models.menu import Menus
from management.serializers.menus import MenusSerializer

class GroupListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Groups
        fields = [ 'id', 'name',]

class GroupRetrieveSerializer(serializers.ModelSerializer):
    menu = serializers.SerializerMethodField()
    class Meta:
        model = Groups
        fields = [ 'id', 'name','menu', 'is_web_login_allowed']
    
    def get_menu(self, group):
        parent = group.menu.filter(parent=None).order_by('serial_number')
        serialize = MenusSerializer(parent,many=True, context={"group" :group })
        return serialize.data

class GroupSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    menu = serializers.CharField()
    class Meta:
        model = Groups
        fields = [ 'id', 'name','menu']
    
    def validate(self, data):
        group_id = data.get('id')
        name = data.get('name')
        if group_id:
            user = Groups.objects.get_or_none(id=group_id)
            if not user:
                    raise serializers.ValidationError({"group not exist"})

            isGroupExist = Groups.objects.exclude(id=group_id)\
            .filter(name=name).exists()
            if isGroupExist:
                raise serializers.ValidationError({'name':'group name already exist'})
        else:
            isGroupExist = Groups.objects.filter(name=name).exists()
            if isGroupExist:
                raise serializers.ValidationError({"name": 'group name already exist'})

        return super().validate(data)
   
    def create(self, validated_data):
        menu = validated_data.get('menu')
        group, created = Groups.objects.update_or_create(id=validated_data.get('id'),\
        defaults={'name':validated_data.get('name')})
        menu = Menus.objects.filter(id__in=menu.split(','))
        # group.menu.clear()
        group.menu.set(menu)
        group.save()
        return group