from PyQt5.QtWidgets import  QVBoxLayout,QWidget,QApplication ,QHBoxLayout,QDialog,QPushButton,QMainWindow,QGridLayout,QLabel
from PyQt5.QtGui import QIcon,QPixmap,QFont
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import sys

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTabWidget, QDialog, QDialogButtonBox, QFormLayout, QVBoxLayout, QPushButton, QAction, QLineEdit, QMessageBox, QLabel, QInputDialog, QPushButton
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import pyqtSlot
import matplotlib.pyplot as plt

import pandas as pd
import matplotlib.image as mpimg
import numpy as np
import random



DATA = pd.read_excel(open('dataset_1.xlsx', 'rb'), sheet_name='data')
PRICES = DATA['PR']
LOAD = DATA['Load']
EV = DATA['EV']
HVAC = DATA['HVAC']
RDG = DATA['RDG']
GRID_ON = DATA['GRID_STATUS']

D = np.zeros(shape=(96,30))
w = np.zeros(shape=(96,30))
pi = np.zeros(shape=(96,30))

# a =  np.add(LOAD , random.uniform(-1, 1)*LOAD*0.01)
# print(a)
for x in range(30):
    D[:,x] =  np.add(LOAD , random.gauss(-1, 1)*LOAD*0.05) # base power demand (30 scenarios)
    w[:,x] =  np.add(RDG , random.gauss(-1, 1)*RDG*0.05) # Power output of the renewable (30 scenarios)
    pi[:,x] = np.add(PRICES , random.gauss(-1, 1)*PRICES*0.05) # Time of use electricity price (30 scenarios)

class WindowClass(QMainWindow):

    def __init__(self,parent=None):

        super().__init__()
        self.setWindowTitle("Outline: Resilient Proactive Scheduling for a Commercial Building")            
        self.central_widget = QWidget()               
        self.setCentralWidget(self.central_widget) 
        pixmap = QPixmap('Fig3_.png')  
        scale = 1

        size = pixmap.size()

        scaled_pixmap = pixmap.scaled(scale * size)

        #label.setPixmap(scaled_pixmap) 
        lay = QVBoxLayout(self.central_widget)            
        label = QLabel(self)
        
        #label.setPixmap(pixmap)   
        label.setPixmap(scaled_pixmap)         
        lay.addWidget(label)
        self.show()


    def showDialog(self):
        #  vbox=QVBoxLayout()
        #  hbox=QHBoxLayout()
         self = QDialog()
         # self.dialog.resize(100,100)
         self.setFixedSize(690, 745)
         self.first = QLineEdit(self)
         self.second = QLineEdit(self)
         self.third = QLineEdit(self)
         self.fourth = QLineEdit(self)
         #self.fifth = QLineEdit(self)
         self.first.setFont(QFont("Arial",10))
         self.second.setFont(QFont("Arial",10))
         self.third.setFont(QFont("Arial",10))
         self.fourth.setFont(QFont("Arial",10))
         #self.fifth.setFont(QFont("Arial",10))
         title = 'Resilient Proactive Scheduling for a Commercial Building'
         self.setWindowTitle(title)

         layout = QFormLayout(self)
         layout.addRow("Demo Case: ", self.first)
         layout.addRow("Interruption start time : ", self.second)
         layout.addRow("Interruption end time :  ", self.third)
         layout.addRow("HVAC desired temperature (°F) : ", self.fourth)
        #  layout.addRow("5. Confidence level: ", self.fourth)
        #  self.b = QPlainTextEdit(self)
        #  # self.b.insertPlainText('Reference input values: 73, 104, 48, 0, 0.95')
        #  self.b.insertPlainText('Available Cases: 1, 2, 3.')
        #  self.b.move(7,200)
        #  self.b.resize(650,40)

         self.c = QPlainTextEdit(self)
         self.c.insertPlainText('Notes: \n\n1. Available demo cases: 1, 2, 3.\
                \nCase 1: Both Energy Storage System (ESS) and PV are available. \
                \nCase 2: Energy Storage System (ESS) is not available, and PV is available. \
                \nCase 3: Energy Storage System (ESS) is available, and PV is not available. \
                \n\n2. By default we consider the interruption happened between 60th-70th (time slot). Each time slot is 15 min.\
                \n\n3. The recommeneded value for HAVC desired temperature is 77°F (25°C). \
                \n\nWarning: The inputs far from the reommended values may lead to retraining the model, which needs a couple of hours. ')
 
         self.c.move(9,250)
         self.c.resize(650,400)
         buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
         buttonBox.setFont(QFont('Times', 10))       
         layout.addWidget(buttonBox)

         buttonBox.accepted.connect(self.accept)
         buttonBox.rejected.connect(self.reject)
        
         font = QFont("Times", 10, QFont.Bold)
         self.setFont(font)

         self.exec_()
         #self.getInputs()

         #def getInputs(self):
         # return (self.first.text(), self.second.text())
         return (self.first.text(),self.second.text(),self.third.text(),self.fourth.text())

class plotWindow():
    def __init__(self, parent=None):
        super().__init__()
        self.app = QApplication(sys.argv)
        self.MainWindow = QMainWindow()
        self.MainWindow.__init__()
        self.MainWindow.setWindowTitle("plot window")
        self.canvases = []
        self.figure_handles = []
        self.toolbar_handles = []
        self.tab_handles = []
        self.current_window = -1
        self.tabs = QTabWidget()
        self.tabs.setFont(QFont("Arial",12))
        self.MainWindow.setCentralWidget(self.tabs)
        self.MainWindow.resize(1300, 1300)
        self.MainWindow.show()


    def addPlot(self, title, figure, text):
        new_tab = QWidget()
        layout = QVBoxLayout()
        new_tab.setLayout(layout)

        # figure.subplots_adjust(left=0.05, right=0.99, bottom=0.05, top=0.81, wspace=0.2, hspace=0.2)
        figure.subplots_adjust(left=0.05, right=0.99, bottom=0.15, top=0.75, wspace=0.2, hspace=0.5)
        new_canvas = FigureCanvas(figure)
        new_toolbar = NavigationToolbar(new_canvas, new_tab)
        new_text = QLabel(text)
        new_text.move(2000,500)
        new_text.resize(500,30)
        font = QFont("Times", 14, QFont.Bold)
        new_text.setFont(font)

        layout.addWidget(new_canvas)
        layout.addWidget(new_text)
        layout.addWidget(new_toolbar)

        self.tabs.addTab(new_tab, title)

        self.toolbar_handles.append(new_toolbar)
        self.canvases.append(new_canvas)
        self.figure_handles.append(figure)
        self.tab_handles.append(new_tab)
        #self.l1=[]

    def show(self):
        self.app.exec_()


if __name__=="__main__":
    app=QApplication(sys.argv)
    win=WindowClass()
    win.show()
    inputs = win.showDialog()
    print('inputs',inputs)

    case = inputs[0]
    temp = (float(inputs[3]) - 32) * 5/9
    import building_env as BE
    import building_env_woESS as BE_woESS
    import building_env_woPV as BE_woPV
    exe = BE.ENV_V3.cust_temp(BE.ENV_V3,temp)
    exe1 = BE_woESS.ENV_V3.cust_temp(BE_woESS.ENV_V3,temp)
    exe2 = BE_woPV.ENV_V3.cust_temp(BE_woPV.ENV_V3,temp)
    import learning_model_PPO as PPO
    import learning_model_A2C as A2C
    import learning_model_DQN as DQN


    import rule_based_model as Rule
    exe3 = Rule.Rule_based(temp)
    # print('Rule',exe3)
    import learning_model_PPO_woESS as PPO_woESS
    import learning_model_PPO_woPV as PPO_woPV  
 
    # case number
    if case == '1':
        C = {'algo':['PPO','A2C','DQN'], 'cost':[PPO.TOTAL_COST[0],A2C.TOTAL_COST[0],DQN.TOTAL_COST[0]]}
        print(C)
        dC = pd.DataFrame(C)
        pos = dC['cost'].idxmin()
        algo = dC['algo'][pos]
        if pos == 0:
            dataset = {'ESS':PPO.SOC, 'DG': PPO.PDG, 'EV': PPO.EV, 'HVAC': PPO.HVAC}
        elif pos == 1:
            dataset = {'ESS':A2C.SOC, 'DG': A2C.PDG, 'EV': A2C.EV, 'HVAC': A2C.HVAC}
        elif pos == 2:
            dataset = {'ESS':DQN.SOC, 'DG': DQN.PDG, 'EV': DQN.EV, 'HVAC': DQN.HVAC}

    if case == '2':
        dataset = {'ESS':PPO_woESS.SOC, 'DG': PPO_woESS.PDG, 'EV': PPO_woESS.EV, 'HVAC': PPO_woESS.HVAC}

    if case == '3': 
        dataset = {'ESS':PPO_woPV.SOC, 'DG': PPO_woPV.PDG, 'EV': PPO_woPV.EV, 'HVAC': PPO_woPV.HVAC}
        

    df = pd.DataFrame(dataset)
    df.to_csv('Return_Actions.csv')

    # dataset2 = {'csE':csE, 'csG': csG, 'ClH': ClH, 'ClP': ClP, 'ClE':ClE}
    # df2 = pd.DataFrame(dataset2)
    # df2.to_csv('Return_Obj.csv')

    pw = plotWindow()

    x = np.arange(len(PPO.REWARD))

    # framework: 2
    # fig1 = plt.figure(figsize=(25,10))
   
    # plot11= fig1.add_subplot(121)
    # img1 = mpimg.imread("Fig1_.png")
    # plot11.imshow(img1)
    # plot11.set_title("The Structure of a Commercial Microgrid",fontweight="bold", fontsize=18)
    # plot11.axis('off')     

    # plot12 = fig1.add_subplot(122)
    # img2 = mpimg.imread("Fig2_.png")
    # plot12.imshow(img2)
    # plot12.set_title('The Framework of Algorithm',fontweight="bold", fontsize=18)
    # plot12.axis('off')
    # pw.addPlot("System Configuration", fig1, None)  

    # input (baseload, PV): 2
    fig2 = plt.figure()
    plot21 = fig2.add_subplot(131)
    for i in range(0,D.shape[1]):
        plot21.plot(np.arange(D.shape[0]),D[:,i])
    plot21.set_xlabel('time slot (unit: 15 min)', fontsize=14)
    plot21.set_ylabel('Base load demand (kw)', fontsize=14) 
    plot21.set_title('Base Load Demand',fontweight="bold", fontsize=18)
    

    plot22 = fig2.add_subplot(132)
    for i in range(0,w.shape[1]):
        plot22.plot(np.arange(w.shape[0]),w[:,i])
    plot22.set_xlabel('time slot (unit: 15 min)', fontsize=14)
    plot22.set_ylabel('PV output (kw)', fontsize=14) 
    plot22.set_title('PV Power Output',fontweight="bold", fontsize=18)

    plot23 = fig2.add_subplot(133)
    for i in range(0,pi.shape[1]):
        plot23.plot(np.arange(pi.shape[0]),pi[:,i])
    plot23.set_xlabel('time slot (unit: 15 min)',fontsize=14)
    plot23.set_ylabel('Price ($/kWh)', fontsize=14) 
    plot23.set_title('Electricity Price',fontweight="bold", fontsize=18)
    pw.addPlot("Load Demand and Renewable Energy Output", fig2, 'The figure of base load demand shows the base load demand required by the whole commercial building.\
        \n\nThe figure of PV power output shows the power output generated by PV.\
        \n\nThe figure of electricity price shows the time-varying electricity price of the main grid.\
        \n\n30 scenerios are considered in all figures.')
    # pw.addPlot("Optimal Costs and Comfort Levels", fig4, 'The results were saved as Return_Obj.csv \n\n Total daily cost ($): '+print_cost)

    # Training process 
    # case number
    if case == '1':      
        fig3 = plt.figure()
        plot31 = fig3.add_subplot(121)
        img4 = mpimg.imread("Fig4_.png")
        plot31.imshow(img4)
        plot31.set_aspect(0.9)
        plot31.set_title('Machine Learning Training Process',fontweight="bold", fontsize=18)
        plot31.axis('off')

        plot32 = fig3.add_subplot(122)
        # creating the dataset
        Rule_Cost = exe3[4]
        data_cost = {'PPO':PPO.TOTAL_COST[0]/1000, 'A2C':A2C.TOTAL_COST[0]/1000, 'DQN':DQN.TOTAL_COST[0]/1000, 'Rule-based':Rule_Cost/1000}
        print('data',data_cost)
        algos = list(data_cost.keys())
        values = list(data_cost.values())  
        # creating the bar plot
        plot32.bar(algos, values, width = 0.4) 
        plot32.set_xlabel("Algorithm", fontsize=14)
        plot32.set_ylabel("Cost ($1000)",fontsize=14)
        plot32.set_title("Performance Evaluation: Operating Cost",fontweight="bold", fontsize=18)
        plot32.set_ylim(2.3,3.6)
        pw.addPlot("Algorithm Exploration: Training Process and Operation Cost", fig3, 'PPO, A2C and DQN refers to Proximal Policy Optimization,  Advantage Actor Critic and Deep Q-Network, respectively.\
        \n\nThe rule-based algorithm works as a benchmark, following naive rules to optimize the operation of the commercial building.\
        \n\nWe compare algorithm convergence and optimization results (cost minimization) on this page.')


        # output (actions): 4
        fig4 = plt.figure()
        # ESS, DG, EV, HVAC
        plot1 = fig4.add_subplot(221)
        plot2 = fig4.add_subplot(222)
        plot3 = fig4.add_subplot(223)
        plot4 = fig4.add_subplot(224)
        plot1.plot(np.arange(len(PPO.SOC)),PPO.SOC)
        plot1.set_xlabel('time slot (unit: 15 min)', fontsize=14)
        plot1.set_ylabel('ESS SOC', fontsize=14)

        PPO.PDG = [x / 100 for x in PPO.PDG]
        PPO.EV = [x / 5 for x in PPO.EV]
        PPO.HVAC = [x / 5 for x in PPO.HVAC]
        

        plot2.plot(np.arange(len(PPO.PDG)),PPO.PDG)
        plot2.set_xlabel('time slot (unit: 15 min)', fontsize=14)
        plot2.set_ylabel('DG Power \nOutput (pu)', fontsize=14)

        plot3.plot(np.arange(len(PPO.EV)),PPO.EV)
        plot3.set_xlabel('time slot (unit: 15 min)', fontsize=14)
        plot3.set_ylabel('EV Charging \nConsumption (pu)', fontsize=14)

        plot4.plot(np.arange(len(PPO.HVAC)),PPO.HVAC)
        plot4.set_xlabel('time slot (unit: 15 min)', fontsize=14)
        plot4.set_ylabel('HVAC Power \nConsumption (pu)',fontsize=14)
        fig4.suptitle('Optimal Scheduling: ESS, DG, EV, HVAC',fontweight="bold", fontsize=18)
        # pw.addPlot("Optimal Schedule", fig4, 'The results were saved as Return_Actions.csv')
        pw.addPlot("Optimal Schedule", fig4, 'The results were saved as Return_Actions.csv.\
        \nThe above optimal scheduling is for Case 1 using Proximal Policy Optimization.\
        \nThe base value for DG power output, EV charging consumption and HVAC power consumption is 100kW, 5kW, 5kW, respectively.')


    elif case == '2':      
        fig3 = plt.figure()
        plot31 = fig3.add_subplot(121)
        img4 = mpimg.imread("Fig4_2.png")
        plot31.imshow(img4)
        plot31.set_title('Machine Learning Training Process',fontweight="bold", fontsize=18)
        plot31.axis('off')

        plot32 = fig3.add_subplot(122)
        # creating the dataset
        data_cost = {'PPO':PPO_woESS.TOTAL_COST[0]/1000}
        algos = list(data_cost.keys())
        values = list(data_cost.values())  
        # creating the bar plot
        plot32.bar(algos, values, width = 0.4) 
        plot32.set_xlabel("Algorithm", fontsize=14)
        plot32.set_ylabel("Cost ($1000)",fontsize=14)
        plot32.set_ylim(2.3,3.6)
        plot32.set_title("Performance Evaluation: Operating Cost",fontweight="bold", fontsize=18)
        pw.addPlot("Algorithm Exploration: Training Process and Operation Cost", fig3, 'We compare algorithm convergence for different demo cases.\
        \n\nPPO refers to Proximal Policy Optimization.\
        \n\nWe show the cost minimization by PPO on this page.')

        # output (actions): 4
        fig4 = plt.figure()
        # ESS, DG, EV, HVAC
        plot1 = fig4.add_subplot(221)
        plot2 = fig4.add_subplot(222)
        plot3 = fig4.add_subplot(223)
        plot4 = fig4.add_subplot(224)
        plot1.plot(np.arange(len(PPO_woESS.SOC)),PPO_woESS.SOC)
        plot1.set_xlabel('time slot (unit: 15 min)', fontsize=14)
        plot1.set_ylabel('ESS SOC', fontsize=14)

        PPO_woESS.PDG = [x / 100 for x in PPO_woESS.PDG]
        PPO_woESS.EV = [x / 5 for x in PPO_woESS.EV]
        PPO_woESS.HVAC = [x / 5 for x in PPO_woESS.HVAC]

        plot2.plot(np.arange(len(PPO_woESS.PDG)),PPO_woESS.PDG)
        plot2.set_xlabel('time slot (unit: 15 min)', fontsize=14)
        plot2.set_ylabel('DG Power \nOutput (kW)', fontsize=14)

        plot3.plot(np.arange(len(PPO_woESS.EV)),PPO_woESS.EV)
        plot3.set_xlabel('time slot (unit: 15 min)', fontsize=14)
        plot3.set_ylabel('EV Charging \nConsumption (kW)', fontsize=14)

        plot4.plot(np.arange(len(PPO_woESS.HVAC)),PPO_woESS.HVAC)
        plot4.set_xlabel('time slot (unit: 15 min)', fontsize=14)
        plot4.set_ylabel('HVAC Power \nConsumption (kW)',fontsize=14)
        fig4.suptitle('Optimal Scheduling: ESS, DG, EV, HVAC',fontweight="bold", fontsize=18)
        # pw.addPlot("Optimal Schedule", fig4, 'The results were saved as Return_Actions.csv')
        pw.addPlot("Optimal Schedule", fig4, 'The results were saved as Return_Actions.csv.\
        \nThe above optimal scheduling is for Case 2 using Proximal Policy Optimization.\
        \nThe base value for DG power output, EV charging consumption and HVAC power consumption is 100kW, 5kW, 5kW, respectively.')

    elif case == '3':      
        fig3 = plt.figure()
        plot31 = fig3.add_subplot(121)
        img4 = mpimg.imread("Fig4_2.png")
        plot31.imshow(img4)
        plot31.set_title('Machine Learning Training Process',fontweight="bold", fontsize=18)
        plot31.axis('off')

        plot32 = fig3.add_subplot(122)
        # creating the dataset
        data_cost = {'PPO':PPO_woPV.TOTAL_COST[0]/1000}
        algos = list(data_cost.keys())
        values = list(data_cost.values())  
        # creating the bar plot
        plot32.bar(algos, values, width = 0.4) 
        plot32.set_xlabel("Algorithm", fontsize=14)
        plot32.set_ylabel("Cost (1000$)",fontsize=14)
        plot32.set_ylim(2.3,4)
        plot32.set_title("Performance Evaluation: Operating Cost",fontweight="bold", fontsize=18)
        pw.addPlot("Algorithm Exploration: Training Process and Operation Cost", fig3, 'We compare algorithm convergence for different demo cases.\
        \n\nPPO refers to Proximal Policy Optimization.\
        \n\nWe show the cost minimization by PPO on this page.')

        # output (actions): 4
        fig4 = plt.figure()
        # ESS, DG, EV, HVAC
        plot1 = fig4.add_subplot(221)
        plot2 = fig4.add_subplot(222)
        plot3 = fig4.add_subplot(223)
        plot4 = fig4.add_subplot(224)
        plot1.plot(np.arange(len(PPO_woPV.SOC)),PPO_woPV.SOC)
        plot1.set_xlabel('time slot (unit: 15 min)', fontsize=14)
        plot1.set_ylabel('ESS SOC', fontsize=14)

        PPO_woPV.PDG = [x / 100 for x in PPO_woPV.PDG]
        PPO_woPV.EV = [x / 5 for x in PPO_woPV.EV]
        PPO_woPV.HVAC = [x / 5 for x in PPO_woPV.HVAC]

        plot2.plot(np.arange(len(PPO_woPV.PDG)),PPO_woPV.PDG)
        plot2.set_xlabel('time slot (unit: 15 min)', fontsize=14)
        plot2.set_ylabel('DG Power \nOutput (kW)', fontsize=14)

        plot3.plot(np.arange(len(PPO_woPV.EV)),PPO_woPV.EV)
        plot3.set_xlabel('time slot (unit: 15 min)', fontsize=14)
        plot3.set_ylabel('EV Charging \nConsumption (kW)', fontsize=14)

        plot4.plot(np.arange(len(PPO_woPV.HVAC)),PPO_woPV.HVAC)
        plot4.set_xlabel('time slot (unit: 15 min)', fontsize=14)
        plot4.set_ylabel('HVAC Power \nConsumption (kW)',fontsize=14)
        fig4.suptitle('Optimal Scheduling: ESS, DG, EV, HVAC',fontweight="bold", fontsize=18)
        # pw.addPlot("Optimal Schedule", fig4, 'The results were saved as Return_Actions.csv')
        pw.addPlot("Optimal Schedule", fig4, 'The results were saved as Return_Actions.csv.\
        \nThe above optimal scheduling is for Case 3 using Proximal Policy Optimization.\
        \nThe base value for DG power output, EV charging consumption and HVAC power consumption is 100kW, 5kW, 5kW, respectively.')

    # compare different cases
    
    fig5 = plt.figure()
    plot51 = fig5.add_subplot(111)
    # creating the dataset
    data_cost = {'Case 1 \nPPO':PPO.TOTAL_COST[0]/1000, 'Case 2 \nPPO':PPO_woESS.TOTAL_COST[0]/1000, 'Case 3 \nPPO':PPO_woPV.TOTAL_COST[0]/1000}
    print('Multiple cases', data_cost)
    algos = list(data_cost.keys())
    values = list(data_cost.values())  
    # creating the bar plot
    plot51.bar(algos, values, width = 0.4) 
    plot51.set_xlabel("Tested Cases", fontsize=14)
    plot51.set_ylabel("Cost (1000$)",fontsize=14)
    plot51.set_ylim(2.3,3.6)
    plot51.set_title("The Comparison of Cost",fontweight="bold", fontsize=18)
    pw.addPlot("Multiple Cases Comparison", fig5, 'The comparison of different demo cases is shown on this page.\
        \n\nCase 1: Both Energy Storage System (ESS) and PV are available. -- Proximal Policy Optimization\
        \n\nCase 2: Energy Storage System (ESS) is not available, and PV is available. -- Proximal Policy Optimization\
        \n\nCase 3: Energy Storage System (ESS) is available, and PV is not available. -- Proximal Policy Optimization')

    pw.show()

    sys.exit(app.exec_())
