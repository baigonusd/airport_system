from rest_framework import permissions


class IsAirport(permissions.BasePermission):
    """
    Global permission check for blocked IPs.
    """

    def has_permission(self, request, view):
        ip_addr = request.META["REMOTE_ADDR"]
        token = request.auth.key

        if ip_addr == "127.0.0.1" and token == "example":
            return True
