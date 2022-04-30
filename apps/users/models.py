from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.dispatch import receiver
from django.db.models.signals import post_save

from .managers import CustomUserManager

from utils.choices import role_choices, gender_choices
from utils.abstract import AbstractModel


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Email", unique=True, null=True)
    name = models.CharField("Name", max_length=90, blank=True)
    surname = models.CharField("Surname", max_length=90, blank=True)
    role = models.IntegerField("User role", choices=role_choices, default=4)
    is_valid_email = models.BooleanField("Is the email confirmed", default=False)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    USERNAME_FIELD = "email"
    objects = CustomUserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")

    def __str__(self):
        return self.email


class Passenger(AbstractModel):
    user = models.OneToOneField(
        User,
        verbose_name=_("User"),
        related_name=_("passenger_profile"),
        on_delete=models.CASCADE,
    )
    mobile_phone = models.CharField(
        _("Mobile phone"),
        validators=[
            RegexValidator(regex="^\+77[0-9]{9}$", message="Incorrect phone format")
        ],
        max_length=15,
        null=True,
        blank=True,
    )
    valid_number = models.BooleanField("Verified phone number", default=False)
    gender = models.IntegerField("Passenger gender", choices=gender_choices, default=1)
    number_of_doc = models.CharField(
        "Passenger's number of doc",
        max_length=9,
        validators=[
            RegexValidator(regex="^\d{9}$", message="Incorrect format of doc's number")
        ],
        unique=True,
    )
    iin = models.CharField(
        "Passenger's IIN",
        max_length=12,
        validators=[
            RegexValidator(regex="^\d{12}$", message="Incorrect format of IIN")
        ],
        unique=True,
    )
    scan_udv = models.ImageField(
        "Scan of document",
        upload_to="udv",
        height_field=None,
        width_field=None,
        max_length=None,
        blank=True,
    )

    def __str__(self):
        return "User profile: {}, <id: {}>".format(self.user.email, self.pk)


class Employee(AbstractModel):
    user = models.OneToOneField(
        User,
        verbose_name=_("User"),
        related_name=_("employee_profile"),
        on_delete=models.CASCADE,
    )


################################
# Сигналы
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.role == 4:
            Passenger.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.role == 4:
        try:
            instance.passenger_profile.save()
        except:
            Passenger.objects.create(user=instance)
