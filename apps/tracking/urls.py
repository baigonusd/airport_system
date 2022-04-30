from django.urls import path, include

from rest_framework import routers

from .views import BaggageApi, AirlineApi, TicketApi, BoardingApi

router = routers.DefaultRouter()
router.register(r"ticket", TicketApi, "ticket-api")
router.register(r"boarding", BoardingApi, "boarding-api")


urlpatterns = [
    path("baggage/", BaggageApi.as_view()),
    path("", include(router.urls)),
    path("airline/", AirlineApi.as_view()),
    # path("ticket/", TicketApi),
]
