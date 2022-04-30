import pytz

for key, val in pytz.country_names.items():
    print(key, "=", val, end=",")
    print("\n")
