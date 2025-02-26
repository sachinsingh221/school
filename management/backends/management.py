from django.contrib.auth.backends import BaseBackend
from rest_framework import exceptions
from management.models import AdminAuth
from django.contrib.auth import get_user_model

UserModel = get_user_model()

class ManagementBackend(BaseBackend):

    def authenticate(self, request, username=None, password=None,  device_id=None,**kwargs):
        username = kwargs.get(UserModel.USERNAME_FIELD) if username is None else username
        if username is None or (not device_id and password is None):
            return
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if device_id:
                if not password and user.device_id:
                   return (user if user.validate_devid(device_id) else None)      
                else:
                    if user.check_password(password) and self.user_can_authenticate(user):
                        user.setDeviceId(device_id), user.save() 
                        return user
                    else:
                        return
            else:   
                return (user if user.check_password(password) and self.user_can_authenticate(user) else None)

    def user_can_authenticate(self, user):
        """
        Reject users with is_active=False. Custom user models that don't have
        that attribute are allowed.
        """
        is_active = getattr(user, 'is_active', None)
        return is_active or is_active is None

