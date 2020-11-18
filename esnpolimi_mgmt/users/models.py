from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django_fsm import FSMField, transition


class User(AbstractBaseUser, PermissionsMixin):
    """
    Fully featured User model with admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_("email address"), blank=True)
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
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        swappable = "AUTH_USER_MODEL"

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    person = models.OneToOneField(
        "esnpolimi_mgmt.Person",
        on_delete=models.PROTECT,
    )
    # limit_choices_to={"univeristy": settings.HOME_UNIVERSITY})

    class Status(models.TextChoices):
        aspirant = "aspirant", _("Aspirant")
        rejected = "rejected", _("Rejected Aspirant")
        member = "member", _("Active Member")
        ex_member = "ex_member", _("Ex Member")
        alumnus = "alumnus", _("Alumnus")

    status = FSMField(choices=Status.choices, default=Status.aspirant)

    @transition(field=status, source=Status.aspirant, target=Status.member)
    def activate(self):
        pass

    @transition(field=status, source=Status.aspirant, target=Status.rejected)
    def reject(self):
        pass

    @transition(field=status, source=Status.rejected, target=Status.aspirant)
    def try_again(self):
        pass

    @transition(field=status, source=Status.member, target=Status.ex_member)
    def deactivate(self):
        pass

    @transition(field=status, source=Status.member, target=Status.alumnus)
    def to_alumnus(self):
        pass

    def get_absolute_url(self):
        """Get url for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})
