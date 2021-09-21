from django.contrib.auth.models import User
from django.db import models
# from django.contrib.auth.models import AbstractUser
from django.utils.timezone import get_current_timezone_name
from django.utils.translation import gettext_lazy as _

# class Account(AbstractUser):
#     """
#         Act like a user profile.
#         Need too many changes to uses this model.
#         TODO: When we will change the DataBase engine to postgres, use it.
#     """
#     time_zone = models.CharField(max_length=50,
#                                  default=get_current_timezone_name,
#                                  null=True,
#                                  blank=True)
#     avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
#     bio = models.TextField(max_length=500, blank=True)
#     location = models.CharField(max_length=30, blank=True)
#     birth_date = models.DateField(null=True, blank=True)


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
