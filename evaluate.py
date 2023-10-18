print("Libraries loading.. Wait..")

import argparse
from Env import PongEnv
import logging
from stable_baselines3 import PPO

try:
    parser = argparse.ArgumentParser(description="Load and evaluate a PPO model on PongEnv")
    parser.add_argument("--model", required=True, help="Path to the ZIP file containing the model")
    args = parser.parse_args()
    
    env = PongEnv()
    model = PPO.load(args.model, env=env)

    
    
except Exception as e:
    
    print(e)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)
    logger.error(f' Unknown path. Check the Model path or Folder')
        
    quit()
    
import os
from stable_baselines3.common.evaluation import evaluate_policy

evaluate_policy(model, env, n_eval_episodes=10)
