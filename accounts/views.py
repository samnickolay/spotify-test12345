import random

# from datetime import timedelta, datetime
from django.utils import timezone
from django.http import JsonResponse

from django.conf import settings
from django.contrib.auth import get_user_model

from rest_framework import viewsets, status
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_api_key.permissions import HasAPIKey


from .models import Account

CustomUser = get_user_model()


class ActiveAccount(APIView):
    permission_classes = (HasAPIKey,)

    def get(self, request, id=None):
        try:
            account = Account.objects.get(pk=id)
            account.save()
        except Account.DoesNotExist:
            pass
        except Exception as _e:
            print(_e)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class GetAccount(APIView):
    permission_classes = (HasAPIKey,)

    def get(self, request):
        try:
            five_h_ago = timezone.now() - timezone.timedelta(hours=5)
            five_m_ago = timezone.now() - timezone.timedelta(minutes=5)

            accounts = list(Account.objects.filter(modified__lt=five_m_ago))
            # accounts = list(Account.objects.filter(modified__lt=five_h_ago))
            account = random.choice(accounts)

            return JsonResponse({'pk': account.pk, 'email': account.email, 'password': account.password})

        except Exception as _e:
            print(_e)

        return Response(status=status.HTTP_400_BAD_REQUEST)
