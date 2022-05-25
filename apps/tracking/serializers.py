from django.db import transaction

from rest_framework import serializers, exceptions

from .models import Baggage, Airline, Ticket, BoardingPass


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


class AirlineTicketSerializer(serializers.Serializer):
    class Meta:
        model = Airline
        fields = ("id",)


# class BaggageBoardingSerializer(serializers.Serializer):
#     class Meta:
#         model = Airline
#         fields = ("id",)


class TicketGetSerializer(serializers.Serializer):
    from_location = serializers.CharField(max_length=90)
    to_location = serializers.CharField(max_length=90)
    time_start = serializers.DateTimeField()
    time_finish = serializers.DateTimeField()
    airline = AirlineTicketSerializer
    status = serializers.IntegerField()


class TicketPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = (
            "from_location",
            "to_location",
            "time_start",
            "time_finish",
            "airline",
            "status",
        )

    def validate(self, data):
        if data.get("time_finish") < data.get("time_start"):
            raise serializers.ValidationError(
                {"time": "Departure time can not be after Arrival time"}
            )
        return super().validate(data)

    @transaction.atomic
    def create(self, validated_data):
        ticket = Ticket.objects.create(
            passenger=self.context["request"].user.passenger_profile, **validated_data
        )
        return ticket


class BoardingGetSerializer(serializers.ModelSerializer):
    class Meta:
        model = BoardingPass
        fields = ("baggages", "ticket", "sector", "number")


class BoardingPostSerializer(serializers.ModelSerializer):
    baggages_ids = serializers.PrimaryKeyRelatedField(
        many=True, write_only=True, queryset=Baggage.objects.all()
    )

    class Meta:
        model = BoardingPass
        fields = ("ticket", "sector", "number", "baggages_ids")

    def validate(self, data):
        if len(data.get("sector")) > 1:
            raise serializers.ValidationError(
                {"time": "Sector field has only one argument"}
            )
        return super().validate(data)

    @transaction.atomic
    def create(self, validated_data):
        print(validated_data)
        baggages = validated_data.pop("baggages_ids", None)
        boardingpass = BoardingPass.objects.create(**validated_data)
        print({"###############################": baggages})
        if baggages:
            boardingpass.baggages.set(baggages)
        return boardingpass
