import random
from collections import namedtuple, deque
import numpy as np
import torch

Experience = namedtuple('Experience', ('state', 'action', 'reward', 'next_state', 'done'))

class ReplayBuffer:
    """Fixed-size buffer to store experience tuples."""

    def __init__(self, action_size, buffer_size, batch_size, device):
        """Initialize a ReplayBuffer object.
        Params
        ======
            action_size (int): dimension of each action
            buffer_size (int): maximum size of buffer
            batch_size (int): size of each training batch
            device (torch.device): device to run on (cpu/gpu)
        """
        self.action_size = action_size
        self.memory = deque(maxlen=buffer_size)  
        self.priorities = deque(maxlen=buffer_size) # Importance of each experience
        self.batch_size = batch_size
        self.experience = Experience
        self.device = device
    
    def add(self, state, action, reward, next_state, done):
        """Add a new experience to memory."""
        e = self.experience(state, action, reward, next_state, done)
        self.memory.append(e)
        # New experiences get max priority so they are definitely seen at least once!
        self.priorities.append(max(self.priorities, default=1.0))
    
    def sample(self):
        """
        Sample a batch, but smarter! 
        Experiences with high priority (= high error) are more likely to be picked.
        """
        probs = np.array(self.priorities)
        probs = probs / probs.sum()
        
        indices = np.random.choice(len(self.memory), self.batch_size, p=probs)
        experiences = [self.memory[i] for i in indices]

        states = torch.from_numpy(np.vstack([e.state for e in experiences if e is not None])).float().to(self.device)
        actions = torch.from_numpy(np.vstack([e.action for e in experiences if e is not None])).long().to(self.device)
        rewards = torch.from_numpy(np.vstack([e.reward for e in experiences if e is not None])).float().to(self.device)
        next_states = torch.from_numpy(np.vstack([e.next_state for e in experiences if e is not None])).float().to(self.device)
        dones = torch.from_numpy(np.vstack([e.done for e in experiences if e is not None]).astype(np.uint8)).float().to(self.device)
  
        return (states, actions, rewards, next_states, dones, indices)
    
    def update_priorities(self, indices, errors):
        """Update priorities based on TD error"""
        for i, error in zip(indices, errors):
            self.priorities[i] = abs(error) + 1e-5 # small constant to avoid zero probability

    def __len__(self):
        """Return the current size of internal memory."""
        return len(self.memory)
