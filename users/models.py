from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_admin=False, is_staff=False, is_active=True):
        if not email:
            raise ValueError("User must have an email")
        if not password:
            raise ValueError("User must have a password")
        # if not full_name:
        #     raise ValueError("User must have a full name")

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)  # change password to hash
        user.staff = is_staff
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
        )
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user


class CustomUser(PermissionsMixin, AbstractBaseUser):
    email = models.EmailField(verbose_name=_("Email"), unique=True)
    # first_name = models.CharField(verbose_name=_("first name"), max_length=30, blank=True, null=True)
    # last_name = models.CharField(verbose_name=_("last name"), max_length=30, blank=True, null=True)

    is_staff = models.BooleanField(
        _("staff status"), default=False, help_text=_("Designates whether the user can log into this admin site.")
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. " "Unselect this instead of deleting accounts."
        ),
    )

    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # class Meta:
    #     ordering = ("first_name", "last_name")

    # def __str__(self):
    #     return self.get_full_name() or self.email

    # def get_short_name(self):
    #     if self.first_name:
    #         return self.first_name
    #     return self.email.split("@")[0]

    # def get_full_name(self):
    #     return " ".join(filter(None, [self.first_name, self.last_name]))
