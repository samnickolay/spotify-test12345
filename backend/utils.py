from datetime import datetime

import json
import jwt
import requests

# from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import is_aware, make_aware

from django.utils.crypto import get_random_string

from rest_framework.relations import RelatedField
from rest_framework import serializers

# removed I, O, and 0
ALLOWED_CHARACTERS = "ABCDEFGHJKLMNPQRSTUVWXYZ123456789"
PUBLIC_ID_LENGTH = 10
# PUBLIC_ID_LENGTH_LONG = 20


def create_public_id():
    return get_random_string(length=PUBLIC_ID_LENGTH, allowed_chars=ALLOWED_CHARACTERS)


# def create_public_id_long():
#     return get_random_string(length=PUBLIC_ID_LENGTH_LONG, allowed_chars=ALLOWED_CHARACTERS)


def jwt_get_username_from_payload_handler(payload):
    namespace = 'https://www.vizy.io/'
    user_id_field_name = namespace + 'user_id'
    username = payload.get(user_id_field_name).replace('|', '.')

    # username = payload.get('user_public_id').replace('|', '.')
    # authenticate(remote_user=username)
    return username


def jwt_decode_token(token):
    header = jwt.get_unverified_header(token)
    jwks = requests.get('https://{}/.well-known/jwks.json'.format('dev-y0hew9il.auth0.com')).json()
    public_key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == header['kid']:
            public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(jwk))

    if public_key is None:
        raise Exception('Public key not found.')

    issuer = 'https://{}/'.format('dev-y0hew9il.auth0.com')
    return jwt.decode(token, public_key, audience='https://vizy.io/api', issuer=issuer, algorithms=['RS256'])


class PublicIdRelatedField(RelatedField):
    default_error_messages = {
        'required': _('This field is required.'),
        'does_not_exist': _('Invalid public_id "{public_id}" - object does not exist.'),
        'incorrect_type': _('Incorrect type. Expected public_id value, received {data_type}.'),
    }

    def __init__(self, **kwargs):
        self.public_id = kwargs.pop('public_id', None)
        super().__init__(**kwargs)

    # def use_pk_only_optimization(self):
    #     return True

    def to_internal_value(self, data):
        if self.public_id is not None:
            data = self.public_id.to_internal_value(data)
        try:
            return self.get_queryset().get(public_id=data)
        except ObjectDoesNotExist:
            self.fail('does_not_exist', public_id=data)
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)

    def to_representation(self, value):
        if self.public_id is not None:
            return self.public_id.to_representation(value.public_id)
        return value.public_id


class PublicIdModelSerializer(serializers.ModelSerializer):
    serializer_related_field = PublicIdRelatedField  # gets public_id instead of pk for foreign keys


class TimestampField(serializers.Field):
    def to_internal_value(self, data):
        _dt = datetime.fromtimestamp(data)
        if not is_aware(_dt):
            _dt = make_aware(_dt)
        return _dt

    def to_representation(self, value):
        return datetime.timestamp(value)
