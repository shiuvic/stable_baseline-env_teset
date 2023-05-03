##PPO

from stable_baselines3.common.env_util import make_vec_env
from stable_baselines3 import PPO
from robot_baseline import robot

# multiprocess environment

env = make_vec_env('robot-v0', n_envs=1)

model = PPO("MlpPolicy", env, verbose=1)
model.learn(total_timesteps=124805)
# model.save("ppo2_robot")

# del model # remove to demonstrate saving and loading
#
# model = PPO2.load("ppo2_robot")
#
# # Enjoy trained agent
# obs = env.reset()
# while True:
#     action, _states = model.predict(obs)
#     obs, rewards, dones, info = env.step(action)
#     env.render()

