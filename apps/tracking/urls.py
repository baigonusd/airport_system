from django.urls import path, include

from rest_framework import routers

from .views import BaggageApi, AirlineApi, TicketApi, BoardingApi, IinApi

router = routers.DefaultRouter()
router.register(r"baggage", BaggageApi, "baggage-api")
router.register(r"ticket", TicketApi, "ticket-api")
router.register(r"boarding", BoardingApi, "boarding-api")


urlpatterns = [
    path("", include(router.urls)),
    path("airline/", AirlineApi.as_view()),
    path("iin/", IinApi.as_view()),
]
