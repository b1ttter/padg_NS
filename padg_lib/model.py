import tkintermapview

def _build_headers(self, provider_key, **kwargs):
    return {"User-Agent": 'My User Agent 1.0'}


def get_coordinates(address: str):
    from geocoder.osm import OsmQuery
    OsmQuery._build_headers = _build_headers
    data = tkintermapview.convert_address_to_coordinates(address)
    if data is None:
        return [0, 0]
    latitude = float(data[0])
    longitude = float(data[1])
    return [latitude, longitude]

universities: list = []
employees: list = []
students: list = []
classes: list = []

class University:
    def __init__(self, name: str, city: str, street: str):
        self.name = name
        self.city = city
        self.street = street
        address:str = f"{city}, {street}"
        self.coords = get_coordinates(address)


class Class:
    def __init__(self, name: str, university_name: str):
        self.name = name
        self.university_name = university_name

class Employee:
    def __init__(self, name: str, city: str, street: str, university_name: str):
        self.name = name
        self.city = city
        self.street = street
        self.university_name = university_name
        address: str = f"{city}, {street}"
        self.coords = get_coordinates(address)

class Student:
    def __init__(self, name: str, university_name: str, class_name: str, location: str):
        self.name = name
        self.university_name = university_name
        self.class_name = class_name
        self.location = location
        self.coords = get_coordinates(location)