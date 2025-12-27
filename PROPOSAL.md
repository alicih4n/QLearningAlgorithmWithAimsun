# Project Transformation Proposal: Aimsun Deep RL Platform

## 1. Executive Summary
This proposal outlines the transformation of the existing generic Q-Learning script into a professional, modular Deep Reinforcement Learning (DRL) platform for Intelligent Transportation Systems (ITS) using Aimsun. The new architecture will be robust, scalable, and research-grade.

## 2. Proposed Architecture (Pillar 1)
We will transition from a flat file structure to a modular package structure.

```text
Aimsun_RL_Project/
├── configs/                # Configuration files
│   ├── simulation.yaml     # Aimsun settings (network path, duration, etc.)
│   ├── agent.yaml          # Hyperparameters (alpha, gamma, epsilon, batch_size)
│   └── logging.yaml        # Logging settings
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── environment.py  # Gym-compatible generic Environment wrapper
│   │   └── aimsun_env.py   # Specific implementation for Aimsun API
│   ├── agents/
│   │   ├── base_agent.py   # Abstract base class
│   │   ├── dqn_agent.py    # Deep Q-Network implementation
│   │   └── models.py       # PyTorch Neural Network definitions
│   ├── utils/
│   │   ├── logic_utils.py  # Helper functions
│   │   └── memory.py       # Replay Buffer implementation
│   └── analysis/
│       ├── logger.py       # Metrics tracking and Tensorboard integration
│       └── plotter.py      # Real-time visualization
├── main.py                 # Main entry point for training
├── evaluate.py             # Entry point for testing/visualization
├── requirements.txt
└── README.md
```

## 3. Technology Stack
- **Language**: Python 3.8+
- **Deep Learning Framework**: PyTorch (Standard for research and DRL)
- **RL Interface**: Gymnasium (Standard API for RL environments)
- **Configuration**: Hydra or standard YAML
- **Logging**: Tensorboard & Python logging

## 4. Implementation Plan

### Phase 1: Foundation (Architectural Modernization)
- **Action**: Create the directory structure.
- **Action**: Implement `src/configs` and config loading logic.
- **Action**: Create `src/core/aimsun_env.py`. This will abstract the Aimsun API logic (handling connection, state retrieval using detectors, and action execution for traffic lights). Using a proper class structure will fix the imports and dependency issues seen in the old code.

### Phase 2: The Agent (Algorithmic Sophistication)
- **Action**: Implement `src/utils/memory.py` (Experience Replay).
- **Action**: Create `src/agents/models.py` defining a Deep Q-Network (MLP or CNN if using visual inputs, but likely MLP for state vectors).
- **Action**: Implement `src/agents/dqn_agent.py` enabling Double DQN logic.

### Phase 3: Evaluation & Simulation (Complexity & Realism)
- **Action**: Implement `src/analysis/logger.py` to track rewards, queue lengths, and waiting times.
- **Action**: Create `evaluate.py` to run the agent without exploration (epsilon=0) and record metrics.

### Phase 4: Polish (Documentation)
- **Action**: Write a comprehensive `README.md`.
- **Action**: Add type hinting and docstrings to all code.

## 5. Next Steps
Upon approval of this plan, I will begin with **Phase 1**, creating the directory structure and the foundational `Environment` class.
