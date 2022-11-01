### Set the variables

#   Scenrio Properties
ScenarioName  = 'Paper'
InicialTime   =  '05 Jul 2022 00:00:00.000'
FinalTime     = '23 Jul 2022 00:00:00.000'
StepTime      = 8

#   Ground Starion Properties
CBA_GroundStationName   = 'CordBS'
CBA_GroundStationLatitude = -31.4343
CBA_GroundStationLongitude = -64.2672
CBA_GroundStationAltitude = 0
POLAR_GroundStationName   = 'polarBS'
POLAR_GroundStationLatitude = -90
POLAR_GroundStationLongitude = -90
POLAR_GroundStationAltitude = 0


#   Receptor Properties
CBA_ReceiverName = 'Receiver2'
ReciverType = 'Simple Receiver Model'
POLAR_ReceiverName = 'Receiver3'

#   Transmitter Propieties
TransmitterName = 'Transmitter2'

#Satellite
SatelliteName = 'Saocom-1-B-Julio'

#Demodulation
Dem = '16PSK'

#   Antenna Properties
XantPosition  = 50
YantPosition  = -100
ZantPosition  = 0

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

root.NewScenario(ScenarioName)
scenario_STKObj          = root.CurrentScenario

##    2. Set the analytical time period.

scenario_ScenObj         = scenario_STKObj.QueryInterface(STKObjects.IAgScenario)
scenario_ScenObj.SetTimePeriod(InicialTime,FinalTime)
scenario_ScenObj.Animation.AnimStepValue = StepTime

##    3. Reset the animation time.
root.Rewind();



######################################
##    Task 3
##    1. Add a facility object to the scenario

## CORDOBA'S GROUND STATION
CBAgroundStation_STKObj     = root.CurrentScenario.Children.New(8, CBA_GroundStationName)
CBAgroundStation_FaciObj    = CBAgroundStation_STKObj.QueryInterface(STKObjects.IAgFacility)
root.UnitPreferences.Item('LatitudeUnit').SetCurrentUnit('deg')
root.UnitPreferences.Item('LongitudeUnit').SetCurrentUnit('deg')
CBAgroundStation_FaciObj.UseTerrain = False #buscar el help -> Opt whether to set altitude automatically by using terrain data.
CBAgroundStation_FaciObj.Position.AssignGeodetic(CBA_GroundStationLatitude, CBA_GroundStationLongitude, CBA_GroundStationAltitude)

## POLAR'S GROUND STATION
POLARgroundStation_STKObj = root.CurrentScenario.Children.New(8, POLAR_GroundStationName)
POLARgroundStation_FaciObj = POLARgroundStation_STKObj.QueryInterface(STKObjects.IAgFacility)
root.UnitPreferences.Item('LatitudeUnit').SetCurrentUnit('deg')
root.UnitPreferences.Item('LongitudeUnit').SetCurrentUnit('deg')
POLARgroundStation_FaciObj.UseTerrain = False
POLARgroundStation_FaciObj.Position.AssignGeodetic(POLAR_GroundStationLatitude, POLAR_GroundStationLongitude, POLAR_GroundStationAltitude)


######################################
##    Task 4
##    1. Add a Receptor object to the facility

# CORDOBA'S RECEPTOR (cambiar nombre)
CBAreceiver_STKObj          = CBAgroundStation_STKObj.Children.New(17, CBA_ReceiverName)  # eReceiver
CBAreceiver_RecObj          = CBAreceiver_STKObj.QueryInterface(STKObjects.IAgReceiver)
# POLAR'S RECEPTOR
POLARreceiver_STKObj        = POLARgroundStation_STKObj.Children.New(17, POLAR_ReceiverName)  # eReceiver
POLARreceiver_RecObj        = POLARreceiver_STKObj.QueryInterface(STKObjects.IAgReceiver)

# Modify Receiver Type
CBAreceiver_RecObj.SetModel(ReciverType) #CORDOBA
POLARreceiver_RecObj.SetModel(ReciverType) #POLAR

# Modify Receiver Demodulator Properties
# CORDOBA'S RECEPTOR
CBArecModel_ModObj          = CBAreceiver_RecObj.Model
CBArecModel_SModObj         = CBArecModel_ModObj.QueryInterface(STKObjects.IAgReceiverModelSimple)
CBArecModel_SModObj.AutoSelectDemodulator = False  
CBArecModel_SModObj.SetDemodulator(Dem) 
CBArecModel_SModObj.GOverT  = 24.83 #dB/K 

# POLAR'S RECEPTOR    
POLARrecModel_ModObj        = POLARreceiver_RecObj.Model
POLARrecModel_SModObj       = POLARrecModel_ModObj.QueryInterface(STKObjects.IAgReceiverModelSimple)
POLARrecModel_SModObj.AutoSelectDemodulator = False  
POLARrecModel_SModObj.SetDemodulator(Dem)  
POLARrecModel_SModObj.GOverT = 24.83 #dB/K 

######################################
##    Task 5
##    1. Add a Satellite object to the scenario

SAOCOMsatellite_STKObj      = root.CurrentScenario.Children.New(18, SatelliteName)  # eSatellite
SAOCOMsatellite_SatObj      = SAOCOMsatellite_STKObj.QueryInterface(STKObjects.IAgSatellite)
SAOCOMsatellite_SatObj.SetPropagatorType(STKObjects.ePropagatorSGP4)

# Set satellite propagator to SGP4 and propagate
#satellite2.SetPropagatorType(4)  # ePropagatorSGP4
CBApropagator_PropObj       = SAOCOMsatellite_SatObj.Propagator
CBApropagator_SGP4Obj       = CBApropagator_PropObj.QueryInterface(STKObjects.IAgVePropagatorSGP4)
CBApropagator_SGP4Obj.EphemerisInterval.SetImplicitInterval(root.CurrentScenario.Vgt.EventIntervals.Item("AnalysisInterval"))  # Link to scenario period
CBApropagator_SGP4Obj.Step  = StepTime
CBApropagator_SGP4AutoU = CBApropagator_SGP4Obj.AutoUpdate
CBApropagator_SGP4AutoU.SelectedSource = 3
#
#CBApropagator_SGP4AutoU.FileSource.Filename('SAOCOM-1B.tle')
CBApropagator_SGP4Obj.CommonTasks.AddSegsFromOnlineSource('46265')  # Cambiar a TLE
CBApropagator_SGP4Obj.Propagate()

#Set satellite attitude basic spinning ## me lo va a dar el TLE
CBAattitude_AttObj          = SAOCOMsatellite_SatObj.Attitude
CBAattitude_OrAtStObj       = CBAattitude_AttObj.QueryInterface(STKObjects.IAgVeOrbitAttitudeStandard)
CBAattitude_BasicObj        = CBAattitude_OrAtStObj.Basic
CBAattitude_BasicObj.SetProfileType(6)
CBAattitude_ProfObj         = CBAattitude_BasicObj.Profile
CBAattitude_FIAObj          = CBAattitude_ProfObj.QueryInterface(STKObjects.IAgVeProfileFixedInAxes)
CBAattitude_OrintObj = CBAattitude_FIAObj.Orientation
CBAattitude_OrintObj.AssignYPRAngles(4,-180,0,-90) #YPR sequence.


##    2. Add and Set the antenna object
SAOCOMantenna_STKObj        = SAOCOMsatellite_STKObj.Children.New(31, 'SAOCOMantenna')  # eAntenna
SAOCOMantenna_AntObj        = SAOCOMantenna_STKObj.QueryInterface(STKObjects.IAgAntenna)
SAOCOMantenna_AntObj.SetModel('Bessel Aperture Circular')
SAOCOMantenna_AntModObj     = SAOCOMantenna_AntObj.Model
SAOCOMantenna_AntSCBObj     = SAOCOMantenna_AntModObj.QueryInterface(STKObjects.IAgAntennaModelApertureCircularBessel)
SAOCOMantenna_AntSCBObj.Diameter = 0.5 #m
SAOCOMantenna_AntSCBObj.ComputeMainlobeGain = False
SAOCOMantenna_AntModObj.DesignFrequency = 2.255 #GHz la f que pongo acá es la misma que va en la linea 183
SAOCOMantenna_OrintObj      = SAOCOMantenna_AntObj.Orientation
SAOCOMantenna_OrintObj.AssignAzEl(0, 0, 1)  # 1 represents Rotate About Boresight
#'Value 0° = 1.27222e-14 °'

##    3. Add a Transmiter object to the satellite
CBAtransmitter_STKObj       = SAOCOMsatellite_STKObj.Children.New(24, TransmitterName)  # eTransmitter
CBAtransmitter_TraObj       = CBAtransmitter_STKObj.QueryInterface(STKObjects.IAgTransmitter)


# Modify Transmitter Modulator Properties
CBAtransmitter_TraObj.SetModel('Complex Transmitter Model')
CBAtxModel_ModObj           = CBAtransmitter_TraObj.Model
CBAtxModel_CmxModObj        = CBAtxModel_ModObj.QueryInterface(STKObjects.IAgTransmitterModelComplex)
CBAtxModel_CmxModObj.SetModulator(Dem)
CBAtxModel_CmxModObj.Modulator.AutoScaleBandwidth = True
CBAtxModel_CmxModObj.Frequency = 2.255  # GHz
CBAtxModel_CmxModObj.Power  = -14  # dBW
CBAtxModel_CmxModObj.DataRate = 5  # Mb/sec
CBAtxModel_CmxModObj.AntennaControl.ReferenceType = 0  #Link to an Antenna object
CBAtxModel_CmxModObj.AntennaControl.LinkedAntennaObject


#Modifico masa a satellite
#'Value 0 kg is invalid. Value range is 0.00100000 kg to 1000000000.00000000 kg'
SAOCOMmass                  = SAOCOMsatellite_SatObj.MassProperties
SAOCOMmass.Mass             = 0.00100000

######################################
##    Task 6
##    1. Retrive and view the access data in Phyton

# You now have a scenario with a Target object and a Satelite object. Determine when the Satelite object ...

# 1. Browsw to the STK Programming Interface help files.
# 2. Locate and manual enter code into MATLAB to compute an access between two STK Objects using the ...

# HINT: If you cannot located the code, axpand the following paragraph:

access = CBAreceiver_STKObj.GetAccessToObject(CBAtransmitter_STKObj)
access.ComputeAccess()
accessDP        = access.DataProviders.Item('Access Data')
accessDP2       = accessDP.QueryInterface(STKObjects.IAgDataPrveIntrval)
results         = accessDP2.Exec(scenario_ScenObj.StartTime, scenario_ScenObj.StopTime)
accessStartTime = results.DataSets.GetDataSetByName('Start Time').GetValues()
accessStopTime  = results.DataSets.GetDataSetByName('Stop Time').GetValues()
print(accessStartTime, accessStopTime)

######################################
##    Task 7
##    1. Retrive and view the altitud of the satellite during an access interval.

##Data provider de AER Data -> Default -> Azimuth - Elevation - Range
AERdata                 = access.DataProviders.Item('AER Data')
AERdata_GroupObj        = AERdata.QueryInterface(STKObjects.IAgDataProviderGroup)
AERdata_DataObj         = AERdata_GroupObj.Group
AERdata_Default         = AERdata_DataObj.Item('Default')
AERdata_TimeVar         = AERdata_Default.QueryInterface(STKObjects.IAgDataPrvTimeVar)
AERdata_elements        = ['Azimuth', 'Elevation', 'Range']
AERdata_results         = AERdata_TimeVar.ExecElements(scenario_ScenObj.StartTime,scenario_ScenObj.StopTime,StepTime,AERdata_elements)
accessAzimuth           = AERdata_results.DataSets.GetDataSetByName('Azimuth').GetValues()
accessElevation         = AERdata_results.DataSets.GetDataSetByName('Elevation').GetValues()
accessRange             = AERdata_results.DataSets.GetDataSetByName('Range').GetValues()

##Data provider de To Position Velocity -> ICRF -> x - y - z - xVel - yVel - zVel - RelSpeed
ToPositionVel           = access.DataProviders.Item('To Position Velocity')
ToPositionVel_GroupObj  = ToPositionVel.QueryInterface(STKObjects.IAgDataProviderGroup)
ToPositionVel_DataObj   = ToPositionVel_GroupObj.Group
ToPositionVel_ICRF      = ToPositionVel_DataObj.Item('ICRF')
ToPositionVel_TimeVar   = ToPositionVel_ICRF.QueryInterface(STKObjects.IAgDataPrvTimeVar)
ToPositionVel_elements  = ['x', 'y', 'z', 'xVel', 'yVel', 'zVel', 'RelSpeed']
ToPositionVel_results   = ToPositionVel_TimeVar.ExecElements(scenario_ScenObj.StartTime,scenario_ScenObj.StopTime,StepTime,ToPositionVel_elements)
accessX                 = ToPositionVel_results.DataSets.GetDataSetByName('x').GetValues()
accessY                 = ToPositionVel_results.DataSets.GetDataSetByName('y').GetValues()
accessZ                 = ToPositionVel_results.DataSets.GetDataSetByName('z').GetValues()
accessXVel              = ToPositionVel_results.DataSets.GetDataSetByName('xVel').GetValues()
accessYVel              = ToPositionVel_results.DataSets.GetDataSetByName('yVel').GetValues()
accessZVel              = ToPositionVel_results.DataSets.GetDataSetByName('zVel').GetValues()
accessRelSpeed          = ToPositionVel_results.DataSets.GetDataSetByName('RelSpeed').GetValues()

##Data provider de Link Information -> Prop Loss - EIRP - Rcvd. Frequency - Freq. Doppler Shift -
#                                       - Bandwidth Overlap - Rcvd. Iso. Power - Flux Density -
#                                       - g/T - C/No - Bandwidth - C/N - Spectral Flux Density -
#                                       - Eb/No - BER
LinkInfo                = access.DataProviders.Item('Link Information')
LinkInfo_TimeVar        = LinkInfo.QueryInterface(STKObjects.IAgDataPrvTimeVar)
LinkInfo_elements       = ['Prop Loss', 'EIRP', 'Rcvd. Frequency', 'Freq. Doppler Shift', 'Bandwidth Overlap','Rcvd. Iso. Power', 'Flux Density', 'g/T', 'C/No', 'Bandwidth', 'C/N', 'Spectral Flux Density', 'Eb/No','BER']
LinkInfo_results        = LinkInfo_TimeVar.ExecElements(scenario_ScenObj.StartTime,scenario_ScenObj.StopTime,StepTime,LinkInfo_elements)
accessPropLoss          = LinkInfo_results.DataSets.GetDataSetByName('Prop Loss').GetValues()
accessEIRP              = LinkInfo_results.DataSets.GetDataSetByName('EIRP').GetValues()
accessRcvdFrequency     = LinkInfo_results.DataSets.GetDataSetByName('Rcvd. Frequency').GetValues()
accessFreqDopplerShift  = LinkInfo_results.DataSets.GetDataSetByName('Freq. Doppler Shift').GetValues()
accessBandwidthOverlap  = LinkInfo_results.DataSets.GetDataSetByName('Bandwidth Overlap').GetValues()
accessRcvdIsoPower      = LinkInfo_results.DataSets.GetDataSetByName('Rcvd. Iso. Power').GetValues()
accessFluxDensity       = LinkInfo_results.DataSets.GetDataSetByName('Flux Density').GetValues()
accessgT                = LinkInfo_results.DataSets.GetDataSetByName('g/T').GetValues()
accessCNo               = LinkInfo_results.DataSets.GetDataSetByName('C/No').GetValues()
accessBandwidth         = LinkInfo_results.DataSets.GetDataSetByName('Bandwidth').GetValues()
accessCN                = LinkInfo_results.DataSets.GetDataSetByName('C/N').GetValues()
accessSpectralFluxDensity = LinkInfo_results.DataSets.GetDataSetByName('Spectral Flux Density').GetValues()
accessEbNo              = LinkInfo_results.DataSets.GetDataSetByName('Eb/No').GetValues()
accessBER               = LinkInfo_results.DataSets.GetDataSetByName('BER').GetValues()



#receiverDP       = CBAreceiver_STKObj.DataProviders.Item('Basic Properties')
#receiverDP2      = receiverDP.QueryInterface(STKObjects.IAgDataPrvFixed)
#rptElements       = ['Cable Receiver - BER', 'Gain']
#receiverDPElements = receiverDP2.ExecElements(rptElements)
#receiverModulation = receiverDPElements.DataSets.GetDataSetByName('Cable Receiver - BER').GetValues()
#print(receiverModulation)
#
#transmitterDP       = CBAtransmitter_STKObj.DataProviders.Item('Basic Properties')
#transmitterDP2      = transmitterDP.QueryInterface(STKObjects.IAgDataPrvFixed)
#rptElements       = ['Modulation Type', 'Gain']
#transmitterDPElements = transmitterDP2.ExecElements(rptElements)
#transmitterModulation = transmitterDPElements.DataSets.GetDataSetByName('Modulation Type').GetValues()
#print(transmitterModulation)
