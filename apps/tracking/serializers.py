from django.db import transaction

from rest_framework import serializers, exceptions

from .models import Baggage, Airline, Ticket, BoardingPass, Flight


class BaggageGetSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    weight = serializers.DecimalField(max_digits=5, decimal_places=2)
    status = serializers.IntegerField()


class BaggagePostSerializer(serializers.Serializer):
    # name = serializers.CharField(max_length=90)
    # description = serializers.CharField(max_length=90, required=False)
    weight = serializers.DecimalField(max_digits=5, decimal_places=2)
    status = serializers.IntegerField(required=False)
    xray = serializers.ImageField(required=False)

    @transaction.atomic
    def create(self, validated_data):
        print(validated_data)
        baggage = Baggage.objects.create(**validated_data)
        return baggage


class AirlineSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=90, required=True)
    logo = serializers.ImageField(use_url=False, required=False)

    @transaction.atomic
    def create(self, validated_data):
        airline = {"name": validated_data["name"], "logo": validated_data["logo"]}
        airline_created = Airline.objects.create(**airline)
        return airline_created


# class BaggageBoardingSerializer(serializers.Serializer):
#     class Meta:
#         model = Airline
#         fields = ("id",)


# class FlightGetSerializer(serializers.Serializer):
#     from_location = serializers.CharField(max_length=90)
#     to_location = serializers.CharField(max_length=90)
#     time_start = serializers.DateTimeField()
#     time_finish = serializers.DateTimeField()
#     airline = AirlineFlightSerializer()


class FlightGetSerializer(serializers.ModelSerializer):

    airline = serializers.CharField(source="airline.name")
    airline_logo = serializers.ImageField(source="airline.logo")

    class Meta:
        model = Flight
        fields = (
            "from_location",
            "to_location",
            "time_start",
            "time_finish",
            "airline",
            "airline_logo",
        )


class FlightPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = (
            "from_location",
            "to_location",
            "time_start",
            "time_finish",
            "airline",
        )

    def validate(self, data):
        if data.get("time_finish") < data.get("time_start"):
            raise serializers.ValidationError(
                {"time": "Departure time can not be after Arrival time"}
            )
        return super().validate(data)

    @transaction.atomic
    def create(self, validated_data):
        flight = Flight.objects.create(**validated_data)
        return flight


class TicketGetSerializer(serializers.ModelSerializer):
    passenger_name = serializers.CharField(source="passenger.user.name")
    passenger_surname = serializers.CharField(source="passenger.user.surname")
    flight_from_location = serializers.CharField(source="flight.from_location")
    flight_to_location = serializers.CharField(source="flight.to_location")
    flight_time_start = serializers.CharField(source="flight.time_start")
    flight_time_finish = serializers.CharField(source="flight.time_finish")
    flight_airline = serializers.CharField(source="flight.airline.name")

    class Meta:
        model = Ticket
        fields = (
            "id",
            "status",
            "passenger",
            "flight",
            "passenger_name",
            "passenger_surname",
            "flight_from_location",
            "flight_to_location",
            "flight_time_start",
            "flight_time_finish",
            "flight_airline",
        )


class TicketPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = "__all__"

    @transaction.atomic
    def create(self, validated_data):
        ticket = Ticket.objects.create(**validated_data)
        return ticket


class BoardingGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardingPass
        fields = ("sector", "number")


# class BoardingBaggagesSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Baggage
#         # depth = 3
#         fields = "__all__"


class BoardingPostSerializer(serializers.ModelSerializer):
    # baggages = serializers.PrimaryKeyRelatedField(
    #     many=True, write_only=True, queryset=Baggage.objects.all()
    # )
    # baggages = BoardingBaggagesSerializer(many=True)
    # baggages = serializers.ListField()
    class Meta:
        model = BoardingPass
        fields = ("ticket", "sector", "number", "baggages", "flight")

    def validate(self, data):
        if len(data.get("sector")) > 1:
            raise serializers.ValidationError(
                {"time": "Sector field has only one argument"}
            )
        return super().validate(data)

    @transaction.atomic
    def create(self, validated_data):
        print(validated_data)
        # baggages = validated_data.pop("baggages", None)
        boardingpass = BoardingPass.objects.create(**validated_data)
        # print({"###############################": baggages})
        # if baggages:
        # boardingpass.baggages.set(baggages)
        return boardingpass
