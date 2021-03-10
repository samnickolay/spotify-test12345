from django.urls import path

# from . import views
from .views import ActiveAccount, GetAccount

urlpatterns = [
    path('account/get/', GetAccount.as_view(), name='GetAccount'),
    path('account/<int:id>/', ActiveAccount.as_view(), name='ActiveAccount'),
]
