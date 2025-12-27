import numpy as np
import random
import torch
import torch.nn.functional as F
import torch.optim as optim
from src.agents.models import QNetwork
from src.utils.memory import ReplayBuffer

class DQNAgent:
    """Interacts with and learns from the environment."""

    def __init__(self, state_size, action_size, seed, config):
        """Initialize an Agent object.
        Params
        ======
            state_size (int): dimension of each state
            action_size (int): dimension of each action
            seed (int): random seed
            config (dict): agent configuration
        """
        self.state_size = state_size
        self.action_size = action_size
        self.seed = random.seed(seed)
        self.config = config

        # Hyperparameters
        self.batch_size = config['batch_size']
        self.gamma = config['gamma']
        self.tau = 1e-3              # for soft update of target parameters, hardcoding for now or move to config
        self.lr = config['learning_rate']
        self.update_every = config.get('update_every', 4)

        # Device selection
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        # Q-Network
        hidden_layers = config.get('hidden_layers', [64, 64])
        self.qnetwork_local = QNetwork(state_size, action_size, seed, hidden_layers).to(self.device)
        self.qnetwork_target = QNetwork(state_size, action_size, seed, hidden_layers).to(self.device)
        self.optimizer = optim.Adam(self.qnetwork_local.parameters(), lr=self.lr)

        # Replay memory
        self.memory = ReplayBuffer(action_size, config['memory_size'], self.batch_size, self.device)
        self.t_step = 0
    
    def step(self, state, action, reward, next_state, done):
        # Save experience in replay memory
        self.memory.add(state, action, reward, next_state, done)
        
        # Learn every UPDATE_EVERY time steps.
        self.t_step = (self.t_step + 1) % self.update_every
        if self.t_step == 0:
            # If enough samples are available in memory, get random subset and learn
            if len(self.memory) > self.batch_size:
                experiences = self.memory.sample()
                self.learn(experiences, self.gamma)

    def act(self, state, eps=0.):
        """Returns actions for given state as per current policy.
        
        Params
        ======
            state (array_like): current state
            eps (float): epsilon, for epsilon-greedy action selection
        """
        state = torch.from_numpy(state).float().unsqueeze(0).to(self.device)
        self.qnetwork_local.eval() # set to evaluation mode
        with torch.no_grad():
            action_values = self.qnetwork_local(state)
        self.qnetwork_local.train() # set back to training mode

        # Epsilon-greedy action selection
        if random.random() > eps:
            return np.argmax(action_values.cpu().data.numpy())
        else:
            return random.choice(np.arange(self.action_size))

    def learn(self, experiences, gamma):
        """Update value parameters using given batch of experience tuples.

        Params
        ======
            experiences (Tuple[torch.Tensor]): tuple of (s, a, r, s', done) tuples 
            gamma (float): discount factor
        """
        states, actions, rewards, next_states, dones, indices = experiences

        ## Compute and minimize the loss
        
        # Double DQN Magic happens here:
        # 1. Use Local network to decide BEST action for next state (this avoids overestimation bias)
        # 2. Use Target network to calculate the Q-value of that best action
        
        # Step 1: Selection
        best_actions = self.qnetwork_local(next_states).max(1)[1].unsqueeze(1)
        
        # Step 2: Evaluation
        # We gather the values from the target network corresponding to the selected actions
        Q_targets_next = self.qnetwork_target(next_states).detach().gather(1, best_actions)
        
        # Compute Q targets for current states 
        Q_targets = rewards + (gamma * Q_targets_next * (1 - dones))

        # Get expected Q values from local model
        Q_expected = self.qnetwork_local(states).gather(1, actions)

        # Compute TD errors for Prioritized Replay
        # We need the absolute error to tell the memory "Hey, we messed up big time on these samples, show me them again!"
        td_errors = (Q_targets - Q_expected).detach().cpu().numpy().squeeze()
        self.memory.update_priorities(indices, td_errors)
        
        # Compute loss (MSE is standard, but Huber loss can be more robust against outliers)
        loss = F.mse_loss(Q_expected, Q_targets)
        
        # Minimize the loss
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        # ------------------- update target network ------------------- #
        self.soft_update(self.qnetwork_local, self.qnetwork_target, self.tau)                     

    def soft_update(self, local_model, target_model, tau):
        """Soft update model parameters.
        θ_target = τ*θ_local + (1 - τ)*θ_target

        Params
        ======
            local_model (PyTorch model): weights will be copied from
            target_model (PyTorch model): weights will be copied to
            tau (float): interpolation parameter 
        """
        for target_param, local_param in zip(target_model.parameters(), local_model.parameters()):
            target_param.data.copy_(tau*local_param.data + (1.0-tau)*target_param.data)
