from aimsun_api import AimsunAPI

class DataProcessor:
    def __init__(self):
        self.aimsun_api = AimsunAPI()

    def get_vehicle_data_from_aimsun(self):
        vehicle_data = self.aimsun_api.get_vehicle_data()
        return vehicle_data

    def preprocess_vehicle_data(self, vehicle_data):
        preprocessed_data = []
        for vehicle in vehicle_data:
            if self.filter_vehicle(vehicle):
                preprocessed_vehicle = {}
                preprocessed_vehicle['id'] = vehicle.id
                preprocessed_vehicle['position'] = self.convert_coordinates(vehicle.position)
                preprocessed_vehicle['speed'] = self.convert_speed(vehicle.speed)
                preprocessed_vehicle['lane'] = self.get_lane(vehicle.position)
                preprocessed_data.append(preprocessed_vehicle)
        return preprocessed_data

    def filter_vehicle(self, vehicle):
        return vehicle.speed > 10

    def convert_coordinates(self, position):
        converted_position = position * 1000  
        return converted_position

    def convert_speed(self, speed):
        converted_speed = speed * 3.6  
        return converted_speed

    def get_lane(self, position):
        lane = self.aimsun_api.get_lane(position)
        return lane

class AimsunAPI:
    def __init__(self):
        self.connect()

    def connect(self):

    def get_vehicle_data(self):
        vehicle_data = self.query_database()
        return vehicle_data

    def query_database(self):
        vehicle_data = []  
        return vehicle_data

    def get_lane(self, position):
        lane = self.query_lane(position)
        return lane

    def query_lane(self, position):
        lane = 1  
        return lane
