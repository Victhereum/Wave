from django.urls import path

from wave.apps.users.api.views import PhoneNumberView, RegistrationAPI

app_name = "users"
urlpatterns = [
    path("register/", RegistrationAPI.as_view()),
    path("phone/otp/", PhoneNumberView.as_view()),
]
