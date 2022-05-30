from django.db import models

from apps.users.models import Passenger

from utils.abstract import AbstractModel
from utils.choices import baggage_choices, ticket_choices


class Baggage(AbstractModel):
    weight = models.DecimalField("Weight of baggage", max_digits=5, decimal_places=2)
    xray = models.ImageField(
        "Xray of baggage",
        upload_to="xrays",
        height_field=None,
        width_field=None,
        max_length=None,
        blank=True,
    )
    status = models.IntegerField(
        "Status of baggage", choices=baggage_choices, default=1
    )


class Airline(AbstractModel):
    name = models.CharField("Airline name", max_length=90, unique=True)
    logo = models.ImageField(
        "Logo of Airline",
        upload_to="airlines",
        height_field=None,
        width_field=None,
        max_length=None,
        blank=True,
    )


class Flight(AbstractModel):
    from_location = models.CharField("City/Country from", max_length=90)
    to_location = models.CharField("City/Country to", max_length=90)
    time_start = models.DateTimeField()
    time_finish = models.DateTimeField()
    airline = models.ForeignKey(
        Airline, related_name="ticket", on_delete=models.CASCADE
    )


class Ticket(AbstractModel):
    # from_location = models.CharField("City/Country from", max_length=90)
    # to_location = models.CharField("City/Country to", max_length=90)
    # time_start = models.DateTimeField()
    # time_finish = models.DateTimeField()
    # airline = models.ForeignKey(
    #     Airline, related_name="ticket", on_delete=models.CASCADE
    # )
    passenger = models.ForeignKey(
        Passenger, related_name="tickets", on_delete=models.CASCADE
    )
    status = models.IntegerField("Status", choices=ticket_choices, default=1)
    flight = models.ForeignKey(Flight, related_name="tickets", on_delete=models.CASCADE)


class BoardingPass(AbstractModel):
    baggages = models.ForeignKey(
        Baggage, related_name="baggages", on_delete=models.CASCADE
    )
    ticket = models.OneToOneField(
        Ticket, related_name="tickets", on_delete=models.CASCADE
    )
    sector = models.CharField("Sector of place", max_length=1)
    number = models.IntegerField("Number of place")
    flight = models.ForeignKey(
        Flight, related_name="boarding", on_delete=models.CASCADE
    )
