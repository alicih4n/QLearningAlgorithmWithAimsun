# Aimsun Deep Reinforcement Learning Platform

This project implements a Deep Reinforcement Learning (DQN) agent to control traffic lights using the Aimsun traffic simulator. It represents a significant upgrade from generic Q-Learning to a modular, research-grade deep learning architecture.

## 🚀 Key Features
- **Deep Q-Network (DQN)**: Uses PyTorch to approximate Q-values, handling complex state spaces better than tabular Q-learning.
- **Gymnasium Interface**: The Aimsun environment is wrapped in a standard Gym interface, allowing for easy swapping of agents (PPO, A2C, etc.).
- **Modular Architecture**: Clean separation between Environment, Agent, and experimental configurations.
- **Config-Driven**: run experiments by simply changing `gamma`, `lr`, or `layers` in the YAML config files.

## 📂 Project Structure
```
Aimsun_RL_Project/
├── configs/                # Configuration files
│   ├── simulation.yaml     # Aimsun settings
│   ├── agent.yaml          # DQN Hyperparameters
│   └── logging.yaml        # Logging settings
├── src/
│   ├── core/
│   │   ├── aimsun_env.py   # Gym Wrapper for Aimsun
│   │   └── aimsun_api.py   # API Driver (Mock implementation included)
│   ├── agents/
│   │   ├── dqn_agent.py    # DQN Agent Logic
│   │   └── models.py       # PyTorch Neural Network
│   ├── utils/
│   │   └── memory.py       # Experience Replay Buffer
│   └── analysis/
│       └── logger.py       # Tensorboard & File Logging
├── main.py                 # Main training script
├── requirements.txt
└── README.md
```

## 🛠️ Getting Started

### 1. Prerequisites
- Python 3.8+
- Aimsun Next (with API license if running real simulation)

### 2. Installation
```bash
pip install -r requirements.txt
```

### 3. Running the Training Loop
To start training the agent (currently using the mock API for demonstration):
```bash
python main.py
```
This will initialize the environment, load the agent, and start the training loop, printing metrics to the console.

### 4. Configuration
Modify `configs/agent.yaml` to experiment with different hyperparameters:
```yaml
agent:
  learning_rate: 0.001
  batch_size: 64
  hidden_layers: [128, 128]
```

## 📊 Results & Visualization
Training logs are saved to `logs/`. You can visualize them using TensorBoard:
```bash
tensorboard --logdir logs/
```

## 🔗 Aimsun Connection
To connect to a real Aimsun instance:
1. Open `configs/simulation.yaml` and set the correct paths to your `.ang` and `.cntl` files.
2. Update `src/core/aimsun_api.py` to implement the actual communication logic (e.g., using Aimsun's Python scripting interface or a TCP socket server).
