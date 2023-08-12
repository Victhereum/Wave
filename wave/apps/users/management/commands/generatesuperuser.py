import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.urls import reverse

User = get_user_model()
ADMIN_URL = reverse("admin:index")


class Command(BaseCommand):
    help = "generate super admin"

    # def add_arguments(self, parser):
    #     parser.add_argument('platform', nargs='+', type=str)

    def handle(self, *args, **options):
        phone_no = os.getenv("SUPER_ADMIN_PHONE", "xxxxxxxxx")
        name = os.getenv("SUPER_ADMIN_NAME", "xxxxxxxx")
        password = os.getenv("SUPER_ADMIN_PASSWORD", "xxxxxxxx")
        try:
            if phone_no and password:
                user = User.objects.filter(phone_no=phone_no).first()
                if not user:
                    try:
                        user = User(email=phone_no, name=name)
                        user.is_active = True
                        user.is_superuser = True
                        user.is_staff = True

                        user.set_password(password)
                        user.save()
                        message = f"""
                            new superuser crediential
                            phone_no:{phone_no}
                            name:{name}
                            password: {password}
                        """
                        user.email_user("new super user credential", message)
                        self.stdout.write(self.style.SUCCESS("super admin created"))
                    except Exception as e:
                        self.stdout.write(self.style.ERROR(e))

                elif password:
                    message = f"""
                        updated superuser crediential
                        phone_no:{phone_no}
                        password: {password}
                    """
                    user.set_password(password)
                    user.is_active = True
                    user.is_superuser = True
                    user.is_staff = True
                    user.phone_no = phone_no
                    user.name = name
                    user.save()
                    user.email_user("updated super user credential", message)
                    self.stdout.write(self.style.WARNING("super admin updated"))
                else:
                    self.stdout.write(self.style.WARNING("super admin already exists"))

            else:
                self.stdout.write(
                    self.style.WARNING("SUPER_ADMIN_PHONE_NO does not exist in the enviroment variable.")
                )
        except Exception:
            ...

        self.stdout.write(self.style.SUCCESS("done"))
