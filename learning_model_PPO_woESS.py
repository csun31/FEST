import gym
from stable_baselines3 import A2C, PPO, DQN
from building_env_woESS import ENV_V3
import numpy as np
import os
from stable_baselines3.common.evaluation import evaluate_policy
#%%
env = ENV_V3()

models_dir = "models"
logdir = "logs"

if not os.path.exists(models_dir):
    os.makedirs(models_dir)

if not os.path.exists(logdir):
    os.makedirs(logdir)

# tensorboard --logdir logs/PPO_0/

#%% Un-comment  this section for re-train process
## PPO
# env.reset()
# model = PPO("MlpPolicy", env, verbose=1, tensorboard_log=logdir)
# TIMESTEPS = 10000
# iters = 0
# for i in range(100):
#     model.learn(total_timesteps=TIMESTEPS, reset_num_timesteps=False, tb_log_name="PPO")
#     model.save(f"{models_dir}/{TIMESTEPS*i}")

# del model  # delete trained model to demonstrate loading

#%% load model


model_path = f"{models_dir}/PPO_NO_ESS.zip"
model = PPO.load(model_path, env=env)
# model = A2C.load("model_A2C")
episodes = 1
REWARD = []
EPI_REW = []

SOC = []
PRICE = []
PDG = []
LOAD = []
EV = []
HVAC = []
TEMP = []
TOTAL_COST = []

for ep in range(episodes):
    obs = env.reset()
    done = False
    epi_reward = 0
    env.INVEST_TERM = 0
    cnt = 0
    while not done:
        cnt +=1
        action, _states = model.predict(obs, deterministic= True)
        p_obs = np.copy(obs)
        # soc.append(p_obs[0][0]) 
        obs, rewards, done, info = env.step(action)
        
        PDG.append(env.Pdg)
        SOC.append(obs[1])
        PRICE.append(obs[3])
        LOAD.append(obs[4])
        EV.append(env.Pev)
        HVAC.append(env.Phvac)
        TEMP.append(env.Tinit)
        # print(p_obs, action, obs, rewards, done)
        # print(env.INVEST_TERM)
        REWARD.append(rewards)
        epi_reward += rewards
        # env.render()
        # print(rewards)
    TOTAL_COST.append(env.Total_Cost)
    EPI_REW.append(epi_reward)
    
   
#     print('----------------------------------',cnt)

# import matplotlib.pyplot as plt
# plt.plot(REWARD)
# plt.title('Reward')
# plt.show()
# plt.plot(EPI_REW)
# plt.title('Episode Reward')
# plt.show()

# plt.plot(SOC)
# plt.title('SOC')
# plt.show()
# plt.plot(PDG)
# plt.title('DG generator')
# plt.show()
# plt.plot(PRICE)
# plt.title('Market price')
# plt.show()
# plt.plot(LOAD)
# plt.title('Load')
# plt.show()
# plt.plot(EV)
# plt.title('EV charging amount')
# plt.show()
# plt.plot(HVAC)
# plt.title('HVAC comsumption')
# plt.show()
# plt.plot(TEMP)
# plt.title('Room Temp')
# plt.show()
# print(sum(TOTAL_COST))

