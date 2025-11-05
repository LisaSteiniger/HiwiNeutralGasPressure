import w7xarchive
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.signal import find_peaks
urlAEA21 = {'IC': "ArchiveDB/codac/W7X/ControlStation.2071/FPGA.1_DATASTREAM/1/IonCurrent-A/scaled",
            'EC': "ArchiveDB/codac/W7X/ControlStation.2071/FPGA.1_DATASTREAM/0/ElectronCurrent-A/scaled",
            'HC': "ArchiveDB/codac/W7X/ControlStation.2071/ADC.1_DATASTREAM/0/Output Current A/scaled",
            'HV': "ArchiveDB/codac/W7X/ControlStation.2071/ADC.1_DATASTREAM/1/Output Voltage A/scaled",
            'ECRH': "Test/raw/W7X/CBG_ECRH/TotalPower_DATASTREAM/V1/0/Ptot_ECRH",
            'ne' : "ArchiveDB/views/KKS/QMJ_Interferometer/Processed/Density"}

urlAEE11 = {'IC': "ArchiveDB/codac/W7X/ControlStation.2097/FPGA.1_DATASTREAM/1/IonCurrent-A/scaled",
            'EC': "ArchiveDB/codac/W7X/ControlStation.2097/FPGA.1_DATASTREAM/0/ElectronCurrent-A/scaled",
            'HC': "ArchiveDB/codac/W7X/ControlStation.2097/ADC.1_DATASTREAM/0/Output Current A/scaled",
            'HV': "ArchiveDB/codac/W7X/ControlStation.2097/ADC.1_DATASTREAM/1/Output Voltage A/scaled",
            'ECRH': "Test/raw/W7X/CBG_ECRH/TotalPower_DATASTREAM/V1/0/Ptot_ECRH",
            'ne' : "ArchiveDB/views/KKS/QMJ_Interferometer/Processed/Density"}

urlAEE30 = {'IC': "ArchiveDB/codac/W7X/ControlStation.2071/FPGA.1_DATASTREAM/3/IonCurrent-B/scaled",
            'EC': "ArchiveDB/codac/W7X/ControlStation.2071/FPGA.1_DATASTREAM/2/ElectronCurrent-B/scaled",
            'HC': "ArchiveDB/codac/W7X/ControlStation.2071/ADC.1_DATASTREAM/2/Output Current B/scaled",
            'HV': "ArchiveDB/codac/W7X/ControlStation.2071/ADC.1_DATASTREAM/3/Output Voltage B/scaled",
            'ECRH': "Test/raw/W7X/CBG_ECRH/TotalPower_DATASTREAM/V1/0/Ptot_ECRH",
            'ne' : "ArchiveDB/views/KKS/QMJ_Interferometer/Processed/Density"}

urlAEE41 = {'IC': "ArchiveDB/codac/W7X/ControlStation.2098/FPGA.1_DATASTREAM/1/IonCurrent-A/scaled",
            'EC': "ArchiveDB/codac/W7X/ControlStation.2098/FPGA.1_DATASTREAM/0/ElectronCurrent-A/scaled",
            'HC': "ArchiveDB/codac/W7X/ControlStation.2098/ADC.1_DATASTREAM/0/Output Current A/scaled",
            'HV': "ArchiveDB/codac/W7X/ControlStation.2098/ADC.1_DATASTREAM/1/Output Voltage A/scaled",
            'ECRH': "Test/raw/W7X/CBG_ECRH/TotalPower_DATASTREAM/V1/0/Ptot_ECRH",
            'ne' : "ArchiveDB/views/KKS/QMJ_Interferometer/Processed/Density"}

urlAEE50 = {'IC': "ArchiveDB/codac/W7X/ControlStation.2099/FPGA.1_DATASTREAM/1/IonCurrent-A/scaled",
            'EC': "ArchiveDB/codac/W7X/ControlStation.2099/FPGA.1_DATASTREAM/0/ElectronCurrent-A/scaled",
            'HC': "ArchiveDB/codac/W7X/ControlStation.2099/ADC.1_DATASTREAM/0/Output Current A/scaled",
            'HV': "ArchiveDB/codac/W7X/ControlStation.2099/ADC.1_DATASTREAM/1/Output Voltage A/scaled",
            'ECRH': "Test/raw/W7X/CBG_ECRH/TotalPower_DATASTREAM/V1/0/Ptot_ECRH",
            'ne' : "ArchiveDB/views/KKS/QMJ_Interferometer/Processed/Density"}

urlAEH11 = {'IC': "ArchiveDB/codac/W7X/ControlStation.2100/FPGA.1_DATASTREAM/1/IonCurrent-A/scaled",
            'EC': "ArchiveDB/codac/W7X/ControlStation.2100/FPGA.1_DATASTREAM/0/ElectronCurrent-A/scaled",
            'HC': "ArchiveDB/codac/W7X/ControlStation.2100/ADC.1_DATASTREAM/0/Output Current A/scaled",
            'HV': "ArchiveDB/codac/W7X/ControlStation.2100/ADC.1_DATASTREAM/1/Output Voltage A/scaled",
            'ECRH': "Test/raw/W7X/CBG_ECRH/TotalPower_DATASTREAM/V1/0/Ptot_ECRH",
            'ne' : "ArchiveDB/views/KKS/QMJ_Interferometer/Processed/Density"}

urlAEH21 = {'IC': "ArchiveDB/codac/W7X/ControlStation.2100/FPGA.1_DATASTREAM/3/IonCurrent-B/scaled",
            'EC': "ArchiveDB/codac/W7X/ControlStation.2100/FPGA.1_DATASTREAM/2/ElectronCurrent-B/scaled",
            'HC': "ArchiveDB/codac/W7X/ControlStation.2100/ADC.1_DATASTREAM/2/Output Current B/scaled",
            'HV': "ArchiveDB/codac/W7X/ControlStation.2100/ADC.1_DATASTREAM/3/Output Voltage B/scaled",
            'ECRH': "Test/raw/W7X/CBG_ECRH/TotalPower_DATASTREAM/V1/0/Ptot_ECRH",
            'ne' : "ArchiveDB/views/KKS/QMJ_Interferometer/Processed/Density"}

urlAEH30 = {'IC': "ArchiveDB/codac/W7X/ControlStation.2071/FPGA.1_DATASTREAM/5/IonCurrent-C/scaled",
            'EC': "ArchiveDB/codac/W7X/ControlStation.2071/FPGA.1_DATASTREAM/4/ElectronCurrent-C/scaled",
            'HC': "ArchiveDB/codac/W7X/ControlStation.2071/ADC.1_DATASTREAM/4/Output Current C/scaled",
            'HV': "ArchiveDB/codac/W7X/ControlStation.2071/ADC.1_DATASTREAM/5/Output Voltage C/scaled",
            'ECRH': "Test/raw/W7X/CBG_ECRH/TotalPower_DATASTREAM/V1/0/Ptot_ECRH",
            'ne' : "ArchiveDB/views/KKS/QMJ_Interferometer/Processed/Density"}

urlAEH31 = {'IC': "ArchiveDB/codac/W7X/ControlStation.2100/FPGA.1_DATASTREAM/5/IonCurrent-C/scaled",
            'EC': "ArchiveDB/codac/W7X/ControlStation.2100/FPGA.1_DATASTREAM/4/ElectronCurrent-C/scaled",
            'HC': "ArchiveDB/codac/W7X/ControlStation.2100/ADC.1_DATASTREAM/4/Output Current C/scaled",
            'HV': "ArchiveDB/codac/W7X/ControlStation.2100/ADC.1_DATASTREAM/5/Output Voltage C/scaled",
            'ECRH': "Test/raw/W7X/CBG_ECRH/TotalPower_DATASTREAM/V1/0/Ptot_ECRH",
            'ne' : "ArchiveDB/views/KKS/QMJ_Interferometer/Processed/Density"}

urlAEH50 = {'IC': "ArchiveDB/codac/W7X/ControlStation.2099/FPGA.1_DATASTREAM/3/IonCurrent-B/scaled",
            'EC': "ArchiveDB/codac/W7X/ControlStation.2099/FPGA.1_DATASTREAM/2/ElectronCurrent-B/scaled",
            'HC': "ArchiveDB/codac/W7X/ControlStation.2099/ADC.1_DATASTREAM/2/Output Current B/scaled",
            'HV': "ArchiveDB/codac/W7X/ControlStation.2099/ADC.1_DATASTREAM/3/Output Voltage B/scaled",
            'ECRH': "Test/raw/W7X/CBG_ECRH/TotalPower_DATASTREAM/V1/0/Ptot_ECRH",
            'ne' : "ArchiveDB/views/KKS/QMJ_Interferometer/Processed/Density"}

urlAEH51 = {'IC': "ArchiveDB/codac/W7X/ControlStation.2101/FPGA.1_DATASTREAM/1/IonCurrent-A/scaled",
            'EC': "ArchiveDB/codac/W7X/ControlStation.2101/FPGA.1_DATASTREAM/0/ElectronCurrent-A/scaled",
            'HC': "ArchiveDB/codac/W7X/ControlStation.2101/ADC.1_DATASTREAM/0/Output Current A/scaled",
            'HV': "ArchiveDB/codac/W7X/ControlStation.2101/ADC.1_DATASTREAM/1/Output Voltage A/scaled",
            'ECRH': "Test/raw/W7X/CBG_ECRH/TotalPower_DATASTREAM/V1/0/Ptot_ECRH",
            'ne' : "ArchiveDB/views/KKS/QMJ_Interferometer/Processed/Density"}

urlAEI30 = {'IC': "ArchiveDB/codac/W7X/ControlStation.2101/FPGA.1_DATASTREAM/3/IonCurrent-B/scaled",
            'EC': "ArchiveDB/codac/W7X/ControlStation.2101/FPGA.1_DATASTREAM/2/ElectronCurrent-B/scaled",
            'HC': "ArchiveDB/codac/W7X/ControlStation.2101/ADC.1_DATASTREAM/2/Output Current B/scaled",
            'HV': "ArchiveDB/codac/W7X/ControlStation.2101/ADC.1_DATASTREAM/3/Output Voltage B/scaled",
            'ECRH': "Test/raw/W7X/CBG_ECRH/TotalPower_DATASTREAM/V1/0/Ptot_ECRH",
            'ne' : "ArchiveDB/views/KKS/QMJ_Interferometer/Processed/Density"}

urlAEI50 = {'IC': "ArchiveDB/codac/W7X/ControlStation.2101/FPGA.1_DATASTREAM/5/IonCurrent-C/scaled",
            'EC': "ArchiveDB/codac/W7X/ControlStation.2101/FPGA.1_DATASTREAM/4/ElectronCurrent-C/scaled",
            'HC': "ArchiveDB/codac/W7X/ControlStation.2101/ADC.1_DATASTREAM/4/Output Current C/scaled",
            'HV': "ArchiveDB/codac/W7X/ControlStation.2101/ADC.1_DATASTREAM/5/Output Voltage C/scaled",
            'ECRH': "Test/raw/W7X/CBG_ECRH/TotalPower_DATASTREAM/V1/0/Ptot_ECRH",
            'ne' : "ArchiveDB/views/KKS/QMJ_Interferometer/Processed/Density"}

urlAEI51 = {'IC': "ArchiveDB/codac/W7X/ControlStation.2101/FPGA.1_DATASTREAM/7/IonCurrent-D/scaled",
            'EC': "ArchiveDB/codac/W7X/ControlStation.2101/FPGA.1_DATASTREAM/6/ElectronCurrent-D/scaled",
            'HC': "ArchiveDB/codac/W7X/ControlStation.2101/ADC.1_DATASTREAM/6/Output Current D/scaled",
            'HV': "ArchiveDB/codac/W7X/ControlStation.2101/ADC.1_DATASTREAM/7/Output Voltage D/scaled",
            'ECRH': "Test/raw/W7X/CBG_ECRH/TotalPower_DATASTREAM/V1/0/Ptot_ECRH",
            'ne' : "ArchiveDB/views/KKS/QMJ_Interferometer/Processed/Density"}

urlAEL10 = {'IC': "ArchiveDB/codac/W7X/ControlStation.2100/FPGA.1_DATASTREAM/7/IonCurrent-D/scaled",
            'EC': "ArchiveDB/codac/W7X/ControlStation.2100/FPGA.1_DATASTREAM/6/ElectronCurrent-D/scaled",
            'HC': "ArchiveDB/codac/W7X/ControlStation.2100/ADC.1_DATASTREAM/6/Output Current D/scaled",
            'HV': "ArchiveDB/codac/W7X/ControlStation.2100/ADC.1_DATASTREAM/7/Output Voltage D/scaled",
            'ECRH': "Test/raw/W7X/CBG_ECRH/TotalPower_DATASTREAM/V1/0/Ptot_ECRH",
            'ne' : "ArchiveDB/views/KKS/QMJ_Interferometer/Processed/Density"}

urlAEP30 = {'IC': "ArchiveDB/codac/W7X/ControlStation.2071/FPGA.1_DATASTREAM/7/IonCurrent-D/scaled",
            'EC': "ArchiveDB/codac/W7X/ControlStation.2071/FPGA.1_DATASTREAM/6/ElectronCurrent-D/scaled",
            'HC': "ArchiveDB/codac/W7X/ControlStation.2071/ADC.1_DATASTREAM/6/Output Current D/scaled",
            'HV': "ArchiveDB/codac/W7X/ControlStation.2071/ADC.1_DATASTREAM/7/Output Voltage D/scaled",
            'ECRH': "Test/raw/W7X/CBG_ECRH/TotalPower_DATASTREAM/V1/0/Ptot_ECRH",
            'ne' : "ArchiveDB/views/KKS/QMJ_Interferometer/Processed/Density"}

urlAEP50 = {'IC': "ArchiveDB/codac/W7X/ControlStation.2099/FPGA.1_DATASTREAM/7/IonCurrent-D/scaled",
            'EC': "ArchiveDB/codac/W7X/ControlStation.2099/FPGA.1_DATASTREAM/6/ElectronCurrent-D/scaled",
            'HC': "ArchiveDB/codac/W7X/ControlStation.2099/ADC.1_DATASTREAM/6/Output Current D/scaled",
            'HV': "ArchiveDB/codac/W7X/ControlStation.2099/ADC.1_DATASTREAM/7/Output Voltage D/scaled",
            'ECRH': "Test/raw/W7X/CBG_ECRH/TotalPower_DATASTREAM/V1/0/Ptot_ECRH",
            'ne' : "ArchiveDB/views/KKS/QMJ_Interferometer/Processed/Density"}

urlAEP51 = {'IC': "ArchiveDB/codac/W7X/ControlStation.2099/FPGA.1_DATASTREAM/5/IonCurrent-C/scaled",
            'EC': "ArchiveDB/codac/W7X/ControlStation.2099/FPGA.1_DATASTREAM/4/ElectronCurrent-C/scaled",
            'HC': "ArchiveDB/codac/W7X/ControlStation.2099/ADC.1_DATASTREAM/4/Output Current C/scaled",
            'HV': "ArchiveDB/codac/W7X/ControlStation.2099/ADC.1_DATASTREAM/5/Output Voltage C/scaled",
            'ECRH': "Test/raw/W7X/CBG_ECRH/TotalPower_DATASTREAM/V1/0/Ptot_ECRH",
            'ne' : "ArchiveDB/views/KKS/QMJ_Interferometer/Processed/Density"}

urls = [urlAEA21, urlAEE11, urlAEE30, urlAEE41, urlAEE50, urlAEH11, urlAEH21, urlAEH30, urlAEH31, urlAEH50, urlAEH51, urlAEI30, urlAEI50, urlAEI51, urlAEL10, urlAEP30, urlAEP50, urlAEP51]
manometers = ['AEA21', 'AEE11', 'AEE30', 'AEE41', 'AEE50', 'AEH11', 'AEH21' ,'AEH30', 'AEH31', 'AEH50', 'AEH51', 'AEI30', 'AEI50', 'AEI51', 'AEL10', 'AEP30', 'AEP50', 'AEP51']
manometers = ['AEH30']
#refernece discharges
dischargeIDs = ['20240918.5', '20241001.11', '20241008.40', '20241009.9', '20241016.14', '20241023.10', '20241023.11', '20241105.10', '20241106.6', '20241112.11', '20241113.18', '20241114.10', '20241120.8', '20241127.10', '20241203.7', '20241204.9', '20241205.9', '20241210.7', '20241212.9', 
                '20250311.62', '20250312.71', '20250325.65','20250326.11', '20250403.61', '20250423.32', '20250424.6', '20250506.9', '20250508.15', '20250513.6', '20250513.54', '20250514.10', '20250515.8', '20250521.9']

#times corresponding to ECRH step ends
times = [[2.94, 9.07, 15.05], [2.90, 9.04, 15.05], [3.06, 9.07, 15.02], [3.04, 9.04, 15.05], [3.04, 9.07, 15.07], [2.94, 9.07, 15.07], [3.04, 9.07, 15.03], [3.04, 9.07, 15.03], [3.06, 9.07, 15.07], [3.03, 9.03, 13.94], [3.02, 9.02, 15.07], [2.99, 9.05, 15.05], [2.99, 9.04, 15.02], [3.02, 9.05, 15.05], [3.04, 9.04, 15.05], [2.99, 9.04, 15.07], [2.99, 9.04, 15.07], [3.02, 9.07, 15.05], [3.04, 9.07, 15.10], 
         [2.99, 9.04, 15.07], [3.06, 9.02, 15.03], [3.04, 9.07, 15.05], [3.04, 9.05, 15.07], [3.06, 9.07, 15.10], [2.99, 9.05, 15.05], [2.97, 9.07, 15.05], [2.99, 9.05, 15.03], [3.02, 9.04, 15.07], [2.99, 9.04, 15.07], [2.99, 9.07, 15.10], [3.04, 9.04, 15.07], [2.99, 9.07, 15.05], [2.99, 9.02, 15.03]]

overviewTable = pd.DataFrame({})

for manometer, url in zip(manometers, [urlAEH30]):
    EC_av, HC_av, HV_av, IC_av1, ECRH_av1, ne_av1, IC_av2, ECRH_av2, ne_av2, IC_av3, ECRH_av3, ne_av3, OP = [], [], [], [], [], [], [], [], [], [], [], [], []

    for dischargeID, time in zip(dischargeIDs, times):
        t1, t2, t3 = time
        t1 -= 0.1
        t2 -= 0.1
        t3 -= 0.1
        
        #data is dictionary with same keys as url, each data[key] is a tuple of two lists containing timestemps (index 0) and data (index 1)
        data = w7xarchive.get_signal_for_program(url, dischargeID) 

        #index of data value 2s before ECRH starts
        index0_IC = list(data['IC'][0]).index((min(data['IC'][0], key=lambda x: abs(x+2))))
        index0_ne = list(data['ne'][0]).index((min(data['ne'][0], key=lambda x: abs(x+2))))

        data_IC = np.array(data['IC'][1]) * 1e6 #conversion to µA for plotting
        data_EC = np.array(data['EC'][1]) * 1e6 #conversion to µA for plotting
        data_HC = np.array(data['HC'][1]) 
        data_HV = np.array(data['HV'][1]) 
        data_ECRH = np.array(data['ECRH'][1]) 
        data_ne = np.array(data['ne'][1]) 

        #peaks, _ = find_peaks(data_IC[index0_IC:], height=[0.05, 0.1])
        #plt.plot(data['IC'][0][index0_IC:], data_IC[index0_IC:])
        #plt.plot(data['IC'][0][index0_IC:][peaks], data_IC[index0_IC:][peaks], 'o')
        #plt.show()
        '''
        fig, ax = plt.subplots(3, 2, layout='constrained', figsize=(10, 12))
        ax[0][0].plot(data['IC'][0][index0_IC:], data_IC[index0_IC:], label='ion current')
        ax[0][1].plot(data['EC'][0], data_EC, label='electron current')
        ax[1][0].plot(data['HC'][0], data_HC, label='heating current')
        ax[1][1].plot(data['HV'][0], data_HV, label='heating voltage')
        ax[2][0].plot(data['ECRH'][0], data_ECRH, label='ECRH heating power')
        ax[2][1].plot(data['ne'][0][index0_ne:], data_ne[index0_ne:], label='line-integrated electron density')

        ax[0][0].set_xlabel("time [s]")
        ax[0][1].set_xlabel("time [s]")
        ax[1][0].set_xlabel("time [s]")
        ax[1][1].set_xlabel("time [s]")

        ax[0][0].set_ylabel("ion current [µA]")
        ax[0][1].set_ylabel("electron current [µA]")
        ax[1][0].set_ylabel("heating current [A]")
        ax[1][1].set_ylabel("heating voltage [V]")
        ax[2][0].set_ylabel("ECRH heating power [kW]")
        ax[2][1].set_ylabel("line-integrated electron density [1/$m^{3}$]")

        ax[0][0].grid(True)
        ax[0][1].grid(True)
        ax[1][0].grid(True)
        ax[1][1].grid(True)
        ax[2][0].grid(True)
        ax[2][1].grid(True)

        safe = "plots/{dischargeID}{manometer}.png".format(dischargeID=dischargeID, manometer=manometer)
        fig.savefig(safe, bbox_inches='tight')
        fig.show()
        plt.close()
        '''

        #cut to real experimental time by finding ECRH start and stop value and matching data indices
        indexStart_EC = list(data['EC'][0]).index((min(data['EC'][0], key=lambda x: abs(x-data['ECRH'][0][0]))))
        indexStart_HC = list(data['HC'][0]).index((min(data['HC'][0], key=lambda x: abs(x-data['ECRH'][0][0]))))
        indexStart_HV = list(data['HV'][0]).index((min(data['HV'][0], key=lambda x: abs(x-data['ECRH'][0][0]))))
        indexStop_EC = list(data['EC'][0]).index((min(data['EC'][0], key=lambda x: abs(x-data['ECRH'][0][-1]))))
        indexStop_HC = list(data['HC'][0]).index((min(data['HC'][0], key=lambda x: abs(x-data['ECRH'][0][-1]))))
        indexStop_HV = list(data['HV'][0]).index((min(data['HV'][0], key=lambda x: abs(x-data['ECRH'][0][-1]))))
        
        EC_av.append(sum(data['EC'][1][indexStart_EC:indexStop_EC])/len(data['EC'][1][indexStart_EC:indexStop_EC]))
        HC_av.append(sum(data['HC'][1][indexStart_HC:indexStop_HC])/len(data['HC'][1][indexStart_HC:indexStop_HC]))
        HV_av.append(sum(data['HV'][1][indexStart_HV:indexStop_HV])/len(data['HV'][1][indexStart_HV:indexStop_HV]))

        #find value at each ECRH step by searching for value at a certain time
        index1_IC = list(data['IC'][0]).index((min(data['IC'][0], key=lambda x: abs(x-t1))))
        index2_IC = list(data['IC'][0]).index((min(data['IC'][0], key=lambda x: abs(x-t2))))
        index3_IC = list(data['IC'][0]).index((min(data['IC'][0], key=lambda x: abs(x-t3))))
        IC_av1.append(data['IC'][1][index1_IC])
        IC_av2.append(data['IC'][1][index2_IC])
        IC_av3.append(data['IC'][1][index3_IC])

        index1_ne = list(data['ne'][0]).index((min(data['ne'][0], key=lambda x: abs(x-t1))))
        index2_ne = list(data['ne'][0]).index((min(data['ne'][0], key=lambda x: abs(x-t2))))
        index3_ne = list(data['ne'][0]).index((min(data['ne'][0], key=lambda x: abs(x-t3))))
        ne_av1.append(data['ne'][1][index1_ne])
        ne_av2.append(data['ne'][1][index2_ne])
        ne_av3.append(data['ne'][1][index3_ne])

        index1_ECRH = list(data['ECRH'][0]).index((min(data['ECRH'][0], key=lambda x: abs(x-t1+0.5))))
        index2_ECRH = list(data['ECRH'][0]).index((min(data['ECRH'][0], key=lambda x: abs(x-t2+0.5))))
        index3_ECRH = list(data['ECRH'][0]).index((min(data['ECRH'][0], key=lambda x: abs(x-t3+0.5))))
        ECRH_av1.append(data['ECRH'][1][index1_ECRH])
        ECRH_av2.append(data['ECRH'][1][index2_ECRH])
        ECRH_av3.append(data['ECRH'][1][index3_ECRH])
        
        if manometer == manometers[0]:
            if float(dischargeID) < 20181019:
                OP.append('1.2b')
            elif float(dischargeID) < 20230331:
                OP.append('2.1')
            elif float(dischargeID) <20241213:
                OP.append('2.2')
            else:
                OP.append('2.3')
    
    if manometer == manometers[0]:
        overviewTable['discharge'] = dischargeIDs
        overviewTable['OP'] = OP            
        overviewTable['ne_av1'] = ne_av1
        overviewTable['ne_av2'] = ne_av2
        overviewTable['ne_av3'] = ne_av3
        overviewTable['ECRH_av1'] = ECRH_av1
        overviewTable['ECRH_av2'] = ECRH_av2
        overviewTable['ECRH_av3'] = ECRH_av3
        overviewTable['space'.format(manometer=manometer)] = [np.nan] * len(EC_av) #empty column for better readability

        
    overviewTable['EC_av_{manometer}'.format(manometer=manometer)] = EC_av
    overviewTable['HC_av_{manometer}'.format(manometer=manometer)] = HC_av
    overviewTable['HV_av_{manometer}'.format(manometer=manometer)] = HV_av
    overviewTable['IC_av1_{manometer}'.format(manometer=manometer)] = IC_av1
    overviewTable['IC_av2_{manometer}'.format(manometer=manometer)] = IC_av2
    overviewTable['IC_av3_{manometer}'.format(manometer=manometer)] = IC_av3
    overviewTable['space_{manometer}'.format(manometer=manometer)] = [np.nan] * len(EC_av)  #empty column for better readability
    
overviewTable.to_csv('overviewQRGdata.csv', sep=';')

def findReferenceDischarges(dischargeID, url, ne, ECRH):
    data = w7xarchive.get_signal_for_program(url, dischargeID) 
    filter_ne = np.array([j < 0.9 * ne and j > 1.1 * ne for j in data['ne'][1]])
    filter_ECRH = np.array([j < 0.9 * ECRH and j > 1.1 * ECRH for j in data['ECRH'][1]])
    times_ne = data['ne'][0][filter_ne]
    times_ECRH = data['ECRH'][0][filter_ECRH]

    dt_min, dt_index = [], []
    for time in times_ne:
        dt_min.append(min(times_ECRH, key=lambda x: abs(x-time)))
        dt_index.append(times_ECRH.index(dt_min[-1]))
    print(dt_min)


