import random
import logging

class ScenarioManager:
    def __init__(self, config, aimsun_api):
        self.config = config['simulation']
        self.aimsun_api = aimsun_api
        self.scenarios = list(self.config.get('scenarios', {}).keys())
        self.current_scenario = None
        self.logger = logging.getLogger(__name__)

    def select_scenario(self, scenario_name=None):
        """
        Selects a traffic scenario. If name is not provided, selects randomly.
        """
        if not self.scenarios:
            self.logger.warning("No scenarios defined in configuration.")
            return

        if scenario_name is None:
            scenario_name = random.choice(self.scenarios)
            
        if scenario_name not in self.scenarios:
            raise ValueError(f"Scenario {scenario_name} not found in config.")

        self.current_scenario = scenario_name
        settings = self.config['scenarios'][scenario_name]
        
        self.logger.info(f"Loading Scenario: {scenario_name}")
        self.aimsun_api.load_traffic_demand(settings['traffic_demand'])
        self.aimsun_api.load_control_file(settings['control_plan'])

        return scenario_name

class EventManager:
    def __init__(self, config, aimsun_api):
        self.config = config['simulation'].get('stochastic_events', {})
        self.aimsun_api = aimsun_api
        self.logger = logging.getLogger(__name__)
        self.active_event = None

    def check_for_event(self, step):
        """
        Checks if a random event should occur at this step.
        This is a simplified check (e.g., probability per episode roughly).
        """
        if not self.config.get('enabled', False):
            return

        # Simple logic: Single event check at start of episode or periodically
        # Here we just implement a trigger method
        pass

    def trigger_random_accident(self):
        """
        Simulate an accident on a random link.
        """
        if random.random() < self.config.get('accident_probability', 0):
             duration = random.randint(*self.config['accident_duration_range'])
             # In a real simulation, we would select a link ID
             link_id = 123 
             self.logger.info(f"Stochastic Event: Accident on Link {link_id} for {duration}s")
             self.aimsun_api.close_lane(link_id, duration)
