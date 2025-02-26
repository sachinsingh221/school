
from django.db import models
from django.conf import settings
from school_api.managers.school_models_manager import SchoolModelsManager

class Menus(models.Model):
    serial_number = models.FloatField(blank=True, null=True)
    parent =  models.ForeignKey('self', blank=True, null=True, related_name='sub_menu',
    on_delete=models.SET_NULL)
    key = models.CharField(max_length=225, blank=True, null=True)
    icon = models.CharField(max_length=225, blank=True, null=True)
    title = models.CharField(max_length=225, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='menu_created_by',
        on_delete=models.SET_NULL)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='menu_modified_by',
        on_delete=models.SET_NULL)

    objects = SchoolModelsManager()


class Xref_Groups_Menus(models.Model):
    groups = models.ForeignKey('Groups', blank=True, null=True, related_name='xref_groups_menu',
        on_delete=models.SET_NULL)
    menus = models.ForeignKey(Menus, blank=True, null=True, related_name='xref_groups_menu',
        on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='xref_groups_menu_created_by',
        on_delete=models.SET_NULL)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='xref_groups_menu_modified_by',
        on_delete=models.SET_NULL)