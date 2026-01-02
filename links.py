#Pfeiffer Piezo Pirani (RPT100): 10-4 to 1200 mbar -> gas correction factor [Pfeiffer RPT100 datasheet.pdf]: N2, Air=1, H2=0.58, He=1.02, Ar=1.59
#Pennings (IKR 070) 10-11 to 5e-03 mbar [https://www.pfeiffer-vacuum.com/filepool/file/measurement/bg5033bde_a.pdf?referer=1844&detailPdoId=3860&request_locale=de_DE]:  Peff = K**angezeigter Druck: N2, Air, O2, CO2 =1, Xe=0.4, Kr=0.5, Ar=0.8, H2=2.4, He=5.9, Ne=4.1

#look for OP1.2b data of NGMs: http://archive-webapi.ipp-hgw.mpg.de/ArchiveDB/raw/W7X/QRG_Manometer/CAB01_CHC_DATASTREAM

#cryo pump status
urlCVP = {'inletT': "ArchiveDB/raw/W7X/ControlStation.2139/BCA.5_DATASTREAM/0/BCA5_20TI8200",
          'returnT': "ArchiveDB/raw/W7X/ControlStation.2139/BCA.5_DATASTREAM/1/BCA5_21TI8200"}

#neutral gas manometer archive links
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

#pressure gauges archive links
pADB_av_AEH18 = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/899/ADB18_CP402/scaled", #this is where I think I must go to
                 'p_archive': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/897/ADB59_Reserve100[19]/scaled", #this is where the archive sends me
                 'p_victoria': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/897/ADB18_CP402/scaled"} 

pADB_av_AEH19 = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/901/ADB19_CP402/scaled", #this is where I think I must go to
                 'p_archive': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/899/ADB18_CP402/scaled", #this is where the archive sends me
                 'p_victoria': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/899/ADB19_CP402/scaled"} 

pADB_av_AEH28 = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/903/ADB28_CP402/scaled", 
                 'p_archive': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/901/ADB19_CP402/scaled", #this is where the archive sends me
                 'p_victoria': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/901/ADB28_CP402/scaled"} 

pADB_av_AEH29 = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/905/ADB29_CP402/scaled",
                 'p_archive': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/903/ADB28_CP402/scaled", #this is where the archive sends me
                 'p_victoria': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/903/ADB29_CP402/scaled"} 

pADB_av_AEH38 = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/907/ADB38_CP402/scaled",
                 'p_archive': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/905/ADB29_CP402/scaled", #this is where the archive sends me
                 'p_victoria': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/905/ADB38_CP402/scaled"} 

pADB_av_AEH39 = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/909/ADB39_CP402/scaled",
                 'p_archive': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/907/ADB38_CP402/scaled", #this is where the archive sends me
                 'p_victoria': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/907/ADB39_CP402/scaled"} 

pADB_av_AEH48 = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/911/ADB48_CP402/scaled",
                 'p_archive': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/909/ADB39_CP402/scaled", #this is where the archive sends me
                 'p_victoria': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/909/ADB48_CP402/scaled"} 

pADB_av_AEH49 = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/913/ADB49_CP402/scaled",
                 'p_archive': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/911/ADB48_CP402/scaled", #this is where the archive sends me
                 'p_victoria': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/911/ADB49_CP402/scaled"} 

pADB_av_AEH58 = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/915/ADB58_CP402/scaled",
                 'p_archive': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/913/ADB49_CP402/scaled", #this is where the archive sends me
                 'p_victoria': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/913/ADB58_CP402/scaled"} 

pADB_av_AEH59 = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/917/ADB59_CP402/scaled",
                 'p_archive': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/915/ADB58_CP402/scaled", #this is where the archive sends me
                 'p_victoria': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/915/ADB59_CP402/scaled"} 


pADB_av_AEP18 = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/898/ADB18_CP202/scaled"} 

pADB_av_AEP19 = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/900/ADB19_CP202/scaled"} 

pADB_av_AEP28 = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/902/ADB28_CP202/scaled"} 

pADB_av_AEP29 = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/904/ADB29_CP202/scaled"} 

pADB_av_AEP38 = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/906/ADB38_CP202/scaled"} 

pADB_av_AEP39 = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/908/ADB39_CP202/scaled"} 

pADB_av_AEP48 = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/910/ADB48_CP202/scaled"} 

pADB_av_AEP49 = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/912/ADB49_CP202/scaled"} 

pADB_av_AEP58 = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/914/ADB58_CP202/scaled"} 

pADB_av_AEP59 = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/916/ADB59_CP202/scaled"} 

p_CP302 = {'p_ADB18': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/941/ADB18_CP302/scaled",
           'p_ADB29': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/943/ADB29_CP302/scaled",
           'p_ADB38': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/945/ADB38_CP302/scaled",
           'p_ADB49': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/947/ADB49_CP302/scaled",
           'p_ADBav': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/949/ADB_average_CP302/scaled"}


pADB_av_hpa = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/918/ADB_average_hpa/scaled"}

pADB_av_lpa = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/920/ADB_average_lpa/scaled"}

# whatever this is (Dirks Links)
pADB_av_CP301 = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/948/ADB_average_CP301/scaled"}

pADB_18_CP301 = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/940/ADB18_CP301/scaled"} #there are more for 29, 38, 49

pADB_18_KA201 = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/6/ADB18_KA201auf/scaled"}

pADB_18_KA301 = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/14/ADB18_KA301auf/scaled"}

pADB_18_KA401 = {'p': "ArchiveDB/codac/W7X/ControlStation.2068/PLC.1_DATASTREAM/18/ADB18_KA401auf/scaled"}


pBaratron = {'p': "ArchiveDB/raw/W7X/QRR_Residual_Gas_Analyzer/PVTotalPressureBaratron_DATASTREAM/V1/1/BaratronPressure",
             'p_raw': "ArchiveDB/raw/W7X/QRR_Residual_Gas_Analyzer/PVTotalPressureBaratron_DATASTREAM/V1/0/BaratronPressureRaw"}

url_gasValves = {'BG013H_V': "ArchiveDB/raw/W7X/ControlStation.2224/PiezoValveData_DATASTREAM/8/Actual Value Pressure Sensor Valve BG013",# "ArchiveDB/raw/W7X/ControlStation.2059/PiezoValveData_DATASTREAM/8/Actual Value Pressure Sensor Valve BG013",
                 'BG013H_flow': "ArchiveDB/raw/W7X/ControlStation.2224/PiezoValveData_DATASTREAM/15/Actual Value Flow Valve BG013",
                 'BG013H_p': "ArchiveDB/raw/W7X/ControlStation.2059/PLC.1_DATASTREAM/233/BG013CP01_IST",
                 'BG034He_V': "ArchiveDB/raw/W7X/ControlStation.2224/PiezoValveData_DATASTREAM/4/Actual Value Pressure Sensor Valve BG034",# "ArchiveDB/raw/W7X/ControlStation.2059/PiezoValveData_DATASTREAM/4/Actual Value Pressure Sensor Valve BG034",
                 'BG034He_flow': "ArchiveDB/raw/W7X/ControlStation.2224/PiezoValveData_DATASTREAM/19/Actual Value Flow Valve BG034",
                 'BG034He_p': "ArchiveDB/raw/W7X/ControlStation.2059/PLC.1_DATASTREAM/254/BG034CP01_IST"}


#date of calibration days from 12:00:00AM to 11:59:59PM
#w7xarchive.to_timestamp('YYYY-MM-DD:HH:MM:SS') to get nanosecond timestamp
calibration_dates = [#['2025-06-05 11:22:42', '2025-06-05 11:26:29'],
                     ['2025-06-05 00:00:00', '2025-06-05 23:59:59'],
                     #['2025-06-04 07:17:00', '2025-06-04 07:19:59'],
                     ['2025-06-04 00:00:00', '2025-06-04 23:59:59'],
                     #['2024-09-10 07:55:00', '2024-09-10 07:56:59'],#one spike
                     #['2024-09-10 11:59:00', '2024-09-10 12:01:29'],
                     #['2024-09-10 12:07:00', '2024-09-10 12:10:39'],
                     ['2024-09-10 00:00:00', '2024-09-10 23:59:59'],
                     #['2024-07-12 07:28:30', '2024-07-12 07:54:59'],
                     #['2024-07-12 08:02:00', '2024-07-12 08:28:09'],
                    
                     #['2024-07-12 08:53:00', '2024-07-12 08:56:59'],
                     #['2024-07-12 08:57:00', '2024-07-12 09:01:59'],#only spikes
                     #['2024-07-12 09:04:00', '2024-07-12 09:07:59'],
                     #['2024-07-12 09:10:00', '2024-07-12 09:12:59'],
                     
                     #['2024-07-12 09:15:00', '2024-07-12 09:35:00'],#blurry
                     #['2024-07-12 09:35:00', '2024-07-12 10:05:59'],
                     #['2024-07-12 11:17:00', '2024-07-12 12:02:59'],
                     #['2024-07-12 12:03:00', '2024-07-12 12:24:59'],
                     #['2024-07-12 00:00:00', '2024-07-12 23:59:59']
                     ]

#calibration days for earlier campagnes
calibration_datesOP21_1 = [['2023-04-04 00:00:00', '2023-04-04 23:59:59'],
                            ['2023-04-03 00:00:00', '2023-04-03 23:59:59'],
                            ['2022-12-13 00:00:00', '2022-12-13 23:59:59'],
                            ['2022-11-17 00:00:00', '2022-11-17 23:59:59'],
                            ['2018-10-10 00:00:00', '2018-10-10 23:59:59'],
                            ['2018-10-04 00:00:00', '2018-10-04 23:59:59'],
                            ['2018-10-02 00:00:00', '2018-10-02 23:59:59'],
                            ['2018-08-16 00:00:00', '2018-08-16 23:59:59'],
                            ['2018-07-03 00:00:00', '2018-07-03 23:59:59'],
                            ['2016-02-18 00:00:00', '2016-02-18 23:59:59']]

calibrations = [
                # OP2.2 first attempt, not ideal (slight pumping), do not use
                {"#": 0, "B": 2.5, "gas": "He", "program": "20240910.29", 'y': 35, 'inactive': ["AEH21"], },
                {"#": 1, "B": 2.5, "gas": "H2", "program": "20240910.30", 'y': 35, 'inactive': ["AEH21"], },
                # OP2.2 calibrations
                {"#": 2, "B": 2.5, "gas": "He", "program": "20240926.21", 'y': 0, 'inactive': ["AEH21", "AEH31"], 'config': {'AEI51': {'ignore_steps': []}}},
                {"#": 3, "B": 2.5, "gas": "H2", "program": "20240926.22", 'y': 0, 'inactive': ["AEH21", "AEH31"], },
                {"#": 4, "B": 2.5, "gas": "H2+He", "program": "20240926.23", 'y': 35, 'inactive': ["AEH21", "AEH31"], },
                # OP2.3 calibrations
                # low field calibration
                {"#": 5, "B": 1.8, "gas": "H2", "program": "20250218.40", 'y': 35, 'inactive': ["AEH21", "AEH11", "AEE50", "AEI51", "AEH31"], 'skip_steps': {'AEP51': [], 'AEP50': [17]}, "pref_correction_factor": 4.196051423324151},
                # normal calibrations (reversed field)
                {"#": 2, "B": 2.5, "gas": "H2", "program": "20250220.25", 'y': 35, 'inactive': ["AEH21", "AEH11", "AEE50", "AEI51", "AEH31"], 'skip_steps': {'AEP51': [], 'AEP50': [17]}, "pref_correction_factor": 4.1822773186409545},
                {"#": 3, "B": 2.5, "gas": "He", "program": "20250220.24", 'y': 35, 'inactive': ["AEH21", "AEH11", "AEE50", "AEI51", "AEH31"], 'skip_steps': {}, "pref_correction_factor": 4.313131313131313},
                # normal calibration (forward field)
                {"#": 4, "B": 2.5, "gas": "H2", "program": "20250604.1", 'y': 35, 'inactive': ["AEH21", "AEH11", "AEE50", "AEI51", "AEP50", "AEH31", "AEH30"], 'skip_steps': []},
                {"#": 5, "B": 2.5, "gas": "H2", "program": "20250605.43", 'y': 35, 'inactive': ["AEH21", "AEH11", "AEE50", "AEI51", "AEP50", "AEH31", "AEH30"], 'skip_steps': []}
                ]