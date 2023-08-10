from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, phone_no, name, **extra_fields):
        if not phone_no:
            raise ValueError("The phone number must be set")
        user = self.model(phone_no=phone_no, name=name, **extra_fields)
        # user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_no, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        if not phone_no:
            raise ValueError("The phone number must be set")
        user = self.model(phone_no=phone_no, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
