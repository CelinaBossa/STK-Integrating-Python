## Para guardar el escenarios
# root.Save -----------------> (si esta cargado)
# root.SaveScenario ---------> (si no esta previamente guardado)
# root.CloseScenario

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
AntName                 = 'SAOCOMantenna'
ElvOptions              = [-65,-32.5,0,32.5,65]
Elv                     = ElvOptions[0]

#-------------------------------------------------------------------------------
################################## Funtions ##################################
# REPORTES
# single_report(Demodulation, Angle)
# report()
#
# SCENARIO
# change_time(InicialTime,FinalTime,StepTime)
#
# GROUND STATION
# new_GdSta(Name,Lat,Lon,Alt)
# setUseTerrainTrue(FacilityName)
#
# RECEPTOR
# setRecDemodulation(FacilityName,ReceptorName, Demodulation)
# setRecGainOverT(FacilityName,ReceptorName,GT)
#
# SATELLITE
# new_Satellite(SatelliteName,StepTime)
# boolean_AutoUpdateEnabled(SatelliteName,state)
# getAttAvailableRefAcex(SatelliteName)
# setAttReferenceAxes(SatelliteName,referece)
# setYPR(SatelliteName,Yaw,Pitch,Roll)
# setSaMass(SatelliteName,Mass):
#
# ANTENNA
# setDiameterAnt(SatelliteName, AntennaName, Diemater)
# setFrecuencyAnt(SatelliteName,AntennaName,Frecuency)
# setAzimuthElevation(SatelliteName,AntennaName,Azimuth,Elevation)
#
# TRANSMITTER
# new_Transmitter(SatelliteName,TransmitterName)
# setTraDemodulation(SatelliteName,TransmitterName, Demodulation):
# setTraFrecuency(SatelliteName,TransmitterName, Frecuency):
# setTraPower(SatelliteName,TransmitterName, Power)
# setTraDataRate(SatelliteName,TransmitterName, Data_Rate):
#-------------------------------------------------------------------------------

###############################################################################
##    Task 1
##    1. Set up your phyton workspace
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

######################################
##    Task 2
##    1. Create a new scenario

## !! SI SE DESEA CARGAR UN ESCENARIO PREVIO DEBE OBVIAR LA PROXIMA LINEA DE CÓDIGO
## Y EJECUTAR LA SIGUIENTE !!
## root.Load(r"Path")

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
POLARGdSta_FaObj.UseTerrain = False
POLARGdSta_FaObj.Position.AssignGeodetic(POLAR_GdStaLat, POLAR_GdStaLon, POLAR_GdStaAlt)


######################################
##    Task 4
##    1. Add a Receptor object to the facility

# CORDOBA'S RECEPTOR
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
#CBAprop_SGP4Obj.CommonTasks.AddSegsFromFile("46265",r"SAOCOM-1B-18-May.tle.txt")
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
SAOCOMant_STKObj        = SAOCOMsa_STKObj.Children.New(31, AntName)  # eAntenna
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
CBAtxModel_CmxModObj.Frequency = 20.2  # GHz
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
    if Demodulation == DemOptions[0]:
      DataRate = DataRateOptions[0]
    elif Demodulation == DemOptions[1]:
      DataRate = DataRateOptions[1]
    elif Demodulation ==  DemOptions[2]:
      DataRate = DataRateOptions[2]
    elif Demodulation ==  DemOptions[3]:
      DataRate = DataRateOptions[3]
    elif Demodulation ==  DemOptions[4]:
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
            accessAzimuth.append(round(Azimuth[j],3))
            accessElevation.append(round(Elevation[j],3))
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
            accessPropLoss.append(round(PropLoss[j],4))
            accessEIRP.append(round(EIRP[j],3))
            accessRcvdFrequency.append(round(RcvdFrequency[j],3))
            accessFreqDopplerShift.append(round(FreqDopplerShift[j],3))
            accessBandwidthOverlap.append(round(BandwidthOverlap[j],4))
            accessRcvdIsoPower.append(round(RcvdIsoPower[j],3))
            accessFluxDensity.append(round(FluxDensity[j],6))
            accessgT.append(round(gT[j],6))
            accessCNo.append(round(CNo[j],6))
            accessBandwidth.append(round(Bandwidth[j],3))
            accessCN.append(round(CN[j],4))
            accessSpectralFluxDensity.append(round(SpectralFluxDensity[j],6))
            accessEbNo.append(round(EbNo[j],4))
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
    
def change_time(InicialTime,FinalTime,StepTime):
  Sc_STKObj          = root.CurrentScenario
  Sc_ScObj           = Sc_STKObj.QueryInterface(STKObjects.IAgScenario)
  Sc_ScObj.SetTimePeriod(InicialTime,FinalTime)
  Sc_ScObj.Animation.AnimStepValue = StepTime
  root.Rewind();    


def new_GdSta(Name,Lat,Lon,Alt):
  GdSta_STKObj              = root.CurrentScenario.Children.New(8, Name)
  GdSta_FaObj               = GdSta_STKObj.QueryInterface(STKObjects.IAgFacility)
  root.UnitPreferences.Item('LatitudeUnit').SetCurrentUnit('deg')
  root.UnitPreferences.Item('LongitudeUnit').SetCurrentUnit('deg')
  GdSta_FaObj.UseTerrain    = False
  GdSta_FaObj.Position.AssignGeodetic(Lat, Lon, Alt)

def setUseTerrainTrue(FacilityName):
  GdSta_STKObj           = root.CurrentScenario.Children.Item(FacilityName) 
  GdSta_FaObj            = GdSta_STKObj.QueryInterface(STKObjects.IAgFacility)
  GdSta_FaObj.UseTerrain = 'True'

def setRecDemodulation(FacilityName,ReceptorName, Demodulation):
  GdSta_STKObj          = root.CurrentScenario.Children.Item(FacilityName) 
  Rec_STKObj            = GdSta_STKObj.Children.Item(ReceptorName)
  Rec_RecObj            = Rec_STKObj.QueryInterface(STKObjects.IAgReceiver)
  RecModel_ModObj       = Rec_RecObj.Model
  RecModel_SModObj      = RecModel_ModObj.QueryInterface(STKObjects.IAgReceiverModelSimple)
  RecModel_SModObj.AutoSelectDemodulator = False  
  RecModel_SModObj.SetDemodulator(Demodulation)
  print("Make sure you have change the Transmitter's Demodulation too")
  
def setRecGainOverT(FacilityName,ReceptorName,GT):
  GdSta_STKObj          = root.CurrentScenario.Children.Item(FacilityName) 
  Rec_STKObj            = GdSta_STKObj.Children.Item(ReceptorName)
  Rec_RecObj            = Rec_STKObj.QueryInterface(STKObjects.IAgReceiver)
  RecModel_ModObj       = Rec_RecObj.Model
  RecModel_SModObj      = RecModel_ModObj.QueryInterface(STKObjects.IAgReceiverModelSimple)
  RecModel_SModObj.GOverT  = GT #dB/K
  
def new_Satellite(SatelliteName,StepTime):
  Sa_STKObj      = root.CurrentScenario.Children.New(18, SatelliteName)  # eSatellite
  Sa_SaObj       = Sa_STKObj.QueryInterface(STKObjects.IAgSatellite)
  Sa_SaObj.SetPropagatorType(STKObjects.ePropagatorSGP4)
  Prop_PropObj       = Sa_SaObj.Propagator
  Prop_SGP4Obj       = Prop_PropObj.QueryInterface(STKObjects.IAgVePropagatorSGP4)
  Prop_SGP4Obj.EphemerisInterval.SetImplicitInterval(root.CurrentScenario.Vgt.EventIntervals.Item("AnalysisInterval"))  # Link to scenario period
  Prop_SGP4Obj.Step  = StepTime
  Prop_SGP4Obj.AutoUpdateEnabled = False
  Prop_SGP4Obj.Propagate()
  print("You can upload the TLE")
  
def boolean_AutoUpdateEnabled(SatelliteName,state):
  Sa_STKObj      = root.CurrentScenario.Children.Item(SatelliteName)
  Sa_SaObj       = Sa_STKObj.QueryInterface(STKObjects.IAgSatellite)
  Prop_PropObj       = Sa_SaObj.Propagator
  Prop_SGP4Obj       = Prop_PropObj.QueryInterface(STKObjects.IAgVePropagatorSGP4)
  Prop_SGP4Obj.AutoUpdateEnabled = state
  Prop_SGP4Obj.Propagate()
  
def getAttAvailableRefAcex(SatelliteName):
  Sa_STKObj      = root.CurrentScenario.Children.Item(SatelliteName)
  Sa_SaObj       = Sa_STKObj.QueryInterface(STKObjects.IAgSatellite)
  Att_AttObj          = Sa_SaObj.Attitude
  Att_OrbitAttStdObj  = Att_AttObj.QueryInterface(STKObjects.IAgVeOrbitAttitudeStandard)
  Att_BasicObj        = Att_OrbitAttStdObj.Basic
  Att_ProfObj         = Att_BasicObj.Profile
  Att_FIAObj          = Att_ProfObj.QueryInterface(STKObjects.IAgVeProfileFixedInAxes)
  return (Att_FIAObj.AvailableReferenceAxes)

def setAttReferenceAxes(SatelliteName,referece):
  Sa_STKObj      = root.CurrentScenario.Children.Item(SatelliteName)
  Sa_SaObj       = Sa_STKObj.QueryInterface(STKObjects.IAgSatellite)
  Att_AttObj          = Sa_SaObj.Attitude
  Att_OrbitAttStdObj  = Att_AttObj.QueryInterface(STKObjects.IAgVeOrbitAttitudeStandard)
  Att_BasicObj        = Att_OrbitAttStdObj.Basic
  Att_ProfObj         = Att_BasicObj.Profile
  Att_FIAObj          = Att_ProfObj.QueryInterface(STKObjects.IAgVeProfileFixedInAxes)
  Att_FIAObj.ReferenceAxes = referece
  
def setYPR(SatelliteName,Yaw,Pitch,Roll):
  Sa_STKObj           = root.CurrentScenario.Children.Item(SatelliteName)
  Sa_SaObj            = Sa_STKObj.QueryInterface(STKObjects.IAgSatellite)
  Att_AttObj          = Sa_SaObj.Attitude
  Att_OrbitAttStdObj  = Att_AttObj.QueryInterface(STKObjects.IAgVeOrbitAttitudeStandard)
  Att_BasicObj        = Att_OrbitAttStdObj.Basic
  Att_ProfObj         = Att_BasicObj.Profile
  Att_FIAObj          = Att_ProfObj.QueryInterface(STKObjects.IAgVeProfileFixedInAxes)
  Att_OrintObj        = Att_FIAObj.Orientation
  Att_OrintObj.AssignYPRAngles(4,Yaw,Pitch,Roll) #YPR sequence.
  
def setDiameterAnt(SatelliteName, AntennaName, Diemater):
  Sa_STKObj             = root.CurrentScenario.Children.Item(SatelliteName)
  Ant_STKObj            = Sa_STKObj.Children.Item(AntennaName)
  Ant_AntObj            = Ant_STKObj.QueryInterface(STKObjects.IAgAntenna)
  Ant_AntModObj         = Ant_AntObj.Model
  Ant_AntSABObj         = Ant_AntModObj.QueryInterface(STKObjects.IAgAntennaModelApertureCircularBessel)
  Ant_AntSABObj.Diameter = Diemater #m
  
def setFrecuencyAnt(SatelliteName,AntennaName,Frecuency):
  Sa_STKObj             = root.CurrentScenario.Children.Item(SatelliteName)
  Ant_STKObj            = Sa_STKObj.Children.Item(AntennaName)
  Ant_AntObj            = Ant_STKObj.QueryInterface(STKObjects.IAgAntenna)
  Ant_AntModObj     = Ant_AntObj.Model
  Ant_AntModObj.DesignFrequency = Frecuency #GHz
  
def setAzimuthElevation(SatelliteName,AntennaName,Azimuth,Elevation):
  Sa_STKObj             = root.CurrentScenario.Children.Item(SatelliteName)
  Ant_STKObj            = Sa_STKObj.Children.Item(AntennaName)
  Ant_AntObj            = Ant_STKObj.QueryInterface(STKObjects.IAgAntenna)
  Ant_OrintObj          = Ant_AntObj.Orientation
  Ant_OrintObj.AssignAzEl(Azimuth, Elevation, 1)  # 1 represents Rotate About Boresight
  #'Value 0° = 1.27222e-14 °'
  
def setSaMass(SatelliteName,Mass):
  Sa_STKObj             = root.CurrentScenario.Children.Item(SatelliteName)
  Sa_SaObj              = Sa_STKObj.QueryInterface(STKObjects.IAgSatellite)
  SaMass                = Sa_SaObj.MassProperties
  SaMass.Mass           = Mass  
  
def new_Transmitter(SatelliteName,TransmitterName):
  Sa_STKObj           = root.CurrentScenario.Children.Item(SatelliteName)
  Sa_STKObj.Children.New(24, TransmitterName)
  
def setTraDemodulation(SatelliteName,TransmitterName, Demodulation):
  Sa_STKObj             = root.CurrentScenario.Children.Item(SatelliteName)
  Tra_STKObj            = Sa_STKObj.Children.Item(TransmitterName)
  Tra_TraObj            = Tra_STKObj.QueryInterface(STKObjects.IAgTransmitter)
  TxModel_ModObj        = Tra_TraObj.Model
  TxModel_CmxModObj  = TxModel_ModObj.QueryInterface(STKObjects.IAgTransmitterModelComplex)
  TxModel_CmxModObj.SetModulator(Demodulation)
  if Demodulation == DemOptions[0]:
        DataRate = DataRateOptions[0]
  elif Demodulation == DemOptions[1]:
        DataRate = DataRateOptions[1]
  elif Demodulation ==  DemOptions[2]:
        DataRate = DataRateOptions[2]
  elif Demodulation ==  DemOptions[3]:
        DataRate = DataRateOptions[3]
  elif Demodulation ==  DemOptions[4]:
        DataRate = DataRateOptions[4]
  CBAtxModel_CmxModObj.DataRate = DataRate  # Mb/sec
  print("Make sure you have change the Receiver's Demodulation too")
  
def setTraFrecuency(SatelliteName,TransmitterName, Frecuency):
  Sa_STKObj             = root.CurrentScenario.Children.Item(SatelliteName)
  Tra_STKObj            = Sa_STKObj.Children.Item(TransmitterName)
  Tra_TraObj            = Tra_STKObj.QueryInterface(STKObjects.IAgTransmitter)
  TxModel_ModObj        = Tra_TraObj.Model
  TxModel_CmxModObj  = TxModel_ModObj.QueryInterface(STKObjects.IAgTransmitterModelComplex)
  TxModel_CmxModObj.Frequency = Frecuency # GHz
  
def setTraPower(SatelliteName,TransmitterName, Power):
  Sa_STKObj             = root.CurrentScenario.Children.Item(SatelliteName)
  Tra_STKObj            = Sa_STKObj.Children.Item(TransmitterName)
  Tra_TraObj            = Tra_STKObj.QueryInterface(STKObjects.IAgTransmitter)
  TxModel_ModObj        = Tra_TraObj.Model
  TxModel_CmxModObj  = TxModel_ModObj.QueryInterface(STKObjects.IAgTransmitterModelComplex)
  TxModel_CmxModObj.Power = Power # dBW
  
def setTraDataRate(SatelliteName,TransmitterName, Data_Rate):
  Sa_STKObj             = root.CurrentScenario.Children.Item(SatelliteName)
  Tra_STKObj            = Sa_STKObj.Children.Item(TransmitterName)
  Tra_TraObj            = Tra_STKObj.QueryInterface(STKObjects.IAgTransmitter)
  TxModel_ModObj        = Tra_TraObj.Model
  TxModel_CmxModObj  = TxModel_ModObj.QueryInterface(STKObjects.IAgTransmitterModelComplex)
  TxModel_CmxModObj.DataRate = Data_Rate # Mb/sec
  print("Make sure that you select the demodulation you want")
  
def getAccessTimeData(ReferenceObject, ObjectToAccess,element):
#  element = ['Start Time','Stop Time']
  access = CBArec_STKObj.GetAccessToObject(CBAtra_STKObj)
  access.ComputeAccess()
  AccessData            = access.DataProviders.Item('Access Data')
  AccessData_ProvG      = AccessData.QueryInterface(STKObjects.IAgDataPrvInterval)
  AccessData_results    = AccessData_ProvG.Exec(scenario_ScObj.StartTime, scenario_ScObj.StopTime)
  accessTime            = AccessData_results.DataSets.GetDataSetByName(element).GetValues()
  return accessTime

def getTmData(ReferenceObject, ObjectToAccess,ItemName,GroupName,StartTime,StopTime,StepTime,element):
  access = ReferenceObject.GetAccessToObject(ObjectToAccess)
  access.ComputeAccess()
  Item              = access.DataProviders.Item(ItemName)
  if GroupName != None:
    GroupObj    = Item.QueryInterface(STKObjects.IAgDataProviderGroup)
    DataObj     = GroupObj.Group
    Item  = DataObj.Item(GroupName)
  TimeVar           = Item.QueryInterface(STKObjects.IAgDataPrvTimeVar)
  Elements          = [element]
  Results           = TimeVar.ExecElements(StartTime,StopTime,StepTime,Elements)
  Data              = list(Results.DataSets.GetDataSetByName(element).GetValues())
  return Data

def getTmIntervals(ReferenceObject, ObjectToAccess,StartTime,StopTime,StepTime):
  Time = getTmData(ReferenceObject,ObjectToAccess,'AER Data','Default',StartTime,StopTime,StepTime,'Time')
  return Time

def getTmRealData(ReferenceObject, ObjectToAccess,ItemName,GroupName,StartTime,StopTime,StepTime,elements):
  DataList = []
  for i in range(len(elements)):
    element = elements[i]
    Data = getTmData(ReferenceObject, ObjectToAccess,ItemName,GroupName,StartTime,StopTime,StepTime,element)
    TmREalData = round(Data[0],3)
    DataList.append(TmREalData)
  return DataList

def getStaticData(ReferenceObject,ItemName,GroupName,element):
  Item                  = ReferenceObject.DataProviders.Item(ItemName)
  if GroupName != None:
    GroupObj    = Item.QueryInterface(STKObjects.IAgDataProviderGroup)
    DataObj     = GroupObj.Group
    Item        = DataObj.Item(GroupName)
  DataPrvFixed          = Item.QueryInterface(STKObjects.IAgDataPrvFixed)
  Elements              = [element]
  Results               = DataPrvFixed.ExecElements(Elements)
  Data                  = list(Results.DataSets.GetDataSetByName(element).GetValues())
  return Data

def Step(ReferenceObject, ObjectToAccess,ItemNameList,GroupNameList,StartTime,StopTime,
         StepTime,elementsList,SatelliteName,TransmitterName,FacilityName,
         ReceptorName,AntennaName,Demodulation,Angle,Azimuth):
  setAzimuthElevation(SatelliteName,AntennaName,Azimuth,Angle) #Cambio angulo
  setTraDemodulation(SatelliteName,TransmitterName, Demodulation)
  setRecDemodulation(FacilityName,ReceptorName, Demodulation)
  Data = []
  for i in range(len(ItemNameList)):
    ItemName = ItemNameList[i]
    GroupName = GroupNameList[i]
    elements = elementsList[i]
    DataList = getTmRealData(ReferenceObject, ObjectToAccess,ItemName,GroupName,StartTime,StopTime,StepTime,elements)
    for j in range(len(DataList)):
      Data.append(DataList[j])
  return Data

##Obtengo los accesos
#accessStartTime = getAccessTimeData(CBArec_STKObj,CBAtra_STKObj,'Start Time')
#accessStopTime = getAccessTimeData(CBArec_STKObj,CBAtra_STKObj,'Stop Time')
#
##Muestro que valores tiene en la primer columna
#print(accessStartTime[0])
#print(accessStopTime[0])
#
##Obtengo los tiempos de los accesos para (por ejemplo) 8PSK 0°
#Demodulacion = '8PSK'
#Angulo = 0
#Tiempo = getTmIntervals(CBArec_STKObj,CBAtra_STKObj,accessStartTime[0],accessStopTime[0],StepTm)
#
##Muestro que valores tiene Tiempo
#print(Tiempo[0])
#print(Tiempo[1])
#print(Tiempo[2])
#print(Tiempo[3])
#
##Defino los datos que voy a quere sacar
#Item = ['AER Data','To Position Velocity']
#Group = ['Default','ICRF']
#elements = [['Access Number','Azimuth','Elevation','Range'],['x', 'y', 'z', 'xVel', 'yVel', 'zVel', 'RelSpeed']]
#
##Defino una variable contador para que sea más facil iterar
#aux = 0
#
##Obtengo datos del primer step
#Step(CBArec_STKObj,CBAtra_STKObj,Item,Group,Tiempo[aux],Tiempo[aux+1],StepTm,elements,SaName,TraName,CBA_GdStaName,CBA_RecName,AntName,Demodulacion,Angulo,0)
#
##Cambio democulacion
#Demodulacion = 'QAM16'
#Angulo = 0
#
##Incremento contador 
#aux = aux+1
#
##Obtengo segundo step
#Step(CBArec_STKObj,CBAtra_STKObj,Item,Group,Tiempo[aux],Tiempo[aux+1],StepTm,elements,SaName,TraName,CBA_GdStaName,CBA_RecName,AntName,Demodulacion,Angulo,0)
#
##Cambio democulacion y ángulo
#Demodulacion = 'QPSK'
#Angulo = -65
#
##Incremento contador 
#aux = aux+1
#
##Obtengo tercer step
#Step(CBArec_STKObj,CBAtra_STKObj,Item,Group,Tiempo[aux],Tiempo[aux+1],StepTm,elements,SaName,TraName,CBA_GdStaName,CBA_RecName,AntName,Demodulacion,Angulo,0)
