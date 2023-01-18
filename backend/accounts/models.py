from django.contrib.auth.models import AbstractUser


class Account(AbstractUser):
    pass

    def __str__(self) -> str:
        return self.username
