import django_filters
from management.models.admin_auth import AdminAuth, Groups

class ManagementUsersFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(lookup_expr='icontains')
    group_name = django_filters.CharFilter(field_name='group__name',lookup_expr='iexact')
    class Meta:
        model = AdminAuth
        fields = ['email','group', 'group_name']


class ManagementGroupsFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Groups
        fields = ['name']