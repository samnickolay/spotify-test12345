from datetime import datetime, timedelta
from time import sleep
import random
from users.models import CustomUser
from random import randint

# import django_rq

from django.utils import timezone
from django.contrib.auth import get_user_model
from django.conf import settings

from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.decorators import action
