import json

def list_of_places(data):
    places = json.loads(json.dumps(data))
    a = []
    for place in places:
        mesto = place['sector']+str(place['number'])
        a.append(mesto)

    dict_places = {
        "A1": False,
        "A2": False,
        "A3": False,
        "A4": False,
        "A5": False,
        "B1": False,
        "B2": False,
        "B3": False,
        "B4": False,
        "B5": False,
        "C1": False,
        "C2": False,
        "C3": False,
        "C4": False,
        "C5": False,
        "D1": False,
        "D2": False,
        "D3": False,
        "D4": False,
        "D5": False,
        "E1": False,
        "E2": False,
        "E3": False,
        "E4": False,
        "E5": False,
        "F1": False,
        "F2": False,
        "F3": False,
        "F4": False,
        "F5": False,
    }

    for i in a:
        dict_places[i]=True

    return dict_places    