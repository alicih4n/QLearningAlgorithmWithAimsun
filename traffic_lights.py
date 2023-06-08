import random

class TrafficLights:
    def __init__(self, junction_id, initial_state='red', durations=None):
        self.junction_id = junction_id
        self.states = ['green', 'yellow', 'red']
        self.current_state = initial_state
        self.durations = durations if durations else {'green': 30, 'yellow': 5, 'red': 25}
        self.timer = 0
        self.priority = None

    def update_state(self):
        if self.current_state == 'green':
            if self.timer >= self.durations['green']:
                self.current_state = 'yellow'
                self.timer = 0
            else:
                self.timer += 1
        elif self.current_state == 'yellow':
            if self.timer >= self.durations['yellow']:
                self.current_state = 'red'
                self.timer = 0
            else:
                self.timer += 1
        elif self.current_state == 'red':
            if self.timer >= self.durations['red']:
                self.current_state = 'green'
                self.timer = 0
            else:
                self.timer += 1

    def get_state(self):
        return self.current_state

    def set_state(self, state):
        if state in self.states:
            self.current_state = state
        else:
            raise ValueError('Geçersiz durum!')

    def get_duration(self, state):
        return self.durations[state]

    def set_duration(self, state, duration):
        self.durations[state] = duration

    def get_remaining_time(self):
        return self.durations[self.current_state] - self.timer

    def randomize_durations(self, min_duration=10, max_duration=60):
        for state in self.states:
            self.durations[state] = random.randint(min_duration, max_duration)

    def set_priority(self, priority):
        self.priority = priority

    def get_priority(self):
        return self.priority

    def print_info(self):
        print(f"Junction ID: {self.junction_id}")
        print(f"Current State: {self.current_state}")
        for state in self.states:
            print(f"{state.capitalize()} Duration: {self.durations[state]}")
        if self.priority:
            print(f"Priority: {self.priority}")
        else:
            print("Priority: None")
