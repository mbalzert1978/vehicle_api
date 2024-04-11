from vehicle_api.schemas.vehicle import VehicleForCreate

BODY = {
    "color": "test_color",
    "kilometer": 10,
    "price": 10_000,
    "vehicle_type": "test_type",
}
BODY_I30 = {
    "color": "black",
    "kilometer": 10000,
    "price": 15000,
    "vehicle_type": "limusine",
}
BODY_Q7 = {
    "color": "red",
    "kilometer": 100_000,
    "price": 75_000,
    "vehicle_type": "suv",
}
PARAMS = {
    "name": "test_vehicle",
    "year_of_manufacture": 2020,
    "ready_to_drive": False,
    "body": {
        "color": "test_color",
        "kilometer": 10,
        "price": 10_000,
        "vehicle_type": "test_type",
    },
}
UPDATE = {
    "name": "updated_vehicle",
    "year_of_manufacture": 2010,
    "ready_to_drive": True,
    "body": {
        "price": 100,
        "kilometers": 100,
        "type": "car",
    },
}
TEST_VEHICLE = VehicleForCreate(
    name="test_car",
    year_of_manufacture=2020,
    body=BODY,
    ready_to_drive=False,
)
I30 = VehicleForCreate(
    name="I30",
    year_of_manufacture=2017,
    body=BODY_I30,
    ready_to_drive=True,
)
Q7 = VehicleForCreate(
    name="Q7",
    year_of_manufacture=2020,
    body=BODY_Q7,
    ready_to_drive=True,
)
