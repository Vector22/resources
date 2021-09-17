from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import get_current_timezone_name
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    """
        One user has only one profile (here just to save the user Time Zone)
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    time_zone = models.CharField(max_length=50,
                                 default=get_current_timezone_name)

    def __str__(self) -> str:
        # return f"_(Profile of) {self.user.username}"
        return _("Profile of ").format(self.user.username)
