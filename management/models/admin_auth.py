import jwt
from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from management.exceptions import custom_exceptions
from school_api.managers.school_models_manager import SchoolModelsManager


class Groups(models.Model):
    menu = models.ManyToManyField('Menus', blank=True, through='Xref_Groups_Menus',
    related_name='groups')
    name = models.CharField(max_length=128)
    is_web_login_allowed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    description = models.CharField(max_length=128, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='UserGroup_created_by',
        on_delete=models.SET_NULL)
    modified_at = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, blank=True, null=True, related_name='UserGroup_modified_by',
        on_delete=models.SET_NULL)

    objects=SchoolModelsManager()


class UserManager(BaseUserManager):

    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`.

    All we have to do is override the `create_user` function which we will use
    to create `user` objects.
    """

    def create_user(self, email, group_id, id=None, mobile_number=None,
    name=None, username=None, password=None):
        """Create and return a `User` with an email, mobile number and password."""

        # if mobile_number is None:
        #     raise TypeError('User must have a mobile number.')

        if email is None:
            raise TypeError('User must have an email address.')

        if id:
            user = self.get_or_none(id=id)
            if user:
                user.email = self.normalize_email(email)
                user.mobile_number = mobile_number
                user.username = username
                user.name = name
                user.group = group_id
            else:
                raise TypeError('plese provide valid user')
        else:
            user = self.model(email=self.normalize_email(email),mobile_number=mobile_number,
            name=name,username=username,group=group_id)
            user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        """
        Create and return a `User` with superuser (user) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(email, password)
        user.is_superuser = True
        user.save()

        return user

    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except self.model.DoesNotExist:
            return None

class AdminAuth(AbstractBaseUser, PermissionsMixin):
    group = models.ForeignKey(Groups, blank=True, null=True, related_name='users',
        on_delete=models.SET_NULL)
    name = models.CharField(max_length=128)
    device_id = models.CharField(blank=True, null=True,max_length=128)
    username = models.CharField(db_index=True, unique=True, max_length=255,)
    mobile_number = PhoneNumberField()
    email = models.EmailField(db_index=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def get_full_name(self):
        return self.username

    def get_mobile_number(self):
        return self.mobile_number

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        
        dt = timezone.now() + timedelta(days=60)


        token = jwt.encode({
            'email': self.email,
            # int(dt.strftime('%S'))
            'device_id': str(self.device_id),
            'exp': int(dt.timestamp())  # str(time.mktime(dt.timetuple()))[:-2]
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    def setDeviceId(self, device_id=None):
        self.device_id = device_id

    def validate_devid(self,requested_devid):
        if not self.device_id:
            raise custom_exceptions.ClientException('Device id was not saved') 
        if not (self.device_id == requested_devid):
            raise custom_exceptions.ClientException('Invalid device id')
        return True