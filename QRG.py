import w7xarchive
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib as mpl

from links import *

mpl.rcParams['agg.path.chunksize'] = 10000
#https://w7x-logbook.ipp-hgw.mpg.de/components?id=DCH#dataaccess

def overflow_correction(dat, fullrange = 5e-6, signed=True, thresh=0.9, nan_thresh=8.7499e-6):
    """
    Corrects overflow in the input data vector by adjusting the affected samples.
    Note: This function was performance optimized using ChatGPT3.5.

    :param dat (ndarray): The input data vector.
    :param fullrange (float): The full range where overflow is expected.
    :param signed (bool): Indicates if the data type is signed or unsigned.
    :param thresh (float): Maximum allowed variation between data points.
    :param nan_thresh (float): Threshold to consider a value as invalid and set it to NaN. Set to 0 to disable
    :return: ndarray: The corrected data vector with overflow adjusted.
    """

    # Create a copy of the input data to work with
    new_dat = np.copy(dat)

    # Array to track the cumulative overruns and underruns
    domain = np.zeros_like(dat)

    # Find the indices where overruns and underruns occur
    overrun_indices = np.where(dat[1:] - dat[:-1] < -2 * fullrange * thresh)[0]
    underrun_indices = np.where(dat[1:] - dat[:-1] > 2 * fullrange * thresh)[0]

    # Mark overruns with 1 and underruns with -1 in the domain array
    domain[overrun_indices + 1] = 1
    domain[underrun_indices + 1] = -1

    # Calculate the correction values based on the domain and full range
    correction = domain.cumsum() * (int(signed) + 1) * fullrange

    # Apply the corrections to the data vector, starting from the second element
    new_dat[1:] += correction[1:]

    # Identify values that exceed the nan_thresh and set them to NaN.
    #if nan_thresh:
    #    overflow_indices = np.where(new_dat >= nan_thresh)[0]
    #    new_dat[overflow_indices] = np.nan
    return new_dat

def getManometerDataRaw(manometers, urls, dischargeIDs, times):
    overviewTable = pd.DataFrame({})
    for manometer, url in zip(manometers, urls):
        EC_av, HC_av, HV_av, IC_av1, ECRH_av1, ne_av1, IC_av2, ECRH_av2, ne_av2, IC_av3, ECRH_av3, ne_av3, OP, fails = [], [], [], [], [], [], [], [], [], [], [], [], [], []
        data_save = []
        for dischargeID, time in zip(dischargeIDs, times):
            t1, t2, t3 = time
            t1 -= 0.05
            t2 -= 0.05
            t3 -= 0.05
            
            #data is dictionary with same keys as url, each data[key] is a tuple of two lists containing timestemps (index 0) and data (index 1)
            data = w7xarchive.get_signal_for_program(url, dischargeID) 

            #test for existance of all datastreams
            keys = data.keys()
            if 'IC' in keys and 'EC' in keys and 'HC' in keys and 'HV' in keys:
                pass
            else:
                print('not all datastreams available in {discharge} for {manometer}'.format(discharge=dischargeID, manometer=manometer))
                EC_av.append(np.nan)
                HC_av.append(np.nan)
                HV_av.append(np.nan)

                IC_av1.append(np.nan)
                IC_av2.append(np.nan)
                IC_av3.append(np.nan)

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
                continue

            #index of data value 2s before ECRH starts
            index0_IC = list(data['IC'][0]).index((min(data['IC'][0], key=lambda x: abs(x+2))))
            index0_ne = list(data['ne'][0]).index((min(data['ne'][0], key=lambda x: abs(x+2))))

            data_IC = np.array(data['IC'][1]) * 1e6 #conversion to µA for plotting
            data_EC = np.array(data['EC'][1]) * 1e6 #conversion to µA for plotting
            data_HC = np.array(data['HC'][1]) 
            data_HV = np.array(data['HV'][1]) 
            data_ECRH = np.array(data['ECRH'][1]) 
            data_ne = np.array(data['ne'][1]) 

            #index1_IC = list(data['IC'][0]).index((min(data['IC'][0], key=lambda x: abs(x-t1))))
            #index1_ICd = list(data_IC).index((min(data_IC, key=lambda x: abs(x-t1))))
            #index2_ICd = list(data_IC).index((min(data_IC, key=lambda x: abs(x-t2))))
            #index3_ICd = list(data_IC).index((min(data_IC, key=lambda x: abs(x-t3))))
            #index2_IC = list(data['IC'][0]).index((min(data['IC'][0], key=lambda x: abs(x-t2))))
            #index3_IC = list(data['IC'][0]).index((min(data['IC'][0], key=lambda x: abs(x-t3))))
            #plt.plot(range(len(data['IC'][1][index1_IC-50:index1_IC+50])), np.array(data['IC'][1][index1_IC-50:index1_IC+50])*1e6, 'bx')
            #plt.plot(range(len(data['IC'][1][index2_IC-50:index2_IC+50])), np.array(data['IC'][1][index2_IC-50:index2_IC+50])*1e6, 'mx')
            #plt.plot(range(len(data['IC'][1][index3_IC-50:index3_IC+50])),  np.array(data['IC'][1][index3_IC-50:index3_IC+50])*1e6, 'gx')
            #plt.plot(range(len(data_IC[index1_ICd-50:index1_ICd+50])), data_IC[index1_IC-50:index1_IC+50], 'b-')
            #plt.plot(range(len(data_IC[index2_ICd-50:index2_ICd+50])), data_IC[index2_IC-50:index2_IC+50], 'm-')
            #plt.plot(range(len(data_IC[index3_ICd-50:index3_ICd+50])), data_IC[index3_IC-50:index3_IC+50], 'g-')
            #plt.plot(data['IC'][0][index0_IC:], data_IC[index0_IC:])
            #plt.plot(data['IC'][0][index0_IC:], np.array(data['IC'][1][index0_IC:])*1e6)
            #plt.show()
            
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

            #cut to real experimental time by finding ECRH start and stop value and matching data indices
            #print((min(data['EC'][0], key=lambda x: abs(x-data['ECRH'][0][0]))), (min(data['EC'][0], key=lambda x: abs(x-data['ECRH'][0][-1]))), data['ECRH'][0][0], data['ECRH'][0][-1])
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
            #print((min(data['IC'][0], key=lambda x: abs(x-t1))))
            #print((min(data['IC'][0], key=lambda x: abs(x-t2))))
            #print((min(data['IC'][0], key=lambda x: abs(x-t3))))
            index1_IC = list(data['IC'][0]).index((min(data['IC'][0], key=lambda x: abs(x-t1))))
            index2_IC = list(data['IC'][0]).index((min(data['IC'][0], key=lambda x: abs(x-t2))))
            index3_IC = list(data['IC'][0]).index((min(data['IC'][0], key=lambda x: abs(x-t3))))
            #print(data['IC'][1][index3_IC-20:index3_IC+20])
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

            if EC_av[-1] < 210 * 1e-6 and EC_av[-1] > 190 * 1e-6:
                data_save.append([dischargeID, data['IC'][0][index0_IC:], data_IC[index0_IC:]])
            if EC_av[-1] < 50 * 1e-6:
                fails.append(0)
            else:
                fails.append(1)
        
        for discharge in data_save:
            plt.plot(discharge[1], discharge[2], label = discharge[0])
        plt.legend()
        plt.xlabel('time in [s]')
        plt.ylabel('ion current in [µA]')
        plt.show()

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
        overviewTable['fail_{manometer}'.format(manometer=manometer)] = fails
        overviewTable['space_{manometer}'.format(manometer=manometer)] = [np.nan] * len(EC_av)  #empty column for better readability
        
    overviewTable.to_csv('overviewQRGdata.csv', sep=';')

def findReferenceDischarges(dischargeID, url, ne, ECRH):
    data = w7xarchive.get_signal_for_program(url, dischargeID) 
    print(data)
    filter_ne = np.array([j > 0.9 * ne and j < 1.1 * ne for j in data['ne'][1]])
    filter_ECRH = np.array([j > 0.9 * ECRH and j < 1.1 * ECRH for j in data['ECRH'][1]])
    times_ne = data['ne'][0][filter_ne]
    times_ECRH = data['ECRH'][0][filter_ECRH]
    print(len(data['ne'][0]), len(times_ne))
    print(len(data['ECRH'][0]), len(times_ECRH))

    if len(times_ne) != 0 and len(times_ECRH) != 0:
        dt_min, dt_index, t = [], [], []
        for time in times_ne:
            dt_min.append(min(times_ECRH, key=lambda x: abs(x-time)))
            dt_index.append(list(times_ECRH).index(dt_min[-1]))
        print(dt_min)
        print(times_ne[dt_min.index(min(dt_min))])
    else: 
        print('no fitting times found')

def scatterPlotICfromX(overviewTable, X_name, manometer='AEP30'):
    overviewTableCombined = pd.DataFrame({})
    IC = [list(overviewTable['IC_av1_{manometer}'.format(manometer=manometer)])]
    IC.append(list(overviewTable['IC_av2_{manometer}'.format(manometer=manometer)]))
    IC.append(list(overviewTable['IC_av3_{manometer}'.format(manometer=manometer)]))
    overviewTableCombined['IC'] = np.hstack(np.array(IC))

    if X_name == 'ne':
        ne = [list(overviewTable['ne_av1'])]
        ne.append(list(overviewTable['ne_av2']))
        ne.append(list(overviewTable['ne_av3']))
        overviewTableCombined['X'] = np.hstack(np.array(ne))
        plt.xlabel('electron density in [$m^{-3}$]')
    
    elif X_name == 'ECRH':
        ECRH = [list(overviewTable['ECRH_av1'])]
        ECRH.append(list(overviewTable['ECRH_av2']))
        ECRH.append(list(overviewTable['ECRH_av3']))
        overviewTableCombined['X'] = np.hstack(np.array(ECRH))
        plt.xlabel('ECRH heating power in [kW]')

    OP = overviewTable['OP']*3
    overviewTableCombined['OP'] = np.hstack(np.array(OP))

    plt.scatter(overviewTableCombined['X'], overviewTableCombined['IC'], c=np.array(overviewTableCombined['OP']))
    plt.ylabel('ion current in [µA]')
    plt.show()

def scatterPlotICfromX3D(overviewTable, manometer='AEP30'):
    overviewTableCombined = pd.DataFrame({})
    IC = [list(overviewTable['IC_av1_{manometer}'.format(manometer=manometer)])]
    IC.append(list(overviewTable['IC_av2_{manometer}'.format(manometer=manometer)]))
    IC.append(list(overviewTable['IC_av3_{manometer}'.format(manometer=manometer)]))

    ne = [list(overviewTable['ne_av1'])]
    ne.append(list(overviewTable['ne_av2']))
    ne.append(list(overviewTable['ne_av3']))
    
    ECRH = [list(overviewTable['ECRH_av1'])]
    ECRH.append(list(overviewTable['ECRH_av2']))
    ECRH.append(list(overviewTable['ECRH_av3']))
   
    OP = list(overviewTable['OP'])*3

    overviewTableCombined['IC'] = np.hstack(np.array(IC))
    overviewTableCombined['ne'] = np.hstack(np.array(ne))
    overviewTableCombined['ECRH'] = np.hstack(np.array(ECRH))
    overviewTableCombined['OP'] = np.hstack(np.array(OP))

    fig1 = px.scatter_3d(overviewTableCombined,   
                         x = 'IC',                 
                         y = 'ECRH',
                         z = 'ne', 
                         color = overviewTableCombined['OP'],           
                         size = np.ones_like(overviewTableCombined['OP']))
    fig1.show()

urls = [urlAEA21, urlAEE11, urlAEE30, urlAEE41, urlAEE50, urlAEH11, urlAEH21, urlAEH30, urlAEH31, urlAEH50, urlAEH51, urlAEI30, urlAEI50, urlAEI51, urlAEL10, urlAEP30, urlAEP50, urlAEP51]
#urls = [urlAEP30]
manometers = ['AEA21', 'AEE11', 'AEE30', 'AEE41', 'AEE50', 'AEH11', 'AEH21' ,'AEH30', 'AEH31', 'AEH50', 'AEH51', 'AEI30', 'AEI50', 'AEI51', 'AEL10', 'AEP30', 'AEP50', 'AEP51']
#manometers = ['AEP30']

#refernece discharges
dischargeIDs = [#'20180809.25', '20180809.27', '20180809.38', '20180814.13',  '20180828.19', '20180828.21', '20180904.22', '20180904.23', '20180911.24', '20180912.10', '20181018.3', '20230126.4', '20241212.7', '20250409.8', '20250410.5',
                '20240918.5', '20241001.11', '20241008.40', '20241009.9', '20241016.14', '20241023.10', '20241023.11', '20241105.10', '20241106.6', '20241112.11', '20241113.18', '20241114.10', '20241120.8', '20241127.10', '20241203.7', '20241204.9', '20241205.9', '20241210.7', '20241212.9', 
                '20250311.62', '20250312.71', '20250325.65','20250326.11', '20250403.61', '20250423.32', '20250424.6', '20250506.9', '20250508.15', '20250513.6', '20250513.54', '20250514.10', '20250515.8', '20250521.9']

#only real reference discharges for OP2.2/2.3
dischargeIDs = ['20241008.40', '20241009.9', '20241016.14', '20241114.10', '20241127.10', '20241205.9', '20241210.7', '20241212.9', 
                '20250311.62', '20250312.71', '20250325.65', '20250424.6', '20250506.9', '20250513.6', '20250513.54', '20250514.10', '20250521.9']


OP21 = ['20230215.09', '20230215.08', '20221207.27', '20221207.24', '20221207.22', '20221207.21', '20221207.20', '20221129.35', '20221129.36', '20221201.8', '20221201.10', '20230216.40', '20230216.37', '20221206.32', '20221206.30', '20230328.46', '20230328.43', '20230328.11',
        '20221201.54', '20221201.48', '20221215.72', '20230125.10']

#times corresponding to ECRH step ends
times = [[2.94, 9.07, 15.05], [2.90, 9.04, 15.05], [3.06, 9.07, 15.02], [3.04, 9.04, 15.05], [3.04, 9.07, 15.07], [2.94, 9.07, 15.07], [3.04, 9.07, 15.03], [3.04, 9.07, 15.03], [3.06, 9.07, 15.07], [3.03, 9.03, 13.94], [3.02, 9.02, 15.07], [2.99, 9.05, 15.05], [2.99, 9.04, 15.02], [3.02, 9.05, 15.05], [3.04, 9.04, 15.05], [2.99, 9.04, 15.07], [2.99, 9.04, 15.07], [3.02, 9.07, 15.05], [3.04, 9.07, 15.10], 
         [2.99, 9.04, 15.07], [3.06, 9.02, 15.03], [3.04, 9.07, 15.05], [3.04, 9.05, 15.07], [3.06, 9.07, 15.10], [2.99, 9.05, 15.05], [2.97, 9.07, 15.05], [2.99, 9.05, 15.03], [3.02, 9.04, 15.07], [2.99, 9.04, 15.07], [2.99, 9.07, 15.10], [3.04, 9.04, 15.07], [2.99, 9.07, 15.05], [2.99, 9.02, 15.03]]

#only times for real reference discharges in OP2.2/2.3
times = [[3.06, 9.07, 15.02], [3.04, 9.04, 15.05], [3.04, 9.07, 15.07], [2.99, 9.05, 15.05], [3.02, 9.05, 15.05], [2.99, 9.04, 15.07], [3.02, 9.07, 15.05], [3.04, 9.07, 15.10], 
         [2.99, 9.04, 15.07], [3.06, 9.02, 15.03], [3.04, 9.07, 15.05], [2.97, 9.07, 15.05], [2.99, 9.05, 15.03], [2.99, 9.04, 15.07], [2.99, 9.07, 15.10], [3.04, 9.04, 15.07], [2.99, 9.02, 15.03]]

run = False
if run:
    url = {'p_Baratron': pBaratron['p'], 'p_BaratronRaw': pBaratron['p_raw'], 'p_ADBav_hpa': pADB_av_hpa['p'], 'p_ADBav_lpa': pADB_av_lpa['p']}
    for calibrationNumber in [2, 3, 4, 6, 7]:
        data =  w7xarchive.get_signal_for_program(url, calibrations[calibrationNumber]['program'])
        plt.plot(data['p_Baratron'][0], data['p_Baratron'][1], label='Baratron')
        plt.plot(data['p_BaratronRaw'][0], data['p_BaratronRaw'][1], label='Baratron Raw')
        plt.plot(data['p_ADBav_hpa'][0], data['p_ADBav_hpa'][1], label='average hpa')
        plt.plot(data['p_ADBav_lpa'][0], data['p_ADBav_lpa'][1], label='average lpa')
        plt.xlabel('time in s')
        plt.ylabel('pressure in mbar')
        plt.yscale('log')
        plt.legend()
        plt.savefig('plots/CalibrationPressureMeasurements/calibrationPressures{calibration}.png'.format(calibration=calibrations[calibrationNumber]['program']))
        plt.close()

run = False

if run:
    for manometer, url in zip(manometers[4:5], urls[4:5]):
        fig_H18, ax_H18 = plt.subplots(4, 1, layout='constrained', figsize=(10, 15))
        fig_H25, ax_H25 = plt.subplots(4, 1, layout='constrained', figsize=(10, 15))
        fig_He25, ax_He25 = plt.subplots(4, 1, layout='constrained', figsize=(10, 15))
        fig_25, ax_25 = plt.subplots(4, 1, layout='constrained', figsize=(10, 15))
        url['p'] = pBaratron['p']
        for calibration in calibrations:
            #data is dictionary with same keys as url, each data[key] is a tuple of two lists containing timestemps (index 0) and data (index 1)
            data = w7xarchive.get_signal_for_program(url, calibration['program']) 

            #test for existance of all datastreams
            keys = data.keys()
            if 'IC' in keys and 'EC' in keys:
                pass
            else:
                print('not all data present for {manometer}, {discharge}'.format(manometer=manometer, discharge=calibration['program']))
                continue

            #plot sensitivity times p depending on gas and B
            if len(data['IC'][0]) == len(data['EC'][0]):
                y = 0
                x = 0#int(len(data['EC'][0])*31/32)
                IC = overflow_correction(np.array(data['IC'][1][x:]))
                if calibration['gas'] == 'H2':
                    if calibration['B'] == 1.8:
                        ax_H18[0].semilogy(np.array(data['EC'][0][x:]) + y, IC/(np.array(data['EC'][1][x:]) - IC), label=calibration['program'])
                        ax_H18[1].semilogy(np.array(data['EC'][0][x:]) + y, IC * 1e6, label='IC ' + calibration['program'])
                        ax_H18[1].axhline(y=8.7499, color='grey', linestyle=':')
                        ax_H18[2].plot(np.array(data['EC'][0][x:]) + y, np.array(data['EC'][1][x:]) * 1e6, label='EC ' + calibration['program'])
                        ax_H18[3].semilogy(np.array(data['p'][0][x:]) + y, np.array(data['p'][1][x:]), label='p ' + calibration['program'])
                        #ax_H18[3].plot(np.array(data['hpa'][0][x:]) + y, np.array(data['hpa'][1][x:]), label='hpa ' + calibration['program'])
                        #ax_H18[3].plot(np.array(data['lpa'][0][x:]) + y, np.array(data['lpa'][1][x:]), label='lpa ' + calibration['program'])
                    elif calibration['B'] == 2.5:
                        if calibration['program'] == "20240910.30":
                            y = 35
                        elif calibration['program'] == "20240926.21":
                            y = 0
                        elif calibration['program'] == "20250220.25":
                            y = 35#13
                        elif calibration['program'] == "20250604.1":
                            y = 35
                        elif calibration['program'] == "20250605.43":
                            y = 35
                        ax_H25[0].semilogy(np.array(data['EC'][0][x:]) + y, IC/(np.array(data['EC'][1][x:]) - IC), label=calibration['program'])
                        ax_H25[1].semilogy(np.array(data['EC'][0][x:]) + y, IC * 1e6, label='IC ' + calibration['program'])
                        ax_H25[1].axhline(y=8.7499, color='grey', linestyle=':')
                        ax_H25[2].plot(np.array(data['EC'][0][x:]) + y, np.array(data['EC'][1][x:]) * 1e6, label='EC ' + calibration['program'])
                        ax_H25[3].semilogy(np.array(data['p'][0][x:]) + y, np.array(data['p'][1][x:]), label='p ' + calibration['program'])
                        #ax_H25[3].plot(np.array(data['hpa'][0][x:]) + y, np.array(data['hpa'][1][x:]), label='hpa ' + calibration['program'])
                        #ax_H25[3].plot(np.array(data['lpa'][0][x:]) + y, np.array(data['lpa'][1][x:]), label='lpa ' + calibration['program'])
                elif calibration['gas'] == 'He':
                    if calibration['program'] == "20240910.29":
                        y = 35#24
                    elif calibration['program'] == "20240926.22":
                        y = 0
                    elif calibration['program'] == "20250220.24":
                        y = 35#12
                    ax_He25[0].semilogy(np.array(data['EC'][0][x:]) + y, IC/(np.array(data['EC'][1][x:]) - IC), label=calibration['program'])
                    ax_He25[1].semilogy(np.array(data['EC'][0][x:]) + y, IC * 1e6, label='IC ' + calibration['program'])
                    ax_He25[1].axhline(y=8.7499, color='grey', linestyle=':')
                    ax_He25[2].plot(np.array(data['EC'][0][x:]) + y, np.array(data['EC'][1][x:]) * 1e6, label='EC ' + calibration['program'])
                    ax_He25[3].semilogy(np.array(data['p'][0][x:]) + y, np.array(data['p'][1][x:]), label='p ' + calibration['program'])
                    #ax_He25[3].plot(np.array(data['hpa'][0][x:]) + y, np.array(data['hpa'][1][x:]), label='hpa ' + calibration['program'])
                    #ax_He25[3].plot(np.array(data['lpa'][0][x:]) + y, np.array(data['lpa'][1][x:]), label='lpa ' + calibration['program'])
                elif calibration['gas'] == 'H2+He':
                    ax_25[0].semilogy(np.array(data['EC'][0][x:]) + y, IC/(np.array(data['EC'][1][x:]) - IC), label=calibration['program'])
                    ax_25[1].semilogy(np.array(data['EC'][0][x:]) + y, IC * 1e6, label='IC ' + calibration['program'])
                    ax_25[1].axhline(y=8.7499, color='grey', linestyle=':')
                    ax_25[2].plot(np.array(data['EC'][0][x:]) + y, np.array(data['EC'][1][x:]) * 1e6, label='EC ' + calibration['program'])
                    ax_25[3].semilogy(np.array(data['p'][0][x:]) + y, np.array(data['p'][1][x:]), label='p ' + calibration['program'])
                    #ax_25[3].plot(np.array(data['hpa'][0][x:]) + y, np.array(data['hpa'][1][x:]), label='hpa ' + calibration['program'])
                    #ax_25[3].plot(np.array(data['lpa'][0][x:]) + y, np.array(data['lpa'][1][x:]), label='lpa ' + calibration['program'])
        for i in range(4):
            ax_H18[i].set_xlim([0, 275])
            ax_H25[i].set_xlim([0, 275])
            ax_He25[i].set_xlim([0, 275])
            ax_25[i].set_xlim([0, 275])
            ax_H18[i].set_xlabel('time in s')
            ax_H25[i].set_xlabel('time in s')
            ax_He25[i].set_xlabel('time in s')
            ax_25[i].set_xlabel('time in s')
            ax_H18[i].legend()
            ax_H25[i].legend()
            ax_He25[i].legend()
            ax_25[i].legend()
            ax_H18[i].xaxis.grid()
            ax_H25[i].xaxis.grid()
            ax_He25[i].xaxis.grid()
            ax_25[i].xaxis.grid()

        ax_H18[0].set_ylim([0, 0.1])
        ax_H25[0].set_ylim([0, 0.1])
        ax_He25[0].set_ylim([0, 0.1])
        ax_25[0].set_ylim([0, 0.1])

        ax_H18[0].set_ylabel('sensitivity x pressure (IC/(EC - IC))')
        ax_H18[1].set_ylabel('ion current IC in 1e-6 A')
        ax_H18[2].set_ylabel('electron current EC in 1e-6 A')
        ax_H18[3].set_ylabel('neutral gas pressure p in mbar')
        ax_H25[0].set_ylabel('sensitivity x pressure (IC/(EC - IC))')
        ax_H25[1].set_ylabel('ion current IC in 1e-6 A')
        ax_H25[2].set_ylabel('electron current EC in 1e-6 A')
        ax_H25[3].set_ylabel('neutral gas pressure p in mbar')
        ax_He25[0].set_ylabel('sensitivity x pressure (IC/(EC - IC))')
        ax_He25[1].set_ylabel('ion current IC in 1e-6 A')
        ax_He25[2].set_ylabel('electron current EC in 1e-6 A')
        ax_He25[3].set_ylabel('neutral gas pressure p in mbar')
        ax_25[0].set_ylabel('sensitivity x pressure (IC/(EC - IC))')
        ax_25[1].set_ylabel('ion current IC in 1e-6 A')
        ax_25[2].set_ylabel('electron current EC in 1e-6 A')
        ax_H25[3].set_ylabel('neutral gas pressure p in mbar')
        

        safe = 'plots/Sensitivity/{manometer}_sensitivity_'.format(manometer=manometer)
        fig_H18.savefig(safe + 'H_18T.png', bbox_inches='tight')
        fig_H25.savefig(safe + 'H_25T.png', bbox_inches='tight')
        fig_He25.savefig(safe + 'He_25T.png', bbox_inches='tight')
        fig_25.savefig(safe + 'H+He_25T.png', bbox_inches='tight')

        fig_H18.show()
        fig_H25.show()
        fig_He25.show()
        fig_25.show()

        plt.close('all')




run = True
if run:
    safe = 'plots/IC_from_p/IC_from_p_'
    for manometer, url in zip(manometers[:1], urls[:1]):
        url['p'] = pBaratron['p']
        for calibrationCase in [['H2', 1.8], ['H2', 2.5], ['He', 2.5], ['H2+He', 2.5]]:
            for calibration in calibrations:
                if calibration['gas'] == calibrationCase[0] and calibration['B'] == calibrationCase[1]:
                    #data is dictionary with same keys as url, each data[key] is a tuple of two lists containing timestemps (index 0) and data (index 1)
                    data = w7xarchive.get_signal_for_program(url, calibration['program'])
                    p = pd.DataFrame({'time': np.round(data['p'][0], 3), 'p': data['p'][1]})
                    IC = pd.DataFrame({'time': np.round(data['IC'][0], 3), 'IC': data['IC'][1]})
                    merged = pd.merge(p, IC, on='time', how='outer')
                    print(IC.head())
                    print(p.head(30))
                    print(merged.head(100))
                    #merged.fillna(0,inplace=True)
                    plt.plot(merged['p'], merged['IC'], 'x', label=calibration['program'])
            plt.xscale('log')
            plt.yscale('log')
            plt.xlabel('pressure p in mbar')
            plt.ylabel('ion current IC in A')
            plt.legend()
            plt.savefig(safe + manometer + '_' + calibrationCase[0] + '_' + str(calibrationCase[1]) + 'T.png', bbox_inches='tight')
            plt.close()
            
run = False
if not run:
    exit()

#get raw neutral gas manometer data (ion current, electron current, heating current, heating voltage, corresponding ECRH heating and electron density) as .csv file and plots
getManometerDataRaw(manometers, urls, dischargeIDs, times)

#scatter plots to show IC(ne), IC(ECRH), and IC(ne, ECRH) depending on OP(color coded)
overviewTable = pd.read_csv('overviewQRGdata.csv', sep=';')
scatterPlotICfromX(overviewTable, 'ECRH')
scatterPlotICfromX(overviewTable, 'ne')
scatterPlotICfromX3D(overviewTable)

#for campagnes without real reference discharges, find similar value pairs ECRH and ne with corresponding NGM data
#findReferenceDischarges('20240918.5', urlAEP30, 5*1e19, 2500)

for calibration_date in calibration_dates[:]:
    t1, t2 = w7xarchive.to_timestamp(calibration_date)
    t0 = w7xarchive.to_timestamp(calibration_date[0][:11] + '00:00:00')
    
    data = w7xarchive.get_signal(pADB_av_hpa, t1, t2)
    plt.plot((data['p'][0] - t0)/3600 * 1e-9, data['p'][1])
    plt.xlabel('time in [h] since 00:00:00 of that day')
    plt.ylabel('pressure ADB_av_hlp in [mbar]')
    safe = "HiwiNeutralGasPressure/plots/{calibration_date}_{h}-{min}-{s}.png".format(calibration_date=calibration_date[0][:10], h=calibration_date[0][11:13], min=calibration_date[0][14:16], s=calibration_date[0][-2:])
    plt.savefig(safe, bbox_inches='tight')
    
    plt.close()