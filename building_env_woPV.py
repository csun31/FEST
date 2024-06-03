import numpy as np
import gym 
from gym import spaces
from sklearn import preprocessing
import pandas as pd
#%%

class ENV_V3(gym.Env):
    #the agent need to find the way to go to the target and avoid hitting the wall
    metadata ={'render.modes':['console']}
    #define constants
    ACTION = []
    for action_ess in [0, 1, -1]:
        for action_dg in [0, 1]:
            for action_ev in [0, 1]:
                for action_hvac in [0, 1]:
                    ACTION.append([action_ess, action_dg, action_ev, action_hvac])
    CHARGE = 1
    IDLE = 0
    DISCHAR = -1
    
    DATA = pd.read_excel(open('dataset_1.xlsx', 'rb'), sheet_name='data')
    PRICES = DATA['PR']
    PRICES_ORG = DATA['PR']
    LOAD = DATA['Load']
    LOAD_ORG = DATA['Load']
    EV = DATA['EV']
    HVAC = DATA['HVAC']
    RDG = DATA['RDG']*0
    GRID_ON = DATA['GRID_STATUS']
    # penalty of load shedding
    PEN_SHED = 5
    
    CDG = (1.5-min(PRICES))/(max(PRICES)-min(PRICES))
    PMAX = 100
    Pdg = 0 
    
    ESS_CAP = 100
    INVEST_TERM = 0
    
    EV_REQ = 5
    PEN_EV = 10
    EV_ARV = 14
    EV_DEP = 79
    # actual EV load at t
    Pev = 0
    
    # power consumption for maintaining constant temp
    HVAC_REQ_main = 1.5
    # power consumption for increase temp to temp_set (increase 2.5deg in 1 interval)
    HVAC_REQ = 5
    # initial temp (oC)
    Tinit = 15    ### taken from GUI
    # initial temp (oC)
    Tset = 0 ### taken from GUI
    PEN_HVAC = 10
    #actual hvac load at t 
    Phvac = 0
    
    #Grid-connection status!!! Reading from GUI

    # total operation cost at t
    Total_Cost = 0
    
    def __init__(self):
        super(ENV_V3, self).__init__()
        # size of the grid
        # define action and state space
        n_action = len(self.ACTION)
        self.action_space = spaces.Discrete(n_action)
        self.observation_space = spaces.Box(low = 0, high = 1, 
                                            shape = (7,), dtype= np.float32)
   
    def cust_temp(self,temp):
        self.Tset = temp        
        return self.Tset

    def cost_calculation(self):
        pass
        
    
    def list_normalization(self):
        L = np.array(self.PRICES).reshape(-1,1)
        scaler = preprocessing.MinMaxScaler()
        self.PRICES = scaler.fit_transform(L).flatten()
        
        L2 = np.array(self.LOAD).reshape(-1,1)
        scaler2 = preprocessing.MinMaxScaler()
        self.LOAD = scaler2.fit_transform(L2).flatten()
        
    def reset(self):
        # observation should be an array 
        # return also an array
        self.list_normalization()
        # dg, soc, ev_req, price, load, hvac_req, grid on/off
        self.obs = [0.0,0.0,0.0, 0.142857, 0.12937799, 0.0, 1.0]
        self.count = 0
        self.Total_Cost = 0
        self.Pdg = 0
        self.Tinit = 15 ###taken from GUI
        return np.array(self.obs).astype(np.float32)
    
    def step(self, action):
        done = False
        reward =0
        action_bat = self.ACTION[action][0]
        action_dg = self.ACTION[action][1]
        action_ev = self.ACTION[action][2]
        action_hvac = self.ACTION[action][3]
       
        
        dg = self.obs[0]
        soc = self.obs[1]
        ev_req = self.obs[2]
        price = self.obs[3]
        load = self.obs[4]
        hvac_req = self.obs[5]
        grid_status = self.obs[6]
        
        dg_ = 0
        soc_ = 0
        ev_req_ = 0
        price_ = 0
        load_ = 0
        hvac_req_ = 0
        grid_status_ = 0
        
        Pb =0 # discharging amount from BESS
        
        ### reward for dg
        self.Pdg = self.PMAX*action_dg
        reward_dg= (price - self.CDG)*self.Pdg
        if action_dg==1:
            dg_ =1
        
        ### reward for battery
        if action_bat == self.DISCHAR: # discharge
            if soc<=0:
                reward=-1
                soc_ = 0
                self.count+=1
                price_ = self.PRICES[int(self.count)]
            else:
                # print('dis', self.INVEST_TERM)
                reward= price*self.ESS_CAP - self.INVEST_TERM
                self.INVEST_TERM = 0
                self.count+=1
                soc_ = soc-1
                price_ = self.PRICES[int(self.count)]
                Pb = self.ESS_CAP
        elif action_bat == self.IDLE: # keep same
            self.count+=1
            soc_ = soc
            price_ = self.PRICES[int(self.count)]
            reward=0
        elif action_bat == self.CHARGE: #charge
            if soc>=1:
                soc_ = soc
                self.count+=1
                price_ = self.PRICES[int(self.count)]
                reward=-1
            else:
                self.INVEST_TERM += price*self.ESS_CAP
                # print('char', self.INVEST_TERM)
                self.count+=1
                soc_ = 1.0
                price_ = self.PRICES[int(self.count)]
                Pb = -self.ESS_CAP
        else:
            raise ValueError(f'Receive an invalid action = {action_bat}')
        
        
        penalty_hvac = hvac_req*(1-action_hvac)*self.PEN_HVAC
        if hvac_req == 0 and action_hvac == 1:
            penalty_hvac = self.PEN_HVAC
        
        # if tempt < temp_set: HVAC_REQ = 5
        # else: HVAC_REQ = 1.5 for maintaining a constant temp
        # print(action_hvac)
        if action_hvac == 1:
            if self.Tinit < self.Tset:
                self.Phvac = self.HVAC_REQ*action_hvac
            else:
                self.Tinit = self.Tset
                self.Phvac = self.HVAC_REQ_main*action_hvac
            self.Tinit +=2.5
        else:
            self.Phvac = 0 
        hvac_req_ = self.HVAC[int(self.count)]
        grid_status_ = self.GRID_ON[int(self.count)]
        
        ###EV
        penalty_ev = 0
        ev_req_ = 0
        self.Pev=0
        if self.EV_ARV== (self.count-1):
            ev_req = 1
        if self.EV_ARV<= (self.count-1)<=self.EV_DEP:
            if action_ev==1:
                ev_req_ = 0
                self.Pev = self.EV_REQ*action_ev*ev_req
            else:
                ev_req_ = ev_req
            
        if (self.count-1)==self.EV_DEP:
            if action_ev == 0 and ev_req == 1:
                penalty_ev = self.PEN_EV
                
        load_ = self.LOAD[int(self.count)]
            
        self.obs[0] = dg_
        self.obs[1] = soc_
        self.obs[2] = ev_req_
        self.obs[3] = price_
        self.obs[4] = load_
        self.obs[5] = hvac_req_
        self.obs[6] = grid_status_
                
        if (self.count== 95):
            done = True
            if action_bat != self.DISCHAR:
                reward = soc*price*self.ESS_CAP - self.INVEST_TERM
            # self.INVEST_TERM = 0
        
        delta_P = self.Pdg + self.RDG[self.count-1] + Pb - self.LOAD_ORG[self.count-1] - self.Pev - self.Phvac
        # print('Pdg ,self.RDG[self.count-1] ,Pb , self.LOAD_ORG[self.count-1] ,self.Pev ,self.Phvac')
        # print(Pdg ,self.RDG[self.count-1] ,Pb , self.LOAD_ORG[self.count-1] ,self.Pev ,self.Phvac)
        
        if self.GRID_ON[self.count-1]==1:
            pen_power_balance = 0
            self.Total_Cost += 1.5*self.Pdg - delta_P*self.PRICES_ORG[self.count-1]
        else:
            if delta_P >= 0:
                pen_power_balance = 0
                self.Pdg-= delta_P
                self.Total_Cost += 1.5*self.Pdg
            else:
                pen_power_balance = abs(delta_P)*self.PEN_SHED
                self.Total_Cost += 1.5*self.Pdg - delta_P*self.PEN_SHED
        # add info about the env
        info = {}
        
        return np.array(self.obs).astype(np.float32), (reward + reward_dg - penalty_hvac - penalty_ev-pen_power_balance), done, info
    
    def render(self, mode = 'console'):
        pass
    
    def close(self):
        pass
        
        
        
        
            
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        