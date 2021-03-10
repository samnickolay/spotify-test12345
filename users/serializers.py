# from django.contrib.auth import get_user_model
from datetime import timedelta
from rest_framework import serializers
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.auth import get_user_model
from backend.utils import PublicIdModelSerializer
# from rooms.models import Room
# from rooms.permissions import RoomCallViewPermission

User = get_user_model()


class DurationField(serializers.Field):
    def to_representation(self, value):
        return (value - timezone.now()).total_seconds()

    def to_internal_value(self, data):
        seconds = int(data)
        return timezone.now() + timedelta(seconds=seconds)


class UserSerializer(PublicIdModelSerializer):
    team = serializers.StringRelatedField()

    # zen_mode_duration = DurationField(source='zen_mode_until')
    offline_duration = DurationField(source='offline_since')

    id = serializers.CharField(source='public_id')

    class Meta:
        model = User

        fields = (
            'id',
            'team',
            'first_name',
            'last_name',
            'agora_uid',
            # 'current_room',
            'role',
            'status',
            'offline_duration',
            # 'zen_mode_duration',
            'timezone_offset',
            'location',
            'picture_url',
            'email'
        )

        read_only_fields = ('id', 'team', 'role', 'offline_duration', 'email')


class UserChangeRoleSerializer(PublicIdModelSerializer):
    id = serializers.CharField(source='public_id')

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'role',
            'picture_url'
        )
        read_only_fields = ('id', 'email', 'first_name', 'last_name', 'picture_url')

    def validate_role(self, value):
        if value == User.ROLES_OWNER:
            raise ValidationError('Cannot promote account to team owner')
        elif value not in [User.ROLES_MEMBER, User.ROLES_ADMIN]:
            raise ValidationError('Invalid role given')

        return value


class UserSettingsSerializer(PublicIdModelSerializer):
    id = serializers.CharField(source='public_id')

    class Meta:
        model = User

        fields = (
            'id',
            'first_name',
            'last_name',
            'current_team_show_app',
            'current_team_show_status',
            'other_team_show_app',
            'other_team_show_status',
            'auto_mute',
            'notification_teammate_online',
            'notification_receive_file',
            'notification_system_text',
            'notification_sound'
        )
        read_only_fields = ('id',)


class AdminUserSettingsSerializer(PublicIdModelSerializer):
    id = serializers.CharField(source='public_id')

    class Meta:
        model = User

        fields = (
            'id',
            'teammate_joined_email',
            'teammate_left_email',
        )
        read_only_fields = ('id',)
