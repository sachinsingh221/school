from rest_framework import serializers
from management.models.admin_auth import AdminAuth,Groups
from management.serializers.menus import MenusSerializer
from phonenumber_field.serializerfields import PhoneNumberField
from django.contrib.auth import authenticate
from school_api.serializers.dynamic_field_model_serializer import DynamicFieldsModelSerializer
class ManagementUserLoginSerializer(serializers.Serializer):
    """Serializers Login requests and login a managementuser."""

    id = serializers.IntegerField(read_only=True)
    group_id = serializers.PrimaryKeyRelatedField(read_only=True)
    username = serializers.CharField(max_length=255)
    email = serializers.CharField(max_length=255,read_only=True)
    password = serializers.CharField(max_length=128,required=False, write_only=True)
    device_id = serializers.CharField( required=False,max_length=255, write_only=True, allow_null=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # The `validate` method is where we make sure that the current
        # instance of `CompanyUserLoginSerializer` has "valid". In the case of logging a
        # CompanyUser in, this means validating that they've provided an username
        # and password and that this combination matches one of the CompanyUsers in
        # our database.
        username, password, device_id = data.get('username'), data.get('password'), data.get('device_id')

        # Raise an exception if an
        # username is not provided.
        if username is None:
            raise serializers.ValidationError(
                'a username is required to log in.'
            )

        # Raise an exception if a
        # password is not provided.
        if not device_id and password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a CompanyUser that matches this username/password combination. Notice how
        # we pass `username` as the `username` value since in our CompanyUser
        # model we set `USERNAME_FIELD` as `username`.
        adminAuth = authenticate(username=username, password=password, device_id=device_id)

        # If no CompanyUser was found matching this username/password combination then
        # `authenticate` will return `None`. Raise an exception in this case.
        if adminAuth is None:
            raise serializers.ValidationError(
                'A User with this username and password was not found.'
            )

        # Django provides a flag on our `CompanyUser` model called `is_active`. The
        # purpose of this flag is to tell us whether the CompanyUser has been banned
        # or deactivated. This will almost never be the case, but
        # it is worth checking. Raise an exception in this case.
        if not adminAuth.is_active:
            raise serializers.ValidationError(
                'This User has been deactivated.'
            )

        if device_id:
            if not adminAuth.group.is_web_login_allowed:
                raise serializers.ValidationError(
                    'This User not allowed to login'
                )

        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        # that we will see later on.
        return {
            'id' : adminAuth.id,
            'username': adminAuth.username,
            'email': adminAuth.email,
            'token': adminAuth.token,
            'group_id': adminAuth.group
        }
    
class ManagementUserRegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a CompanyUser."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = AdminAuth
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'password', 'token']

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new managementuser.
        return AdminAuth.objects.create_user(**validated_data)

class AdminAuthUpdateSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    # Passwords must be at least 8 characters, but no more than 128
    # characters. These values are the default provided by Django. We could
    # change them, but that would create extra work while introducing no real
    # benefit, so lets just stick with the defaults.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = AdminAuth
        fields = ('email', 'username', 'password', 'token')

        # The `read_only_fields` option is an alternative for explicitly
        # specifying the field with `read_only=True` like we did for password
        # above. The reason we want to use `read_only_fields` here is that
        # we don't need to specify anything else about the field. The
        # password field needed the `min_length` and
        # `max_length` properties, but that isn't the case for the token
        # field.
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        """Performs an update on a CompanyUser."""

        # Passwords should not be handled with `setattr`, unlike other fields.
        # Django provides a function that handles hashing and
        # salting passwords. That means
        # we need to remove the password field from the
        # `validated_data` dictionary before iterating over it.
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `User` instance one at a time.
            setattr(instance, key, value)

        if password is not None:
            # `.set_password()`  handles all
            # of the security stuff that we shouldn't be concerned with.
            instance.set_password(password)

        # After everything has been updated we must explicitly save
        # the model. It's worth pointing out that `.set_password()` does not
        # save the model.
        instance.save()

        return instance

class ManagementUserRegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a CompanyUser."""
    id = serializers.IntegerField(required=False)
    email = serializers.CharField(max_length=255)
    name = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255)

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        required=False
    )
    mobile_number = PhoneNumberField()
    group_id = serializers.PrimaryKeyRelatedField(queryset=Groups.objects.all())

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = AdminAuth
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['id','email', 'name', 'username','mobile_number',
        'password', 'token', 'group_id']

    def validate(self, data):
        user_id = data.get('id')
        email = data.get('email')
        username = data.get('username')
        if user_id:

            user = AdminAuth.objects.get_or_none(id=user_id)
            if not user:
                    raise serializers.ValidationError({'user':'user not exist'})

            isUsernameExist = AdminAuth.objects.exclude(id=user_id)\
            .filter(username=username).exists()
            if isUsernameExist:
                raise serializers.ValidationError({'username':'username already exist'})

            isEmailExist = AdminAuth.objects.exclude(id=user_id).filter(email=email).exists()
            if isEmailExist:
                 raise serializers.ValidationError({'email':'email already exist'})
        else:
            isUsernameExist = AdminAuth.objects.filter(username=username).exists()
            if isUsernameExist:
                raise serializers.ValidationError({'username':'username already exist'})

            isEmailExist = AdminAuth.objects.filter(email=email).exists()
            if isEmailExist:
                 raise serializers.ValidationError({'email':'email already exist'})

        return super().validate(data)
        
    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new managementuser.
        # answer, created = AdminAuth.objects.update_or_create(
        # id=validated_data.get('id', None),
        # defaults={'answer': validated_data.get('answer', None)})
        # return 
        return AdminAuth.objects.create_user(**validated_data)

class ManagementUserListSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source='group.name')
    name = serializers.CharField()
    class Meta:
        model = AdminAuth
        fields = ['id','email','group', 'name']

class ManagementUserRetrieveUpdateDynamicSerializer(DynamicFieldsModelSerializer):
    """Handles serialization and deserialization of User objects."""
    # Passwords must be at least 8 characters, but no more than 128
    # characters. These values are the default provided by Django. We could
    # change them, but that would create extra work while introducing no real
    # benefit, so lets just stick with the defaults.

    class Meta:
        model = AdminAuth
        fields = ('id','email', 'name', 'username', 'mobile_number', 'group_id')

        # The `read_only_fields` option is an alternative for explicitly
        # specifying the field with `read_only=True` like we did for password
        # above. The reason we want to use `read_only_fields` here is that
        # we don't need to specify anything else about the field. The
        # password field needed the `min_length` and
        # `max_length` properties, but that isn't the case for the token
        # field.
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        """Performs an update on a CompanyUser."""

        # Passwords should not be handled with `setattr`, unlike other fields.
        # Django provides a function that handles hashing and
        # salting passwords. That means
        # we need to remove the password field from the
        # `validated_data` dictionary before iterating over it.
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, we will set them on
            # the current `User` instance one at a time.
            setattr(instance, key, value)

        if password is not None:
            # `.set_password()`  handles all
            # of the security stuff that we shouldn't be concerned with.
            instance.set_password(password)

        # After everything has been updated we must explicitly save
        # the model. It's worth pointing out that `.set_password()` does not
        # save the model.
        instance.save()

        return instance

class ManagementUserPasswordResetSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, write_only=True, required=True)

    class Meta:
        model = AdminAuth
        fields = ('id','password')

    def update(self, instance, validated_data):
        instance.set_password(validated_data.get('password'))
        instance.save()
        return instance

