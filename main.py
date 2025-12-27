import yaml
import os
import numpy as np
import time
from collections import deque
from src.core.aimsun_env import AimsunEnv
from src.agents.dqn_agent import DQNAgent
from src.analysis.logger import setup_logging, MetricTracker

def load_config(path):
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def run():
    # Load Configurations
    sim_config = load_config("configs/simulation.yaml")
    agent_config = load_config("configs/agent.yaml")
    
    # Setup Logging
    log_dir = "logs" # simplistic, better from config
    logger, writer = setup_logging("configs/logging.yaml", run_name=f"run_{int(time.time())}")
    # We need to extract the actual log path constructed in setup_logging to be consistent, but let's just pass the root for now or fix logging.
    # Actually setup_logging returns the logger but not the specific dir. 
    # Let's simple hardcode a path that both agree on or re-parse. 
    # For now, let's just assume logs/latest for the dashboard.
    
    tracker = MetricTracker(writer, log_dir="logs/") # Just dumping in root logs/ for simplicity of the dashboard finding it.
    
    logger.info("Initializing Aimsun Environment...")
    env = AimsunEnv(sim_config)
    
    # Get State and Action sizes
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    
    logger.info(f"State Size: {state_size}, Action Size: {action_size}")
    
    # Initialize Agent
    agent = DQNAgent(state_size=state_size, action_size=action_size, seed=sim_config['simulation']['random_seed'], config=agent_config['agent'])
    
    # Training Loop
    n_episodes = agent_config['training']['episodes']
    max_t = agent_config['training']['max_steps_per_episode']
    eps_start = agent_config['agent']['epsilon_start']
    eps_end = agent_config['agent']['epsilon_end']
    eps_decay = agent_config['agent']['epsilon_decay']
    
    scores = []                        # list containing scores from each episode
    scores_window = deque(maxlen=100)  # last 100 scores
    eps = eps_start                    # initialize epsilon
    
    for i_episode in range(1, n_episodes + 1):
        state, _ = env.reset()
        score = 0
        for t in range(max_t):
            action = agent.act(state, eps)
            next_state, reward, done, truncated, _ = env.step(action)
            
            agent.step(state, action, reward, next_state, done)
            state = next_state
            score += reward
            
            if done or truncated:
                break 
                
        scores_window.append(score)       # save most recent score
        scores.append(score)              # save most recent score
        
        eps = max(eps_end, eps_decay * eps) # decrease epsilon
        
        tracker.log_episode(i_episode, score, eps)
        
        print('\rEpisode {}\tAverage Score: {:.2f}'.format(i_episode, np.mean(scores_window)), end="")
        if i_episode % 100 == 0:
            print('\rEpisode {}\tAverage Score: {:.2f}'.format(i_episode, np.mean(scores_window)))
            
        if i_episode % agent_config['logging']['save_freq'] == 0:
             # Save model
             # agent.save("checkpoint.pth")
             pass

    tracker.close()
    logger.info("Training finished.")

if __name__ == "__main__":
    run()
