import logging
import os
import yaml
from torch.utils.tensorboard import SummaryWriter

def setup_logging(config_path="configs/logging.yaml", run_name="default"):
    """
    Sets up the logging configuration.
    """
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
    else:
        # Default config
        config = {'logging': {'log_dir': 'logs/', 'log_level': 'INFO'}}
    
    log_dir = os.path.join(config['logging']['log_dir'], run_name)
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure Python logging
    logging.basicConfig(
        level=getattr(logging, config['logging']['log_level']),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(os.path.join(log_dir, "app.log")),
            logging.StreamHandler()
        ]
    )
    
    # TensorBoard writer
    writer = None
    if config['logging'].get('tensorboard', False):
        writer = SummaryWriter(log_dir=log_dir)
        
    return logging.getLogger(__name__), writer

import pandas as pd

class MetricTracker:
    def __init__(self, writer, log_dir):
        self.writer = writer
        self.log_dir = log_dir
        self.episode_rewards = []
        self.metrics_file = os.path.join(log_dir, "training_metrics.csv")
        # Ensure file validation
        if not os.path.isfile(self.metrics_file):
            pd.DataFrame(columns=['Episode', 'Reward', 'Epsilon']).to_csv(self.metrics_file, index=False)
        
    def log_episode(self, episode, reward, epsilon):
        self.episode_rewards.append(reward)
        if self.writer:
            self.writer.add_scalar('Reward/Episode', reward, episode)
            self.writer.add_scalar('Epsilon/Episode', epsilon, episode)
        
        # Append to CSV for our cool streamlit dashboard
        df = pd.DataFrame([[episode, reward, epsilon]], columns=['Episode', 'Reward', 'Epsilon'])
        df.to_csv(self.metrics_file, mode='a', header=False, index=False)
            
    def close(self):
        if self.writer:
            self.writer.close()
