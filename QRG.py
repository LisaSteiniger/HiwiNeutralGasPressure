import w7xarchive
import itertools
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import matplotlib as mpl
import scipy
from scipy.signal import argrelextrema

from links import *

mpl.rcParams['agg.path.chunksize'] = 10000
#https://w7x-logbook.ipp-hgw.mpg.de/components?id=DCH#dataaccess

####################################################################################################################
#FUNCTIONS FOR TESTING SENSITIVITY
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

####################################################################################################################
#COLLECT GENERAL INFORMATION ABOUT DISCHARGES
def readCryoPumpStatus(dischargeID: str|list[str]) -> tuple[str, float, float]|list[tuple[str, float, float]]:
    '''This function reads out the status of the cryopumps for a given discharge or list of discharges
        Returns a tuple or list of tuples with three elements each: dischargeID, inlet temperature, and returned temperature'''
    
    urlCVP = {'inletT': "ArchiveDB/raw/W7X/ControlStation.2139/BCA.5_DATASTREAM/0/BCA5_20TI8200",
            'returnT': "ArchiveDB/raw/W7X/ControlStation.2139/BCA.5_DATASTREAM/1/BCA5_21TI8200"}

    if type(dischargeID) == list:
        statusList = []
        for shotnumber in dischargeID:
            data = w7xarchive.get_signal_for_program(urlCVP, shotnumber)
            statusList.append([shotnumber, np.mean(np.array(data['inletT'][1])), np.mean(np.array(data['returnT'][1]))])
    else:
        data = w7xarchive.get_signal_for_program(urlCVP, dischargeID)
        statusList = [dischargeID, round(np.mean(np.array(data['inletT'][1])), 1), round(np.mean(np.array(data['returnT'][1])), 1)]

    return statusList

def readECav_HCav(dischargeID: str, url_manometer: dict) -> tuple[str|str]:
    ''' get average electron and heating current of one manometer for a specific discharge (e.g. calibration program)'''
    n = 50 #skip the first n data points
    data = w7xarchive.get_signal_for_program(url_manometer, dischargeID)
    merged = pd.merge(pd.DataFrame({'time': np.round(np.array(data['EC'][0]), 3), 'EC': data['EC'][1]}), pd.DataFrame({'time': np.round(np.array(data['HC'][0]), 3), 'HC': data['HC'][1]}), 'outer', on='time')
    filter_EC = [x > 50 * 1e-6 for x in merged['EC']]
    if sum(filter_EC) > 0:
        avEC = round(np.mean(merged['EC'][filter_EC.index(True) + n : len(filter_EC) - 1 - filter_EC[::-1].index(True) - n]) * 1e6, 1)
        avHC = round(np.mean(merged['HC'][filter_EC.index(True) + n : len(filter_EC) - 1 - filter_EC[::-1].index(True) - n]), 1)
    else:
        avEC = '<50'       
        avHC = 'unknown'       
    return str(avEC), str(avHC)

####################################################################################################################
#BEHAVIOUR OF MANOMETERS IN REFERENCE DISCHARGES

def findReferenceDischarges(dischargeID, url, ne, ECRH):
    '''not working, should find comparable discharges for campaigns not following the recent reference discharge pattern'''
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

def calibrationTimesFromCalibrationDate(calibration_dates):
    for calibration_date in calibration_dates:
        ''' not used any more, initially used to search calibration programs when ID is unknown'''
        t1, t2 = w7xarchive.to_timestamp(calibration_date)
        t0 = w7xarchive.to_timestamp(calibration_date[0][:11] + '00:00:00')
        
        data = w7xarchive.get_signal(pADB_av_hpa, t1, t2)
        plt.plot((data['p'][0] - t0)/3600 * 1e-9, data['p'][1])
        plt.xlabel('time in [h] since 00:00:00 of that day')
        plt.ylabel('pressure ADB_av_hlp in [mbar]')
        safe = "plots/{calibration_date}_{h}-{min}-{s}.png".format(calibration_date=calibration_date[0][:10], h=calibration_date[0][11:13], min=calibration_date[0][14:16], s=calibration_date[0][-2:])
        plt.savefig(safe, bbox_inches='tight')
        
        plt.close()

def getManometerDataRaw(manometers, urls, dischargeIDs, times):
    ''' read out the manometer data (ion/electron/heating current + heating voltage) and corresponding electron density and P_ECRH
        works for reference discharges of OP2.2 and 2.3
        averages the parameters for each of the three P_ECRH steps of the discharge (ne, P_ECRH, IC) or the whole discharge (EC, HC, HV)
        results are saved in .csv file'''
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

def scatterPlotICfromX(overviewTable, X_name, manometer='AEP30'):
    ''' scatter plot for one manometer, plots ion current in dependency of one plasma parameter (ne or P_ECRH)
        based on data collected during reference discharges of OP2.2 and 2.3'''
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
    ''' 3D scatter plot for one manometer, shows ion current in dependency of electron density and P_ECRH
        based on data collected during reference discharges of OP2.2 and 2.3'''
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

####################################################################################################################
#INVESTIGATE CALIBRATION PROGRAMS
def plotGasPressureFlowAndValveVoltageDay(dates=["2024-09-10 ", "2024-09-26 ", "2025-02-18 ", "2025-02-20 ",  "2025-06-04 ",  "2025-06-05 "]):
    ''' plots the pressure in the gas boxes, the valve voltages, and gas flow rates for main inlet of H and He gas
        plots for the whole day (e.g. day with NGM calibration program(s))'''
    for date in dates:
        fig, ax = plt.subplots(2, 3, layout='constrained', figsize=(15, 8), sharex='col')
        t1, t2 = w7xarchive.to_timestamp([date + '00:00:00', date + '23:59:59'])
        
        data = w7xarchive.get_signal(url_gasValves, t1, t2)
        ax[0][0].plot((np.array(data['BG013H_p'][0]) - t1)/3600 * 1e-9, data['BG013H_p'][1], label='H box BG013')
        ax[1][0].plot((np.array(data['BG034He_p'][0]) - t1)/3600 * 1e-9, data['BG034He_p'][1], label='He box BG034')

        ax[0][1].plot((np.array(data['BG013H_V'][0]) - t1)/3600 * 1e-9, data['BG013H_V'][1], label='H valve BG013')
        ax[1][1].plot((np.array(data['BG034He_V'][0]) - t1)/3600 * 1e-9, data['BG034He_V'][1], label='He valve BG034')

        ax[0][2].plot((np.array(data['BG013H_flow'][0]) - t1)/3600 * 1e-9, data['BG013H_flow'][1], label='H valve BG013')
        ax[1][2].plot((np.array(data['BG034He_flow'][0]) - t1)/3600 * 1e-9, data['BG034He_flow'][1], label='He valve BG034')
        
        ax[0][0].set_ylabel('pressure in gas box in bar')
        ax[1][0].set_ylabel('pressure in gas box in bar')
        ax[0][1].set_ylabel('voltage at gas valve in V')
        ax[1][1].set_ylabel('voltage at gas valve in V')
        ax[0][2].set_ylabel('gas flow through gas valve in mbar l/s')
        ax[1][2].set_ylabel('gas flow through gas valve in mbar l/s')
        
        ax[0][0].legend()
        ax[0][1].legend()
        ax[1][0].legend()
        ax[1][1].legend()
        ax[0][2].legend()
        ax[1][2].legend()

        ax[0][0].xaxis.grid()
        ax[0][1].xaxis.grid()
        ax[1][0].xaxis.grid()
        ax[1][1].xaxis.grid()
        ax[0][2].xaxis.grid()
        ax[1][2].xaxis.grid()

        ax[1][0].set_xlabel('time in [h] since 00:00:00 of that day')
        ax[1][1].set_xlabel('time in [h] since 00:00:00 of that day')
        ax[1][2].set_xlabel('time in [h] since 00:00:00 of that day')
        
        safe = "plots/CalibrationPressureMeasurements/{calibration_date}.png".format(calibration_date=date[:-1])
        fig.show()
        fig.savefig(safe, bbox_inches='tight')
        plt.close()

def plotPressureStepsOfCalibrationProgram(calibrationIDs=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]):
    ''' plots the pressures measured by different systems for each calibration program given by calibrationIDs
        additionally plots flow rates and valve voltages for main H and He gas inlet'''
    url = url_gasValves
    url['p_Baratron'] = pBaratron['p']
    url['p_BaratronRaw'] = pBaratron['p_raw']
    url['p_ADBav_hpa'] = pADB_av_hpa['p']
    url['p_ADBav_lpa'] = pADB_av_lpa['p']
    url['p_ADBav_CP302'] = p_CP302['p_ADBav']
    url['p_ADBav_CP301'] = pADB_av_CP301['p']
    
    for calibrationNumber in calibrationIDs:
        fig, ax = plt.subplots(4, 1, layout='constrained', figsize=(10, 15), sharex=True)
        data =  w7xarchive.get_signal_for_program(url, calibrations[calibrationNumber]['program'])
        startTime = w7xarchive.get_program_from_to(calibrations[calibrationNumber]['program'])[0]#w7xarchive.get_program_t0(calibrations[calibrationNumber]['program'])
        startTime = w7xarchive.to_stringdate(startTime)

        ax[0].plot(data['p_Baratron'][0], data['p_Baratron'][1], label='Baratron')
        ax[0].plot(data['p_BaratronRaw'][0], data['p_BaratronRaw'][1], label='Baratron Raw')
        ax[0].plot(data['p_ADBav_hpa'][0], data['p_ADBav_hpa'][1], label='average hpa')
        ax[0].plot(data['p_ADBav_lpa'][0], data['p_ADBav_lpa'][1], label='average lpa')
        ax[0].plot(data['p_ADBav_CP301'][0], data['p_ADBav_CP301'][1], label='average CP301')
        ax[0].plot(data['p_ADBav_CP302'][0], data['p_ADBav_CP302'][1], label='average CP302')

        ax[1].plot(data['BG013H_p'][0], data['BG013H_p'][1], label='H box BG013')
        ax[1].plot(data['BG034He_p'][0], data['BG034He_p'][1], label='He box BG034')

        ax[2].plot(data['BG013H_V'][0], data['BG013H_V'][1], label='H valve BG013')
        ax[2].plot(data['BG034He_V'][0], data['BG034He_V'][1], label='He valve BG034')

        ax[3].plot(data['BG013H_flow'][0], data['BG013H_flow'][1], label='H valve BG013')
        ax[3].plot(data['BG034He_flow'][0], data['BG034He_flow'][1], label='He valve BG034')
        
        #ax[0].set_xlabel('time in s starting from {startTime}'.format(startTime=startTime))
        #ax[1].set_xlabel('time in s starting from {startTime}'.format(startTime=startTime))
        ax[2].set_xlabel('time in s starting from {startTime}'.format(startTime=startTime))
        
        ax[0].set_ylabel('pressure in mbar')
        ax[1].set_ylabel('pressure in gas box in bar')
        ax[2].set_ylabel('voltage at gas valve in V')
        ax[3].set_ylabel('gas flow through gas valve in mbar l/s')
        
        ax[0].set_yscale('log')
        
        ax[0].legend()
        ax[1].legend()
        ax[2].legend()
        ax[3].legend()

        fig.savefig('plots/CalibrationPressureMeasurements/calibrationPressures_{gas}_{B}_{calibration}.png'.format(gas=calibrations[calibrationNumber]['gas'], B=calibrations[calibrationNumber]['B'], calibration=calibrations[calibrationNumber]['program']))
        fig.show()
        plt.close()


def investigateSensitivityOfManometer(manometers, urls):
    ''' plots electron and ion current, sensitivity, and pressure for each manometer in manometers for each category of calibration program
        e.g. all H programs with 2.5T are plotted together for each manometer'''
    for manometer, url in zip(manometers, urls):
        fig_H18, ax_H18 = plt.subplots(4, 1, layout='constrained', figsize=(10, 15))
        fig_H25, ax_H25 = plt.subplots(4, 1, layout='constrained', figsize=(10, 15))
        fig_He25, ax_He25 = plt.subplots(4, 1, layout='constrained', figsize=(10, 15))
        fig_25, ax_25 = plt.subplots(4, 1, layout='constrained', figsize=(10, 15))
        url['p'] = pBaratron['p']
        for calibration in calibrations:
            calibration['EC'], calibration['HC'] = readECav_HCav(calibration['program'], url)
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
                y = calibration['y']
                x = 0#int(len(data['EC'][0])*31/32)
                time_axis = np.array(data['EC'][0][x:]) + y
                
                if manometer in calibration['inactive']:
                    EC = np.zeros_like(time_axis)
                    IC = np.ones_like(time_axis)
                    IC = IC * 1e-9
                    sensitivity = IC * 1e4
                else:
                    IC = overflow_correction(np.array(data['IC'][1][x:]))
                    sensitivity = IC/(np.array(data['EC'][1][x:]) - IC)
                    EC = np.array(data['EC'][1][x:])

                if calibration['gas'] == 'H2':
                    if calibration['B'] == 1.8 or calibration['program'] == '20240910.30' or calibration['program'] == '20240926.22':
                        ax_H18[0].semilogy(time_axis, sensitivity, label=calibration['program'] + ', CVP (K): ' + calibration['CVP'] + ', B (T): ' + str(calibration['B']))
                        ax_H18[1].semilogy(time_axis, IC * 1e6, label='IC ' + calibration['program'] + ', CVP (K): ' + calibration['CVP'] + ', B (T): ' + str(calibration['B']))
                        ax_H18[1].axhline(y=8.7499, color='grey', linestyle=':')
                        ax_H18[2].plot(time_axis, EC * 1e6, label='EC ' + calibration['program'] + ', CVP (K): ' + calibration['CVP'] + ', B (T): ' + str(calibration['B']))
                        ax_H18[3].semilogy(np.array(data['p'][0][x:]) + y, np.array(data['p'][1][x:]), label='p ' + calibration['program'] + ', CVP (K): ' + calibration['CVP'] + ', B (T): ' + str(calibration['B']))
                        #ax_H18[3].plot(np.array(data['hpa'][0][x:]) + y, np.array(data['hpa'][1][x:]), label='hpa ' + calibration['program'])
                        #ax_H18[3].plot(np.array(data['lpa'][0][x:]) + y, np.array(data['lpa'][1][x:]), label='lpa ' + calibration['program'])
                    
                    elif calibration['B'] == 2.5:
                        ax_H25[0].semilogy(time_axis, sensitivity, label=calibration['program'] + ', CVP (K): ' + calibration['CVP'])
                        ax_H25[1].semilogy(time_axis, IC * 1e6, label=calibration['program'] + ', CVP (K): ' + calibration['CVP'])
                        ax_H25[1].axhline(y=8.7499, color='grey', linestyle=':')
                        ax_H25[2].plot(time_axis, EC * 1e6, label=calibration['program'] + ', CVP (K): ' + calibration['CVP'])
                        ax_H25[3].semilogy(np.array(data['p'][0][x:]) + y, np.array(data['p'][1][x:]), label=calibration['program'] + ', CVP (K): ' + calibration['CVP'])
                        #ax_H25[3].plot(np.array(data['hpa'][0][x:]) + y, np.array(data['hpa'][1][x:]), label='hpa ' + calibration['program'])
                        #ax_H25[3].plot(np.array(data['lpa'][0][x:]) + y, np.array(data['lpa'][1][x:]), label='lpa ' + calibration['program'])
                
                elif calibration['gas'] == 'He':
                    ax_He25[0].semilogy(time_axis, sensitivity, label=calibration['program'] + ', CVP (K): ' + calibration['CVP'])
                    ax_He25[1].semilogy(time_axis, IC * 1e6, label=calibration['program'] + ', CVP (K): ' + calibration['CVP'])
                    ax_He25[1].axhline(y=8.7499, color='grey', linestyle=':')
                    ax_He25[2].plot(time_axis, EC * 1e6, label=calibration['program'] + ', CVP (K): ' + calibration['CVP'])
                    ax_He25[3].semilogy(np.array(data['p'][0][x:]) + y, np.array(data['p'][1][x:]), label=calibration['program'] + ', CVP (K): ' + calibration['CVP'])
                    #ax_He25[3].plot(np.array(data['hpa'][0][x:]) + y, np.array(data['hpa'][1][x:]), label='hpa ' + calibration['program'])
                    #ax_He25[3].plot(np.array(data['lpa'][0][x:]) + y, np.array(data['lpa'][1][x:]), label='lpa ' + calibration['program'])
                
                elif calibration['gas'] == 'H2+He':
                    ax_25[0].semilogy(time_axis, sensitivity, label=calibration['program'] + ', CVP (K): ' + calibration['CVP'])
                    ax_25[1].semilogy(time_axis, IC * 1e6, label=calibration['program'] + ', CVP (K): ' + calibration['CVP'])
                    ax_25[1].axhline(y=8.7499, color='grey', linestyle=':')
                    ax_25[2].plot(time_axis, EC * 1e6, label=calibration['program'] + ', CVP (K): ' + calibration['CVP'])
                    ax_25[3].semilogy(np.array(data['p'][0][x:]) + y, np.array(data['p'][1][x:]), label=calibration['program'] + ', CVP (K): ' + calibration['CVP'])
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
        ax_H18[3].set_ylabel('neutral gas pressure (baratron) p in mbar')
        ax_H25[0].set_ylabel('sensitivity x pressure (IC/(EC - IC))')
        ax_H25[1].set_ylabel('ion current IC in 1e-6 A')
        ax_H25[2].set_ylabel('electron current EC in 1e-6 A')
        ax_H25[3].set_ylabel('neutral gas pressure (baratron) p in mbar')
        ax_He25[0].set_ylabel('sensitivity x pressure (IC/(EC - IC))')
        ax_He25[1].set_ylabel('ion current IC in 1e-6 A')
        ax_He25[2].set_ylabel('electron current EC in 1e-6 A')
        ax_He25[3].set_ylabel('neutral gas pressure (baratron) p in mbar')
        ax_25[0].set_ylabel('sensitivity x pressure (IC/(EC - IC))')
        ax_25[1].set_ylabel('ion current IC in 1e-6 A')
        ax_25[2].set_ylabel('electron current EC in 1e-6 A')
        ax_25[3].set_ylabel('neutral gas pressure (baratron) p in mbar')
        

        safe = 'plots/Sensitivity/{manometer}_sensitivity_'.format(manometer=manometer)
        fig_H18.savefig(safe + 'H.png', bbox_inches='tight')
        fig_H25.savefig(safe + 'H_25T.png', bbox_inches='tight')
        fig_He25.savefig(safe + 'He_25T.png', bbox_inches='tight')
        fig_25.savefig(safe + 'H+He_25T.png', bbox_inches='tight')

        fig_H18.show()
        fig_H25.show()
        fig_He25.show()
        fig_25.show()

        plt.close('all')


def plotIonCurrentFromPressureCalibration(manometers, urls):
    ''' for each manometer given in manometers the ion current is plotted in dependency of the pressure for each category of calibration program'''
    safe = 'plots/IC_from_p/IC_from_p_'
    for manometer, url in zip(manometers, urls):
        url['p'] = pBaratron['p']
        for calibrationCase in [['H2', 1.8], ['H2', 2.5], ['He', 2.5], ['H2+He', 2.5]]:
            for calibration in calibrations:
                calibration['EC'], calibration['HC'] = readECav_HCav(calibration['program'], url)
                if calibration['gas'] == calibrationCase[0] and calibration['B'] == calibrationCase[1]:
                    if manometer in calibration['inactive']:
                        plt.axhline(1e-9, label=calibration['program'] + ', CVP (K): ' + calibration['CVP']+ ', EC (µA): ' + calibration['EC']+ ', HC (V): ' + calibration['HC'])
                        continue
            
                    #data is dictionary with same keys as url, each data[key] is a tuple of two lists containing timestemps (index 0) and data (index 1)
                    data = w7xarchive.get_signal_for_program(url, calibration['program'])
                    p = pd.DataFrame({'time': np.round(data['p'][0], 3), 'p': data['p'][1]})
                    IC = pd.DataFrame({'time': np.round(data['IC'][0], 3), 'IC': overflow_correction(np.array(data['IC'][1]))})
                    merged = pd.merge(p, IC, on='time', how='outer')
                    #print(IC.head())
                    #print(p.head(30))
                    #print(merged.head(100))
                    #merged.fillna(0,inplace=True)
                    plt.plot(merged['p'], merged['IC'], 'x', label=calibration['program']+ ', CVP (K): ' + calibration['CVP']+ ', EC (µA): ' + calibration['EC']+ ', HC (V): ' + calibration['HC'])
                    plt.axhline(y=8.7499e-6, color='grey', linestyle=':')
            plt.xscale('log')
            plt.yscale('log')
            plt.xlabel('pressure p (baratron) in mbar')
            plt.ylabel('ion current IC in A')
            plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15))
            plt.savefig(safe + manometer + '_' + calibrationCase[0] + '_' + str(calibrationCase[1]) + 'T.png', bbox_inches='tight')
            plt.close()

####################################################################################################################
#MY OWN CALIBRATION ATTEMPT
def calibrateManometer(manometers, urls, calibration, step_indices, nan_thresh=8.7499e-6):
    ''' calibrate each manometer given by manometers based on one calibration program given by dischargeID'''
    for manometer, url in zip(manometers, urls):
        url['p'] = pBaratron['p']
        data = w7xarchive.get_signal_for_program(url, calibration['program'])
        #merged = pd.merge(pd.DataFrame({'time': np.round(np.array(data['p'][0]), 3), 'p': data['p'][1]}), pd.DataFrame({'time': np.round(np.array(data['IC'][0]), 3), 'IC': data['IC'][1]}), 'outer', on='time')

        #the below is to find the time intervals as a first approximation -> must be corrected manualy
        #ignore if those indices are already known
        '''
        #find times when pressure steps up -> find middle 50% of each time interval
        slopes = np.array([(x - y)/(tx - ty) for x, y, tx, ty in zip(data['p'][1][1:], data['p'][1][:-1], data['p'][0][1:], data['p'][0][:-1])])
        #for local maxima
        maxima = argrelextrema(slopes, np.greater)
        slopes2 = np.array([(x - y)/(tx - ty) for x, y, tx, ty in zip(np.array(data['p'][1][:-1])[maxima][1:], np.array(data['p'][1][:-1])[maxima][:-1], np.array(data['p'][0][:-1])[maxima][1:], np.array(data['p'][0][:-1])[maxima][:-1])])
        #for local maxima
        maxima2 = argrelextrema(slopes2, np.greater)
        #indices of the data points having the steepest slope
        print([list(np.array(data['p'][0][:-1])).index(x) for x in np.array(data['p'][0][:-1])[maxima][:-1][maxima2]])
        '''
        timeintervalStart = [data['p'][0][x] + 0.25 * (data['p'][0][y] - data['p'][0][x]) for x, y in zip(step_indices[:-1], step_indices[1:])]
        timeintervalStop = [data['p'][0][x] + 0.75 * (data['p'][0][y] - data['p'][0][x]) for x, y in zip(step_indices[:-1], step_indices[1:])]
        timeintervalStart.append(data['p'][0][step_indices[-1]] + 0.25 * (data['p'][0][-1] - data['p'][0][step_indices[-1]]))
        timeintervalStop.append(data['p'][0][step_indices[-1]] + 0.75 * (data['p'][0][-1] - data['p'][0][step_indices[-1]]))
        timeintervalStart = np.round(np.array(timeintervalStart), 3)
        timeintervalStop = np.round(np.array(timeintervalStop), 3)

        plt.plot(data['p'][0], data['p'][1], label='baratron')
        plt.plot(np.array(data['p'][0][:-1])[step_indices], np.array(data['p'][1][:-1])[step_indices], 'x', label='local slope maxima')
        for lineStart, lineEnd in zip(timeintervalStart, timeintervalStop):
            plt.axvspan(lineStart, lineEnd, color='grey')
        
        plt.yscale('log')
        plt.xlabel('time in s')
        plt.ylim([1e-8, 0.5*1e-1])
        plt.ylabel('baratron pressure in mbar')
        plt.legend()
        plt.savefig('plots/calibrationAttempt/{gas}_{B}_{program}.png'.format(program=calibration['program'], gas=calibration['gas'], B=calibration['B']))
        plt.close()

        
        #read signal for p and IC and average their values in each interval
        step_IC, step_p = [], []
        n = 0
        for lineStart, lineEnd in zip(timeintervalStart, timeintervalStop):
            startIC = np.argmin(np.array(list(map(lambda x: abs(x - lineStart), data['IC'][0]))))
            start_p = np.argmin(np.array(list(map(lambda x: abs(x - lineStart), data['p'][0]))))
            stopIC = np.argmin(np.array(list(map(lambda x: abs(x - lineEnd), data['IC'][0]))))
            stop_p = np.argmin(np.array(list(map(lambda x: abs(x - lineEnd), data['p'][0]))))
            IC = overflow_correction(np.array(data['IC'][1]))
            if nan_thresh:
                overflow_indices = np.where(IC >= nan_thresh)[0]
                IC[overflow_indices] = np.nan
            step_IC.append(np.mean(IC[startIC:stopIC]))
            step_p.append(np.mean(np.array(data['p'][1])[start_p:stop_p]))
        plt.plot(step_IC, step_p, 'x', label='{manometer} {gas} {B}T'.format(manometer=manometer, gas=calibration['gas'], B=calibration['B']))

        step_IC = list(map(lambda x: np.log10(x), step_IC))
        step_p = list(map(lambda x: np.log10(x), step_p))

        nan_filter = np.array([not np.isnan(x) and not np.isnan(y) and y > -5 and y < -2 for x, y in zip(step_IC, step_p)])
        step_IC = np.array(step_IC)[nan_filter]
        step_p = np.array(step_p)[nan_filter]

        #find least square fit of a linear function through that log-log data
        paramsPolyfit = np.polyfit(step_IC, step_p, 1)
        paramsCurvefit, rest = scipy.optimize.curve_fit(lambda x, m, b: m * x + b, step_IC, step_p)

        #define model (linear)        
        def model(params, x):
            m, b = params
            return m * x + b
        #define residual function
        def residuals(params, x, y):
            return model(params, x) - y
        #initial guess
        initial_params = [paramsPolyfit[0], paramsPolyfit[1]]

        # Fit without robust loss
        result_no_robust = scipy.optimize.least_squares(residuals, initial_params, args=(step_IC, step_p))

        # Fit with robust loss
        result_robust = scipy.optimize.least_squares(
            residuals, initial_params, args=(step_IC, step_p), loss='soft_l1', f_scale=10
        )

        #plot log(p) of log(IC)
        plt.plot(10**step_IC, 10**(paramsPolyfit[0] * step_IC + paramsPolyfit[1]), label='polyfit (m = {m:.2f}, b = {b:.2f})'.format(m=paramsPolyfit[0], b=paramsPolyfit[1]))
        plt.plot(10**step_IC, 10**(paramsCurvefit[0] * step_IC + paramsCurvefit[1]), label='curvefit (m = {m:.2f}, b = {b:.2f})'.format(m=paramsCurvefit[0], b=paramsCurvefit[1]))
        plt.plot(10**step_IC, 10**(model(result_no_robust.x, step_IC)), label='least squares fit')
        plt.plot(10**step_IC, 10**(model(result_robust.x, step_IC)), label='least squares fit robust')
        plt.xlabel('Ion current IC in A')
        plt.ylabel('Baratron pressure p in mbar')
        plt.legend()
        plt.xscale('log')
        plt.yscale('log')
        plt.savefig('plots/calibrationAttempt/PressureFromIC_{manometer}_{gas}_{B}_{program}.png'.format(manometer=manometer, program=calibration['program'], gas=calibration['gas'], B=calibration['B']))
        plt.close()        

####################################################################################################################
#INPUT PARAMETERS
urls = [urlAEA21, urlAEE11, urlAEE30, urlAEE41, urlAEE50, urlAEH11, urlAEH21, urlAEH30, urlAEH31, urlAEH50, urlAEH51, urlAEI30, urlAEI50, urlAEI51, urlAEL10, urlAEP30, urlAEP50, urlAEP51]
urls = [urlAEH50, urlAEH51, urlAEI50, urlAEP51, urlAEP30, urlAEL10]
manometers = ['AEA21', 'AEE11', 'AEE30', 'AEE41', 'AEE50', 'AEH11', 'AEH21' ,'AEH30', 'AEH31', 'AEH50', 'AEH51', 'AEI30', 'AEI50', 'AEI51', 'AEL10', 'AEP30', 'AEP50', 'AEP51']
manometers = ['AEH50', 'AEH51', 'AEI50', 'AEP51', 'AEP30', 'AEL10']

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

#####################################################################################################################
#RUNNING PROGRAM
#read cyro-vaccum pump status (av temp), av EC and av HC
for calibrationNumber in range(len(calibrations)):
    calibrations[calibrationNumber]['CVP'] = str(readCryoPumpStatus(calibrations[calibrationNumber]['program'])[1])

#get raw neutral gas manometer data (ion current, electron current, heating current, heating voltage, corresponding ECRH heating and electron density) as .csv file and plots
#getManometerDataRaw(manometers, urls, dischargeIDs, times)

#scatter plots to show IC(ne), IC(ECRH), and IC(ne, ECRH) depending on OP(color coded)
#overviewTable = pd.read_csv('overviewQRGdata.csv', sep=';')
#scatterPlotICfromX(overviewTable, 'ECRH')
#scatterPlotICfromX(overviewTable, 'ne')
#scatterPlotICfromX3D(overviewTable)

#for campagnes without real reference discharges, find similar value pairs ECRH and ne with corresponding NGM data
#findReferenceDischarges('20240918.5', urlAEP30, 5*1e19, 2500)

#plotGasPressureFlowAndValveVoltageDay()
#plotPressureStepsOfCalibrationProgram()
#investigateSensitivityOfManometer(manometers[:], urls[:])
#plotIonCurrentFromPressureCalibration(manometers[:], urls[:])
        

#indices of steepest slope in pressure data
step_indices20240926_22 = [492, 577, 623, 672, 720, 767, 813, 860, 909, 960, 1010, 1067, 1134]
step_indices20250605_43 = [371, 409, 449, 494, 534, 579, 620, 664, 709, 757, 804, 861]
for calibration, step_indices in zip([calibrations[3], calibrations[-1]], [step_indices20240926_22, step_indices20250605_43]):
    calibrateManometer(manometers[:], urls[:], calibration, step_indices)
