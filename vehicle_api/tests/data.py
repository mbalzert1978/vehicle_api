from presentation.vehicles.schemas import CreateVehicle

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
    "vehicle_type": "limousine",
}
BODY_Q7 = {
    "color": "red",
    "kilometer": 100_000,
    "price": 75_000,
    "vehicle_type": "suv",
}
PARAMS = {
    "name": "test_vehicle",
    "manufacturing_year": 2020,
    "is_drivable": False,
    "body": {
        "color": "test_color",
        "kilometer": 10,
        "price": 10_000,
        "vehicle_type": "test_type",
    },
}
UPDATE = {
    "name": "updated_vehicle",
    "manufacturing_year": 2010,
    "is_drivable": True,
    "body": {
        "price": 100,
        "kilometers": 100,
        "type": "car",
    },
}
TEST_VEHICLE = CreateVehicle(
    name="test_car",
    manufacturing_year=2020,
    body=BODY,
    is_drivable=False,
)
I30 = CreateVehicle(
    name="I30",
    manufacturing_year=2017,
    body=BODY_I30,
    is_drivable=True,
)
Q7 = CreateVehicle(
    name="Q7",
    manufacturing_year=2020,
    body=BODY_Q7,
    is_drivable=True,
)
