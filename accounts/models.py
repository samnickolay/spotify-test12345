
from django.db import models
from django.utils import timezone
# from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, MaxLengthValidator
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class Account(models.Model):

    email = models.EmailField(_('email address'),)
    password = models.CharField(_('password'), max_length=32, blank=True, validators=[MaxLengthValidator(32)])
    modified = models.DateTimeField()

    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        self.modified = timezone.now()
        return super(Account, self).save(*args, **kwargs)

    # def __str__(self):
    #     return str(self.public_id) + ' - ' + self.first_name + " " + self.last_name + " - " + self.email + " - " + str(self.invite_created)
