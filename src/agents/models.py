import torch
import torch.nn as nn
import torch.nn.functional as F

class QNetwork(nn.Module):
    """Actor (Policy) Model."""

    def __init__(self, state_size, action_size, seed, hidden_layers=[128, 128]):
        """
        Building the Dueling DQN Brain!
        Instead of just one path, we split into two:
        1. How good is the state? (Value)
        2. How good is each action? (Advantage)
        Combine them at the end for the final Q-value. simple but effective.
        """
        super(QNetwork, self).__init__()
        self.seed = torch.manual_seed(seed)
        
        # Feature extraction layer (The common body)
        # We process the raw traffic data here before splitting
        self.fc1 = nn.Linear(state_size, hidden_layers[0])
        self.fc2 = nn.Linear(hidden_layers[0], hidden_layers[1])
        
        # Stream 1: Value Function V(s) - One output
        # Tells us: "Man, this traffic situation is terrible/great" regardless of what we do
        self.value_stream = nn.Linear(hidden_layers[1], 1)
        
        # Stream 2: Advantage Function A(s, a) - Action_size outputs
        # Tells us: "Turning green now is X much better than staying red"
        self.advantage_stream = nn.Linear(hidden_layers[1], action_size)

    def forward(self, state):
        """
        Forward pass through the brain.
        Propagate, split, then merge.
        """
        # Pass through the common layers first
        x = F.relu(self.fc1(state))
        x = F.relu(self.fc2(x))
        
        # Split into two streams
        val = self.value_stream(x)
        adv = self.advantage_stream(x)
        
        # Combine them using the dueling formula:
        # Q(s,a) = V(s) + (A(s,a) - mean(A(s,a)))
        # This normalization helps with stability.
        return val + (adv - adv.mean(dim=1, keepdim=True))
