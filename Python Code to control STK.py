### Set the variables

#   Scenrio Properties
ScName                  = 'Paper'
InicialTm               =  '18 May 2022 09:21:00.000'
FinalTm                 = '3 Jun 2022 23:32:30.830'
StepTm                  = 8

#   Ground Starion Properties
CBA_GdStaName           = 'CordBS'
CBA_GdStaLat            = -31.4343
CBA_GdStaLon            = -64.2672
CBA_GdStaAlt            = 0
POLAR_GdStaName         = 'polarBS'
POLAR_GdStaLat          = -90
POLAR_GdStaLon          = -90
POLAR_GdStaAlt          = 0


#   Receptor Properties
CBA_RecName             = 'Receiver2'
RecType                 = 'Simple Receiver Model'
POLAR_RecName           = 'Receiver3'

#   Transmitter Propieties
TraName                 = 'Transmitter2'

#Satellite
SaName                  = 'Saocom-1-B'

#Demodulation
DemOptions              = ['QPSK','8PSK','16PSK','QAM16','QAM32']
Dem                     = DemOptions[0]

#Data Rare
DataRateOptions         = [2,3,4,4,5]
DataRate                = DataRateOptions[0] 

#   Antenna Properties
XantPosition            = 50
YantPosition            = -100
ZantPosition            = 0
ElvOptions              = [-65,-32.5,0,32.5,65]
Elv                     = ElvOptions[0]

#-------------------------------------------------------------------------------
#Funtions
#X
#X
#X
#X
#-------------------------------------------------------------------------------

###############################################################################
##    Task 1
##    1. Set up your phyton workspace
from win32api import GetSystemMetrics
from comtypes.client import CreateObject

##    2. Get reference to running STK instance
uiApplication = CreateObject('STK11.Application')
uiApplication.Visible = True
uiApplication.UsarControl=True

##    3. Get our IAgStkObjectRoot interface
root = uiApplication.Personality2

# Note: When 'root=uiApplication.Personality2' is executed, the comtypes library automatically creates a gen folder that contains STKUtil and STK Objects. 
# After running this at least once on your computer, the following two lines should be moved before the 'uiApplication=CreateObject("STK12.Application")'
# line for improved performance. 

from comtypes.gen import STKObjects
from comtypes.gen import STKUtil

######################################
##    Task 2
##    1. Create a new scenario

root.NewScenario(ScName)
scenario_STKObj          = root.CurrentScenario

##    2. Set the analytical time period.

scenario_ScObj         = scenario_STKObj.QueryInterface(STKObjects.IAgScenario)
scenario_ScObj.SetTimePeriod(InicialTm,FinalTm)
scenario_ScObj.Animation.AnimStepValue = StepTm

##    3. Reset the animation time.
root.Rewind();



######################################
##    Task 3
##    1. Add a facility object to the scenario

## CORDOBA'S GROUND STATION
CBAGdSta_STKObj     = root.CurrentScenario.Children.New(8, CBA_GdStaName)
CBAGdSta_FaObj    = CBAGdSta_STKObj.QueryInterface(STKObjects.IAgFacility)
root.UnitPreferences.Item('LatitudeUnit').SetCurrentUnit('deg')
root.UnitPreferences.Item('LongitudeUnit').SetCurrentUnit('deg')
CBAGdSta_FaObj.UseTerrain = False #buscar el help -> Opt whether to set altitude automatically by using terrain data.
CBAGdSta_FaObj.Position.AssignGeodetic(CBA_GdStaLat, CBA_GdStaLon, CBA_GdStaAlt)

## POLAR'S GROUND STATION
POLARGdSta_STKObj = root.CurrentScenario.Children.New(8, POLAR_GdStaName)
POLARGdSta_FaObj = POLARGdSta_STKObj.QueryInterface(STKObjects.IAgFacility)
root.UnitPreferences.Item('LatitudeUnit').SetCurrentUnit('deg')
root.UnitPreferences.Item('LongitudeUnit').SetCurrentUnit('deg')
POLARGdSta_FaObj.UseTerrain = True
POLARGdSta_FaObj.Position.AssignGeodetic(POLAR_GdStaLat, POLAR_GdStaLon, POLAR_GdStaAlt)


######################################
##    Task 4
##    1. Add a Receptor object to the facility

# CORDOBA'S RECEPTOR (cambiar nombre)
CBArec_STKObj          = CBAGdSta_STKObj.Children.New(17, CBA_RecName)  # eReceiver
CBArec_RecObj          = CBArec_STKObj.QueryInterface(STKObjects.IAgReceiver)
# POLAR'S RECEPTOR
POLARrec_STKObj        = POLARGdSta_STKObj.Children.New(17, POLAR_RecName)  # eReceiver
POLARrec_RecObj        = POLARrec_STKObj.QueryInterface(STKObjects.IAgReceiver)

# Modify Receiver Type
CBArec_RecObj.SetModel(RecType) #CORDOBA
POLARrec_RecObj.SetModel(RecType) #POLAR

# Modify Receiver Demodulator Properties
# CORDOBA'S RECEPTOR
CBArecModel_ModObj          = CBArec_RecObj.Model
CBArecModel_SModObj         = CBArecModel_ModObj.QueryInterface(STKObjects.IAgReceiverModelSimple)
CBArecModel_SModObj.AutoSelectDemodulator = False  
CBArecModel_SModObj.SetDemodulator(Dem) 
CBArecModel_SModObj.GOverT  = 24.83 #dB/K 

# POLAR'S RECEPTOR    
POLARrecModel_ModObj        = POLARrec_RecObj.Model
POLARrecModel_SModObj       = POLARrecModel_ModObj.QueryInterface(STKObjects.IAgReceiverModelSimple)
POLARrecModel_SModObj.AutoSelectDemodulator = False  
POLARrecModel_SModObj.SetDemodulator(Dem)  
POLARrecModel_SModObj.GOverT = 24.83 #dB/K 

######################################
##    Task 5
##    1. Add a Satellite object to the scenario

SAOCOMsa_STKObj      = root.CurrentScenario.Children.New(18, SaName)  # eSatellite
SAOCOMsa_SaObj       = SAOCOMsa_STKObj.QueryInterface(STKObjects.IAgSatellite)
SAOCOMsa_SaObj.SetPropagatorType(STKObjects.ePropagatorSGP4)

# Set satellite propagator to SGP4 and propagate
#satellite2.SetPropagatorType(4)  # ePropagatorSGP4
CBAprop_PropObj       = SAOCOMsa_SaObj.Propagator
CBAprop_SGP4Obj       = CBAprop_PropObj.QueryInterface(STKObjects.IAgVePropagatorSGP4)
CBAprop_SGP4Obj.EphemerisInterval.SetImplicitInterval(root.CurrentScenario.Vgt.EventIntervals.Item("AnalysisInterval"))  # Link to scenario period
CBAprop_SGP4Obj.Step  = StepTm
CBAprop_SGP4Obj.AutoUpdateEnabled = False

#CBApropagator_SGP4Obj.AutoUpdate.SelectedSource = 2
#CBApropagator_SGP4Obj.CommonTasks.AddSegsFromFile("46265","SAOCOM-1B.tle.txt")
#|-> COMError: (-2147220989, 'Error de sintaxis al tratar de evaluar una cadena de consulta', 
#('Cannot open file: SAOCOM-1B.tle.txt.', None, None, 0, None))

#La siguiente linea no es necesaria ejecutarla porque al poner False ya la configura en 3
#CBApropagator_SGP4Obj.AutoUpdate.SelectedSource = 3
#
#CBApropagator_SGP4AutoU.FileSource.Filename('SAOCOM-1B.tle')
#CBApropagator_SGP4Obj.CommonTasks.AddSegsFromOnlineSource('46265')  # Cambiar a TLE
#CBApropagator_SGP4Obj.CommonTasks.AddSegsFromFile("0","SAOCOM-1B")
#CBApropagator_SGP4Obj.AutoUpdate.FileSource.Filename('SAOCOM-1B.tle')
CBAprop_SGP4Obj.Propagate()

#Set satellite attitude basic spinning ## me lo va a dar el TLE
CBAatt_AttObj          = SAOCOMsa_SaObj.Attitude
CBAatt_OrbitAttStdObj  = CBAatt_AttObj.QueryInterface(STKObjects.IAgVeOrbitAttitudeStandard)
CBAatt_BasicObj        = CBAatt_OrbitAttStdObj.Basic
CBAatt_BasicObj.SetProfileType(6)
CBAatt_ProfObj         = CBAatt_BasicObj.Profile
CBAatt_FIAObj          = CBAatt_ProfObj.QueryInterface(STKObjects.IAgVeProfileFixedInAxes)
CBAatt_FIAObj.ReferenceAxes = 'Satellite/Saocom-1-B LVLH(Earth)'
CBAatt_OrintObj        = CBAatt_FIAObj.Orientation
CBAatt_OrintObj.AssignYPRAngles(4,-180,0,-90) #YPR sequence.


##    2. Add and Set the antenna object
SAOCOMant_STKObj        = SAOCOMsa_STKObj.Children.New(31, 'SAOCOMantenna')  # eAntenna
SAOCOMant_AntObj        = SAOCOMant_STKObj.QueryInterface(STKObjects.IAgAntenna)
SAOCOMant_AntObj.SetModel('Bessel Aperture Circular')
SAOCOMant_AntModObj     = SAOCOMant_AntObj.Model
SAOCOMant_AntSABObj     = SAOCOMant_AntModObj.QueryInterface(STKObjects.IAgAntennaModelApertureCircularBessel)
SAOCOMant_AntSABObj.Diameter = 0.5 #m
SAOCOMant_AntSABObj.ComputeMainlobeGain = False
SAOCOMant_AntModObj.DesignFrequency = 2.255 #GHz la f que pongo acá es la misma que va en la linea 183
SAOCOMant_OrintObj      = SAOCOMant_AntObj.Orientation
SAOCOMant_OrintObj.AssignAzEl(0, Elv, 1)  # 1 represents Rotate About Boresight
#'Value 0° = 1.27222e-14 °'

##    3. Add a Transmiter object to the satellite
CBAtra_STKObj       = SAOCOMsa_STKObj.Children.New(24, TraName)  # eTransmitter
CBAtra_TraObj       = CBAtra_STKObj.QueryInterface(STKObjects.IAgTransmitter)


# Modify Transmitter Modulator Properties
CBAtra_TraObj.SetModel('Complex Transmitter Model')
CBAtxModel_ModObj           = CBAtra_TraObj.Model
CBAtxModel_CmxModObj        = CBAtxModel_ModObj.QueryInterface(STKObjects.IAgTransmitterModelComplex)
CBAtxModel_CmxModObj.SetModulator(Dem)
CBAtxModel_CmxModObj.Modulator.AutoScaleBandwidth = True
CBAtxModel_CmxModObj.Frequency = 2.255  # GHz
CBAtxModel_CmxModObj.Power  = -14  # dBW
CBAtxModel_CmxModObj.DataRate = DataRate  # Mb/sec
CBAtxModel_CmxModObj.AntennaControl.ReferenceType = 0  #Link to an Antenna object
CBAtxModel_CmxModObj.AntennaControl.LinkedAntennaObject


#Modifico masa a satellite
#'Value 0 kg is invalid. Value range is 0.00100000 kg to 1000000000.00000000 kg'
SAOCOMmass                  = SAOCOMsa_SaObj.MassProperties
SAOCOMmass.Mass             = 0.00100000

print('The Configuration is Done. Please upload the TLE')

def report():
    for modulation in range(len(DemOptions)):
        for angle in range(len(ElvOptions)):
            single_report(DemOptions[modulation],ElvOptions[angle])
    print('Done')
    
def single_report(Demodulation, Angle):
    Dem = Demodulation
    Elv = Angle
    'QPSK','8PSK','16PSK','QAM16','QAM32'
    if Demodulation == 'QPSK':
        DataRate = DataRateOptions[0]
    elif Demodulation == '8PSK':
        DataRate = DataRateOptions[1]
    elif Demodulation ==  '16PSK':
        DataRate = DataRateOptions[2]
    elif Demodulation ==  'QAM16':
        DataRate = DataRateOptions[3]
    elif Demodulation ==  'QAM32':
        DataRate = DataRateOptions[4]
    CBArecModel_SModObj.SetDemodulator(Dem)
    POLARrecModel_SModObj.SetDemodulator(Dem)
    CBAtxModel_CmxModObj.DataRate = DataRate  # Mb/sec
    SAOCOMant_OrintObj.AssignAzEl(0, Elv, 1)
    CBAtxModel_CmxModObj.SetModulator(Dem)
    access = CBArec_STKObj.GetAccessToObject(CBAtra_STKObj)
    access.ComputeAccess()
    AccessData        = access.DataProviders.Item('Access Data')
    AccessData_ProvG  = AccessData.QueryInterface(STKObjects.IAgDataPrvInterval)
    AccessData_results         = AccessData_ProvG.Exec(scenario_ScObj.StartTime, scenario_ScObj.StopTime)
    accessStartTime = AccessData_results.DataSets.GetDataSetByName('Start Time').GetValues()
    accessStopTime  = AccessData_results.DataSets.GetDataSetByName('Stop Time').GetValues()
    #print(accessStartTime, accessStopTime)
       
     ######################################
    ##    Task 7
    ##    1. Retrive and view the altitud of the satellite during an access interval.
        
    ##Data provider de AER Data -> Default -> Azimuth - Elevation - Range
    AERdata                 = access.DataProviders.Item('AER Data')
    AERdata_GroupObj        = AERdata.QueryInterface(STKObjects.IAgDataProviderGroup)
    AERdata_DataObj         = AERdata_GroupObj.Group
    AERdata_Default         = AERdata_DataObj.Item('Default')
    AERdata_TimeVar         = AERdata_Default.QueryInterface(STKObjects.IAgDataPrvTimeVar)
    AERdata_elements        = ['Access Number', 'Time', 'Azimuth', 'Elevation', 'Range']
    accessTime              = []
    accessAccessNumber      = []
    accessAzimuth           = []
    accessElevation         = []
    accessRange             = []
    for i in range(len(accessStartTime)): 
        AERdata_results         = AERdata_TimeVar.ExecElements(accessStartTime[i],accessStopTime[i],StepTm,AERdata_elements)
        Time = list(AERdata_results.DataSets.GetDataSetByName('Time').GetValues())
        AccessNumber = list(AERdata_results.DataSets.GetDataSetByName('Access Number').GetValues())
        Azimuth = list(AERdata_results.DataSets.GetDataSetByName('Azimuth').GetValues())
        Elevation = list(AERdata_results.DataSets.GetDataSetByName('Elevation').GetValues())
        Range = list(AERdata_results.DataSets.GetDataSetByName('Range').GetValues())
        for j in range (len(AccessNumber)):
            accessTime.append(Time[j])
            accessAccessNumber.append(AccessNumber[j])
            accessAzimuth.append(round(Azimuth[j],6))
            accessElevation.append(round(Elevation[j],6))
            accessRange.append(round(Range[j],6))   
            
    ##Data provider de To Position Velocity -> ICRF -> x - y - z - xVel - yVel - zVel - RelSpeed
    ToPositionVel           = access.DataProviders.Item('To Position Velocity')
    ToPositionVel_GroupObj  = ToPositionVel.QueryInterface(STKObjects.IAgDataProviderGroup)
    ToPositionVel_DataObj   = ToPositionVel_GroupObj.Group
    ToPositionVel_ICRF      = ToPositionVel_DataObj.Item('ICRF')
    ToPositionVel_TimeVar   = ToPositionVel_ICRF.QueryInterface(STKObjects.IAgDataPrvTimeVar)
    ToPositionVel_elements  = ['x', 'y', 'z', 'xVel', 'yVel', 'zVel', 'RelSpeed']
    accessX                 = []
    accessY                 = []
    accessZ                 = []
    accessXVel              = []
    accessYVel              = []
    accessZVel              = []
    accessRelSpeed          = []
    for i in range(len(accessStartTime)): 
        ToPositionVel_results   = ToPositionVel_TimeVar.ExecElements(accessStartTime[i],accessStopTime[i],StepTm,ToPositionVel_elements)
        X = list(ToPositionVel_results.DataSets.GetDataSetByName('x').GetValues())
        Y = list(ToPositionVel_results.DataSets.GetDataSetByName('y').GetValues())
        Z = list(ToPositionVel_results.DataSets.GetDataSetByName('z').GetValues())
        XVel = list(ToPositionVel_results.DataSets.GetDataSetByName('xVel').GetValues())
        YVel = list(ToPositionVel_results.DataSets.GetDataSetByName('yVel').GetValues())
        ZVel = list(ToPositionVel_results.DataSets.GetDataSetByName('zVel').GetValues())
        RelSpeed = (ToPositionVel_results.DataSets.GetDataSetByName('RelSpeed').GetValues())
        for j in range(len(X)):
            accessX.append(round(X[j],6))
            accessY.append(round(Y[j],6))
            accessZ.append(round(Z[j],6))
            accessXVel.append(round(XVel[j],6))
            accessYVel.append(round(YVel[j],6))
            accessZVel.append(round(ZVel[j],6))
            accessRelSpeed.append(round(RelSpeed[j],6))  
            
    ##Data provider de Link Information -> Prop Loss - EIRP - Rcvd. Frequency - Freq. Doppler Shift -
    #                                       - Bandwidth Overlap - Rcvd. Iso. Power - Flux Density -
    #                                       - g/T - C/No - Bandwidth - C/N - Spectral Flux Density -
    #                                       - Eb/No - BER
    LinkInfo                = access.DataProviders.Item('Link Information')
    LinkInfo_TimeVar        = LinkInfo.QueryInterface(STKObjects.IAgDataPrvTimeVar)
    LinkInfo_elements       = ['Prop Loss', 'EIRP', 'Rcvd. Frequency', 'Freq. Doppler Shift', 'Bandwidth Overlap','Rcvd. Iso. Power', 'Flux Density', 'g/T', 'C/No', 'Bandwidth', 'C/N', 'Spectral Flux Density', 'Eb/No','BER']
    accessPropLoss          = []
    accessEIRP              = []
    accessRcvdFrequency     = []
    accessFreqDopplerShift  = []
    accessBandwidthOverlap  = []
    accessRcvdIsoPower      = []
    accessFluxDensity       = []
    accessgT                = []
    accessCNo               = []
    accessBandwidth         = []
    accessCN                = []
    accessSpectralFluxDensity = []
    accessEbNo              = []
    accessBER               = []
    for i in range(len(accessStartTime)):
        LinkInfo_results        = LinkInfo_TimeVar.ExecElements(accessStartTime[i],accessStopTime[i],StepTm,LinkInfo_elements)
        PropLoss = list(LinkInfo_results.DataSets.GetDataSetByName('Prop Loss').GetValues())
        EIRP = list(LinkInfo_results.DataSets.GetDataSetByName('EIRP').GetValues())
        RcvdFrequency = list(LinkInfo_results.DataSets.GetDataSetByName('Rcvd. Frequency').GetValues())
        FreqDopplerShift = list(LinkInfo_results.DataSets.GetDataSetByName('Freq. Doppler Shift').GetValues())
        BandwidthOverlap = list(LinkInfo_results.DataSets.GetDataSetByName('Bandwidth Overlap').GetValues())
        RcvdIsoPower = list(LinkInfo_results.DataSets.GetDataSetByName('Rcvd. Iso. Power').GetValues())
        FluxDensity = list(LinkInfo_results.DataSets.GetDataSetByName('Flux Density').GetValues())
        gT = list(LinkInfo_results.DataSets.GetDataSetByName('g/T').GetValues())
        CNo = list(LinkInfo_results.DataSets.GetDataSetByName('C/No').GetValues())
        Bandwidth = list(LinkInfo_results.DataSets.GetDataSetByName('Bandwidth').GetValues())
        CN = list(LinkInfo_results.DataSets.GetDataSetByName('C/N').GetValues())
        SpectralFluxDensity = list(LinkInfo_results.DataSets.GetDataSetByName('Spectral Flux Density').GetValues())
        EbNo = list(LinkInfo_results.DataSets.GetDataSetByName('Eb/No').GetValues())
        BER = list(LinkInfo_results.DataSets.GetDataSetByName('BER').GetValues())
        for j in range (len(BER)):
            accessPropLoss.append(round(PropLoss[j],6))
            accessEIRP.append(round(EIRP[j],6))
            accessRcvdFrequency.append(round(RcvdFrequency[j],6))
            accessFreqDopplerShift.append(round(FreqDopplerShift[j],6))
            accessBandwidthOverlap.append(round(BandwidthOverlap[j],6))
            accessRcvdIsoPower.append(round(RcvdIsoPower[j],6))
            accessFluxDensity.append(round(FluxDensity[j],6))
            accessgT.append(round(gT[j],6))
            accessCNo.append(round(CNo[j],6))
            accessBandwidth.append(round(Bandwidth[j],6))
            accessCN.append(round(CN[j],6))
            accessSpectralFluxDensity.append(round(SpectralFluxDensity[j],6))
            accessEbNo.append(round(EbNo[j],6))
            accessBER.append(round(BER[j],6))
            
    accessModulation        = []
    accessAntAngle          = []
    for i in range(len(accessTime)):
        accessModulation.append(Dem)
        accessAntAngle.append(str(Elv))  
        
    import pandas as pd
    tabla = {
            	   "Access Number": accessAccessNumber,
            	   'Time (UTCG)': accessTime,
                   'Modulation': accessModulation,
                   'Angulo Antenna' : accessAntAngle,
            	   'Azimuth (deg)': accessAzimuth,
                   'Elevation (deg)': accessElevation,
            	   'Range (km)': accessRange,
                   'x (km)': accessX,
                   'y (km)': accessY,
                   'z (km)': accessZ,
                   'xVel (km/sec)': accessXVel,
                   'yVel (km/sec)': accessYVel,
                   'zVel (km/sec)': accessZVel,
                   'RelSpeed (km/sec)': accessRelSpeed,
                   'Prop Loss (dB)': accessPropLoss,
                   'EIRP (dBW)': accessEIRP,
                   'Rcvd. Frequency (GHz)': accessRcvdFrequency,
                   'Freq. Doppler Shift (GHz)': accessFreqDopplerShift,
                   'Bandwidth Overlap (dB)': accessBandwidthOverlap,
                   'Rcvd. Iso. Power (dBW)': accessRcvdIsoPower,
                   'Flux Density (dBW/m^2)': accessFluxDensity,
                   'g/T (dB/K)': accessgT,
                   'C/No (dB*MHz)': accessCNo,
                   'Bandwidth (MHz)': accessBandwidth,
                   'C/N (dB)': accessCN,
                   'Spectral Flux Density (dBW*m^-2*Hz^-1)': accessSpectralFluxDensity,
                   'Eb/No (dB)': accessEbNo,
                   'BER': accessBER,          
    }
    
    reporte = pd.DataFrame(tabla)
    reporte.to_csv("Reporte_"+Dem+"_"+str(Elv)+".csv")
    reporte.to_excel("Reporte_"+Dem+"_"+str(Elv)+".xlsx")
   
