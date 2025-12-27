import gymnasium as gym
from gymnasium import spaces
import numpy as np
import logging

class AimsunEnv(gym.Env):
    """
    Custom Environment that follows gym interface for Aimsun Traffic Simulation.
    """
    metadata = {'render.modes': ['human']}

    def __init__(self, config, aimsun_api_instance=None):
        super(AimsunEnv, self).__init__()
        
        self.config = config
        
        if aimsun_api_instance:
            self.aimsun_api = aimsun_api_instance
        else:
            from src.core.aimsun_api import AimsunAPI
            self.aimsun_api = AimsunAPI()
            
        self.aimsun_api.connect()
        
        # Managers
        from src.core.simulation_manager import ScenarioManager, EventManager
        self.scenario_manager = ScenarioManager(config, self.aimsun_api)
        self.event_manager = EventManager(config, self.aimsun_api)

        # Multi-Agent Setup
        # We process each intersection independently but training happens centrally (for now)
        self.intersections = config['env'].get('intersections', [{'id': 1}]) # fallback
        self.num_agents = len(self.intersections)
        
        # Define action and observation space
        # Assuming all agents share the same state/action dims for simplicity in this version
        # If they differ, we'd need a Dict space (super complex)
        self.action_space = spaces.Discrete(config['env']['action_dim'])
        
        self.observation_space = spaces.Box(
            low=0, 
            high=np.inf, 
            shape=(config['env']['state_dim'],), 
            dtype=np.float32
        )
        
        self.logger = logging.getLogger(__name__)

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.logger.info("Resetting environment...")
        
        # Select and load a traffic scenario
        self.scenario_manager.select_scenario()
        
        # Check for stochastic events at start of episode
        self.event_manager.trigger_random_accident()
        
        # Reset Aimsun simulation
        # self.aimsun_api.reset_simulation() # If supported
        
        # Get initial state for ALL agents
        # For this version, we will concatenate them or just return the first one?
        # Let's return a list of states, but this breaks standard Gym. 
        # Hack: We will store the states internally and just return the first one to satisfy Gym check for now,
        # but the Agent must know to call get_all_states(). 
        # BETTER APPROACH: Assume Single Agent controlling ONE intersection for now in the gym loop, 
        # OR we treat the whole system as one giant state.
        
        # Let's go with "Giant State" approach - simpler for standard RL
        initial_state = np.random.rand(self.config['env']['state_dim']).astype(np.float32)
        info = {}
        return initial_state, info

    def step(self, action):
        # Execute action in Aimsun
        # If action is scalar, it might apply to all? Or we need a MultiDiscrete action space.
        # For now, let's assume the 'action' passed here is actually a LIST of actions if we changed the agent.
        # But since we didn't change the main loop to handle multi-agent yet, let's keep it simple:
        # One Master Agent controls specific intersection.
        
        junction_id = self.intersections[0]['id'] # Focus on the first one
        self.aimsun_api.set_traffic_light_phase(junction_id, action)
        
        # But we also want to simulate others maybe?
        # Random actions for others to add noise?
        for i in range(1, self.num_agents):
             other_junction = self.intersections[i]['id']
             self.aimsun_api.set_traffic_light_phase(other_junction, 0) # Default phase for others
        
        # Get new state and reward
        # Real implementation: Iterate over detectors defined in config to build state vector
        observation = np.random.rand(self.config['env']['state_dim']).astype(np.float32) 
        
        reward = self._calculate_reward(observation)
        
        # Simple termination for testing
        terminated = False 
        truncated = False 
        info = {}
        
        return observation, reward, terminated, truncated, info

    def _calculate_reward(self, observation):
        # Implement reward function based on config weights
        # For now, just a random reward + some logic based on 'observation' values
        weights = self.config['env']['reward_weights']
        
        # Mock calculation
        throughput = observation[0] * 10 
        wait_time = observation[1] * 5
        
        reward = (weights['throughput'] * throughput) + (weights['wait_time'] * wait_time)
        return reward

    def render(self, mode='human'):
        pass

    def close(self):
        self.aimsun_api.close()
