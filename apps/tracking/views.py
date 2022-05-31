from django.shortcuts import render

from rest_framework import generics, permissions, status, viewsets, mixins
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from .permissions import IsAirport

from .serializers import (
    BaggageGetSerializer,
    BaggagePostSerializer,
    AirlineSerializer,
    TicketGetSerializer,
    TicketPostSerializer,
    BoardingGetSerializer,
    BoardingPostSerializer,
    FlightGetSerializer,
    FlightPostSerializer,
)

from .models import Baggage, Airline, Ticket, BoardingPass, Flight
from utils.facerecognition import verify_by_face

from apps.users.models import Passenger


# class BaggageApi(generics.GenericAPIView):
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = BaggageSerializer

#     def get(self, request, *args, **kwargs):
#         if self.request.user.role == 3:
#             queryset = Baggage.objects.all()
#             return Response({"Baggages": BaggageSerializer(queryset, many=True).data})
#         else:
#             return Response("You have no permission", status=status.HTTP_403_FORBIDDEN)

#     def post(self, request, *args, **kwargs):
#         if self.request.user.role == 3:
#             serializer = self.get_serializer(data=request.data)
#             serializer.is_valid(raise_exception=True)
#             serializer.save()
#         else:
#             return Response("You have no permission", status=status.HTTP_403_FORBIDDEN)

#         return Response(
#             data={"message": f"Baggage {request.data['name']} is succesfully created"},
#             status=status.HTTP_201_CREATED,
# )


class BaggageApi(viewsets.ModelViewSet):
    serializer_class = BaggageGetSerializer
    create_update_serializer_class = BaggagePostSerializer
    permission_class = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Baggage.objects.all()

    def get_serializer_class(self):
        create_update = ["create", "update", "partial_update"]
        safe_actions = ["list", "retrieve"]
        if self.action in create_update:
            self.serializer_class = self.create_update_serializer_class
        elif self.action in safe_actions:
            self.serializer_class = self.serializer_class
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        queryset = Baggage.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(detail=False, methods=["post"])
    def get_baggage_status(self, request, **kwargs):
        baggage = (
            BoardingPass.objects.filter(ticket=self.request.data.get("ticket"))
            .first()
            .baggages
        )
        status = baggage.filter(id=self.request.data.get("id")).first().status
        return Response({"status": status})


class AirlineApi(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AirlineSerializer

    def get(self, request, *args, **kwargs):
        if self.request.user.role == 2:
            queryset = Airline.objects.all()
            return Response({"Airlines": AirlineSerializer(queryset, many=True).data})
        else:
            return Response("You have no permission", status=status.HTTP_403_FORBIDDEN)

    def post(self, request, *args, **kwargs):
        if self.request.user.role == 2:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        else:
            return Response("You have no permission", status=status.HTTP_403_FORBIDDEN)

        return Response(
            data={"message": f"Airline {request.data['name']} is succesfully created"},
            status=status.HTTP_201_CREATED,
        )


class TicketApi(viewsets.ModelViewSet):
    serializer_class = TicketGetSerializer
    create_update_serializer_class = TicketPostSerializer
    permission_class = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Ticket.objects.filter(passenger=self.request.user.passenger_profile)

    def get_serializer_class(self):
        create_update = ["create", "update", "partial_update"]
        safe_actions = ["list", "retrieve"]
        if self.action in create_update:
            self.serializer_class = self.create_update_serializer_class
        elif self.action in safe_actions:
            self.serializer_class = self.serializer_class
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        queryset = Ticket.objects.filter(passenger=self.request.user.passenger_profile)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    @action(
        detail=False,
        methods=["get"],
    )
    def get_tickets_by_iin_or_ticketid(self, request, **kwargs):
        passenger = Passenger.objects.filter(
            iin=self.request.query_params.get("iin")
        ).first()
        if passenger:
            ticket = Ticket.objects.filter(passenger=passenger)
        else:
            ticket = Ticket.objects.filter(
                pk=self.request.query_params.get("ticket_id")
            )
        tickets = self.serializer_class(ticket, many=True)
        # print(tickets.data)
        # print(list(ticket.values()))

        # return Response(list(ticket.values()))
        return Response(tickets.data)


class FlightApi(viewsets.ModelViewSet):
    serializer_class = FlightGetSerializer
    create_update_serializer_class = FlightPostSerializer
    permission_class = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Flight.objects.all()

    def get_serializer_class(self):
        create_update = ["create", "update", "partial_update"]
        safe_actions = ["list", "retrieve"]
        if self.action in create_update:
            self.serializer_class = self.create_update_serializer_class
        elif self.action in safe_actions:
            self.serializer_class = self.serializer_class
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        queryset = Flight.objects.all()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class BoardingApi(viewsets.ModelViewSet):
    serializer_class = BoardingGetSerializer
    create_update_serializer_class = BoardingPostSerializer
    permission_class = [permissions.IsAuthenticated]

    def get_queryset(self):
        return BoardingPass.objects.all()

    def get_serializer_class(self):
        create_update = ["create", "update", "partial_update"]
        safe_actions = ["list", "retrieve"]
        if self.action in create_update:
            self.serializer_class = self.create_update_serializer_class
        elif self.action in safe_actions:
            self.serializer_class = self.serializer_class
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        queryset = BoardingPass.objects.filter(
            flight=self.request.query_params.get("flight")
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class IinApi(APIView):
    permission_classes = [IsAirport]

    # def get(self, request):
    #     ip_addr = self.request.META["REMOTE_ADDR"]
    #     return Response({"ip": ip_addr})

    def post(self, request, *args, **kwargs):
        iin = self.request.data.get("iin")
        verify_by_face(iin)
        return Response({"iin": iin})
