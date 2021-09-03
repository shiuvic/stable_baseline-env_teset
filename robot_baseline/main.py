import gym

from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common import make_vec_env
from stable_baselines import PPO2
from robot_baseline import robot

# multiprocess environment

env = make_vec_env('robot-v0', n_envs=1)

model = PPO2(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=30000)
model.save("ppo2_robot")

del model # remove to demonstrate saving and loading

model = PPO2.load("ppo2_robot")

# Enjoy trained agent
obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    # env.render()


import gym

# from stable_baselines3 import PPO
# from stable_baselines3.common.env_util import make_vec_env
#
# # Parallel environments
# env = make_vec_env('robot-v0', n_envs=1)
#
# model = PPO("MlpPolicy", env, verbose=1)
# model.learn(total_timesteps=1024,n_eval_episodes=3)
# model.save("ppo2_robot")
#
# del model # remove to demonstrate saving and loading
#
# model = PPO.load("ppo2_robot")
#
# obs = env.reset()
# while True:
#     action, _states = model.predict(obs)
#     obs, rewards, dones, info = env.step(action)
#     # env.render()


# model = PPO2.load("ppo2_robot")
# print(PPO2.get_parameters(model))