import numpy as np
from sklearn import preprocessing
import pandas as pd
import matplotlib.pyplot as plt

#%%


DATA = pd.read_excel(open('dataset_1.xlsx', 'rb'), sheet_name='data')
PRICES = DATA['PR']
CDG = (1.5-min(PRICES))/(max(PRICES)-min(PRICES))
#%%
# L = np.array(PRICES).reshape(-1,1)
# scaler = preprocessing.MinMaxScaler()
# PRICES = scaler.fit_transform(L).flatten()
CDG =1.5
#%%
LOAD = DATA['Load']
EV = DATA['EV']
HVAC = DATA['HVAC']
RDG = DATA['RDG']
GRID_ON = DATA['GRID_STATUS']
#%%
# total operation cost at t

def Rule_based(Tset):

    PEN_SHED = 5

    PMAX = 100

    ESS_CAP = 100
    INVEST_TERM = 0

    EV_REQ = 5
    PEN_EV = 10
    EV_ARV = 14
    EV_DEP = 79
    # actual EV load at t
    Pev = 0

    HVAC_REQ = 5
    HVAC_REQ_main = 1.5
    PEN_HVAC = 10
    #actual hvac load at t 
    Phvac = 0

    # Tset = 0

    #HVAC
    Tinit = 15

    SOC =0 

    BESS = []
    DG =[]
    PEV = []
    PHVAC = []

    for d in range(1):
        Total_Cost = 0
        for i in range(95):
            Pdg = 0
            Pb = 0
            Pev = 0 
            Phvac =0
            
            #dg
            if PRICES[i] >= 1.5:
                Pdg = PMAX
            
            #BESS
            if PRICES[i] < 1:
                SOC =1
                Pb = -ESS_CAP
            elif PRICES[i] >= 2:
                Pb = (SOC)*ESS_CAP
                SOC =0
            else:
                Pb = 0
            
            #EV 
            if i ==79:
                Pev = EV_REQ
            #HVAC
            # Tinit = 15
            # Tset = 25
            # dt = 2.5/interval
            if HVAC[i] ==1:
                if Tinit < Tset:
                    Phvac = HVAC_REQ
                    Tinit +=2.5
                else:
                    Tinit = Tset
                    Phvac = HVAC_REQ_main
                    
            else:
                Phvac = 0 
            # cost calculation
            if GRID_ON[i]==1:
                delta_P = Pdg + RDG[i] + Pb - LOAD[i] - Pev - Phvac
                Total_Cost += CDG*Pdg - delta_P*PRICES[i]
            else:
                Pdg = PMAX
                delta_P = Pdg + RDG[i] + Pb - LOAD[i] - Pev - Phvac
                if delta_P>=0:
                    Pdg-= min(delta_P, 100)
                    Total_Cost += CDG*Pdg
                else:
                    Total_Cost += CDG*Pdg - delta_P*PEN_SHED
            
            BESS.append(SOC)
            DG.append(Pdg)
            PEV.append(Pev)
            PHVAC.append(Phvac)

    
    return BESS,DG,PEV,PHVAC,Total_Cost,Tset
    #return Total_Cost
# plt.plot(BESS)
# plt.title('SOC')
# plt.show()
# plt.plot(DG)
# plt.title('DG generator')
# plt.show()
# plt.plot(PEV)
# plt.title('EV charging amount')
# plt.show()
# plt.plot(PHVAC)
# plt.title('HVAC comsumption')
# plt.show()
# print(Total_Cost)





            
        
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
        