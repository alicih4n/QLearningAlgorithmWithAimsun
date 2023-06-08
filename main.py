import aimsun_api

from car import Car
from route import select_route
from data_processing import process_data
from traffic_lights import TrafficLights
from q_learning import QLearning


def configure_simulation():
    aimsun_api.connect()  

    simulation_config = SimulationConfig()
    simulation_config.set_simulation_duration(7200)  

    network_file = "path/to/network_file.xml"  
    aimsun_api.load_network(network_file)

    control_file = "path/to/control_file.cntl"  
    aimsun_api.load_control_file(control_file)

    aimsun_api.start()


def start_simulation():
    aimsun_api.start_simulation()


def create_vehicle():
    vehicle_id = 1  
    initial_position = (0, 0)  
    initial_speed = 20  
    destination = (100, 100)  

    car = Car(vehicle_id)
    car.set_position(initial_position)
    car.set_speed(initial_speed)
    car.set_destination(destination)

    aimsun_api.add_vehicle(car)


def add_vehicles_to_simulation(vehicles):
    pass

def create_traffic_lights():
    pass

def connect_traffic_lights_to_control_file(traffic_lights):
    for traffic_light in traffic_lights:
        aimsun_api.connect_traffic_light_to_control_file(traffic_light)

def configure_q_learning():
    q_learning = QLearning()
    q_learning.configure_parameters()


def start_q_learning():
    q_learning = QLearning()
    q_learning.start_learning()

if __name__ == "__main__":
    aimsun_api.connect()

    configure_simulation()
    start_simulation()

    vehicles = create_vehicles()
    add_vehicles_to_simulation(vehicles)

    traffic_lights = create_traffic_lights()
    connect_traffic_lights_to_control_file(traffic_lights)

    configure_q_learning()
    start_q_learning()

    aimsun_api.start()
