role_choices = (
    (1, "Super admin"),
    (2, "System user"),
    (3, "Employee"),
    (4, "Passenger"),
)

gender_choices = (
    (1, "Man"),
    (2, "Woman"),
)

baggage_choices = (
    (1, "Airport From"),
    (2, "Loading to the board"),
    (3, "On the Board"),
    (4, "Unoading from the board"),
    (5, "Airport To"),
    (6, "Arested"),
)

ticket_choices = (
    (1, "Not used"),
    (2, "Registration"),  # face recognition
    (3, "Security control"),
    (4, "Passport control start"),
    (5, "Used"),
    (6, "Passport control finish"),
    (7, "Baggage"),
)
