class Car:
    def __init__(self, id, initial_position, initial_speed):
        self.id = id
        self.position = initial_position
        self.speed = initial_speed
        self.acceleration = 0
        self.max_speed = 20
        self.min_speed = 0
        self.destination = None
        self.route = []

    def update_position(self, time_step):
        self.position += self.speed * time_step

    def update_speed(self, new_speed):
        if new_speed > self.max_speed:
            self.speed = self.max_speed
        elif new_speed < self.min_speed:
            self.speed = self.min_speed
        else:
            self.speed = new_speed

    def accelerate(self, acceleration):
        self.acceleration = acceleration
        self.speed += self.acceleration

    def decelerate(self, deceleration):
        self.acceleration = -deceleration
        self.speed += self.acceleration

    def set_destination(self, destination):
        self.destination = destination

    def set_route(self, route):
        self.route = route

    def get_position(self):
        return self.position

    def get_speed(self):
        return self.speed

    def get_destination(self):
        return self.destination

    def get_route(self):
        return self.route
