class AimsunAPI:
    """
    Mock Aimsun API for testing RL loop without the simulator.
    Replace/Extend this with actual TCP/Socket or COM client code.
    """
    def __init__(self):
        self.connected = False
        self.vehicles = []
        self.traffic_lights = {}

    def connect(self):
        print("Aimsun API: Connected.")
        self.connected = True
        return True

    def load_network(self, network_file):
        print(f"Aimsun API: Loading network {network_file}")

    def load_control_file(self, control_file):
        print(f"Aimsun API: Loading control file {control_file}")

    def load_traffic_demand(self, demand_file):
        print(f"Aimsun API: Loading traffic demand {demand_file}")

    def close_lane(self, link_id, duration):
        print(f"Aimsun API: Closing lane on Link {link_id} for {duration} seconds (Accident)")


    def start(self):
        print("Aimsun API: Starting simulation engine.")

    def start_simulation(self):
        print("Aimsun API: Simulation started.")

    def add_vehicle(self, vehicle_data):
        # vehicle_data might be a dict or object
        self.vehicles.append(vehicle_data)
        # print(f"Aimsun API: Vehicle added {vehicle_data}")

    def set_traffic_light_phase(self, junction_id, phase_id):
        # print(f"Aimsun API: Setting Junction {junction_id} to Phase {phase_id}")
        self.traffic_lights[junction_id] = phase_id

    def get_detector_data(self, detector_id):
        # Return random data for testing
        import random
        return {
            'count': random.randint(0, 10),
            'occupancy': random.random() * 100
        }

    def close(self):
        print("Aimsun API: Disconnected.")
        self.connected = False
