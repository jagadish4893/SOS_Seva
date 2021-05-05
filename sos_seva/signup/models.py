from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

# USER_TYPE = [
#     ('stateadmin', 'stateadmin'),
#     ('nodaladmin', 'nodaladmin'),
#     ('hospitaladmin', 'hospitaladmin'),
# ]

COMMUNITY_LIST = [
    ("", ""),
    ('mirinda', 'MIRINDA'),
]

# USER_TYPE = [
#     ('stateadmin', 'stateadmin'),
#     ('nodaladmin', 'nodaladmin'),
#     ('hospitaladmin', 'hospitaladmin'),
# ]


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile_no = models.CharField(max_length=50, null=True,
                            blank=True, default="")
    community = models.CharField(max_length=50, null=True,
                            blank=True, choices=COMMUNITY_LIST, default="")

    def __str__(self):
        return "{} - {}".format(self.user, self.community)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # if instance.profile:
    if hasattr(instance, 'profile'):
        instance.profile.save()
