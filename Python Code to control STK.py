### Set the variables

#   Scenrio Properties
ScenarioName  = 'Paper'
InicialTime   =  '01 Sep 2022 12:00:00.000'
FinalTime     = '+5 days'
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
Dem = '8PSK'

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
# POLAR'S RECEPTOR    
POLARrecModel_ModObj        = POLARreceiver_RecObj.Model
POLARrecModel_SModObj       = POLARrecModel_ModObj.QueryInterface(STKObjects.IAgReceiverModelSimple)
POLARrecModel_SModObj.AutoSelectDemodulator = False  
POLARrecModel_SModObj.SetDemodulator(Dem)  

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
CBApropagator_SGP4Obj.CommonTasks.AddSegsFromOnlineSource('46265')  # Cambiar a TLE
CBApropagator_SGP4Obj.AutoUpdateEnabled = True
CBApropagator_SGP4Obj.Propagate()

#Set satellite attitude basic spinning ## me lo va a dar el TLE
CBAattitude_AttObj          = SAOCOMsatellite_SatObj.Attitude
CBAattitude_OrAtStObj       = CBAattitude_AttObj.QueryInterface(STKObjects.IAgVeOrbitAttitudeStandard)
CBAattitude_BasicObj        = CBAattitude_OrAtStObj.Basic
CBAattitude_BasicObj.SetProfileType(6)
CBAattitude_ProfObj         = CBAattitude_BasicObj.Profile
CBAattitude_FIAObj          = CBAattitude_ProfObj.QueryInterface(STKObjects.IAgVeProfileFixedInAxes)
#basic6 = satellite2.Attitude.QueryInterface(STKObjects.IAgVeAttitudeRealTime)
#basic6.AddYPR('YPR',0,60,0)
## !! FALTA CAMBIAR LOS VALORES DE YAW Y ROLL(AddYPR) <------------------------

#basic5.Body.AssignXYZ(0, 0, 1)
#basic5.Inertial.AssignXYZ(0, 1, 0)
#basic5.Rate = 6

##    4. Add a Transmiter object to the satellite
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
CBAtxModel_CmxModObj.AntennaControl.SetEmbeddedModel('Bessel Aperture Circular')

#Modifico masa a satellite
#'Value 0 kg is invalid. Value range is 0.00100000 kg to 1000000000.00000000 kg'
SAOCOMmass                  = SAOCOMsatellite_SatObj.MassProperties
SAOCOMmass.Mass             = 0.00100000

######################################
##    Task 4
##    1. Retrive and view the access data in Phyton

# You now have a scenario with a Target object and a Satelite object. Determine when the Satelite object ...

# 1. Browsw to the STK Programming Interface help files.
# 2. Locate and manual enter code into MATLAB to compute an access between two STK Objects using the ...

# HINT: If you cannot located the code, axpand the following paragraph:

access = CBAreceiver_STKObj.GetAccessToObject(CBAtransmitter_STKObj)
access.ComputeAccess()
accessDP        = access.DataProviders.Item('Access Data')
accessDP2       = accessDP.QueryInterface(STKObjects.IAgDataPrvInterval)
results         = accessDP2.Exec(scenario_ScenObj.StartTime, scenario_ScenObj.StopTime)
accessStartTime = results.DataSets.GetDataSetByName('Start Time').GetValues()
accessStopTime  = results.DataSets.GetDataSetByName('Stop Time').GetValues()
print(accessStartTime, accessStopTime)

######################################
##    Task 5
##    2. Retrive and view the altitud of the satellite during an access interval.

receiverDP       = CBAreceiver_STKObj.DataProviders.Item('Basic Properties')
receiverDP2      = receiverDP.QueryInterface(STKObjects.IAgDataPrvFixed)
rptElements       = ['Cable Receiver - BER', 'Gain']
receiverDPElements = receiverDP2.ExecElements(rptElements)
receiverModulation = receiverDPElements.DataSets.GetDataSetByName('Cable Receiver - BER').GetValues()
print(receiverModulation)

transmitterDP       = CBAtransmitter_STKObj.DataProviders.Item('Basic Properties')
transmitterDP2      = transmitterDP.QueryInterface(STKObjects.IAgDataPrvFixed)
rptElements       = ['Modulation Type', 'Gain']
transmitterDPElements = transmitterDP2.ExecElements(rptElements)
transmitterModulation = transmitterDPElements.DataSets.GetDataSetByName('Modulation Type').GetValues()
print(transmitterModulation)




## Modify Receiver System Noise Temperature
#recModel = receiver2.Model
#receiver2.SetModel(CbaReciverType)
##recModel.SystemNoiseTemperature.ConstantNoiseTemperature = 20  # K


######################################
##    Task 4
##    1. Add a satellite to the scenario
#satellite = root.CurrentScenario.Children.New(18, SatelliteName)  # eSatellite
#satellite2 = satellite.QueryInterface(STKObjects.IAgSatellite)

##Set satellite propagator to SGP4 and propagate
#satellite2.SetPropagatorType(4)  # ePropagatorSGP4
#propagator = satellite2.Propagator
#propagator.EphemerisInterval.SetImplicitInterval(root.CurrentScenario.Vgt.EventIntervals.Item("AnalysisInterval")  # Link to scenario period
#propagator.CommonTasks.AddSegsFromOnlineSource = '25544'  # International Space Station
#propagator.AutoUpdateEnabled = True
#propagator.Propagate()



#groundStation3 = root.CurrentScenario.Children.New(8, 'PolarBs')
#groundStation4 = groundStation3.QueryInterface(STKObjects.IAgFacility)
#root.UnitPreferences.Item('LatitudeUnit').SetCurrentUnit('deg')
#root.UnitPreferences.Item('LongitudeUnit').SetCurrentUnit('deg')
#groundStation4.Position.AssignGeodetic(-90, -90, 0)

###    2. Add a Receptor object to the facility

#receiver3    = groundStation3.Children.New(17, 'Receiver3')  # eReceiver
#receiver4    = receiver3.QueryInterface(STKObjects.IAgReceiver)

## Modify Receiver System Noise Temperature
#receiver4.SetModel("Simple Receiver Model")
#recModel2 = receiver4.Model
##recModel.SystemNoiseTemperature.ConstantNoiseTemperature = 20  # K


## Modify Receiver Demodulator Properties
#recModel2.AutoSelectDemodulator = False
#recModel2.SetDemodulator = Dem 

######################################
##    Task 4
##    1. Add a satellite to the scenario
#satellite = root.CurrentScenario.Children.New(18, SatelliteName)  # eSatellite
#satellite2 = satellite.QueryInterface(STKObjects.IAgSatellite)

##Set satellite propagator to SGP4 and propagate
#satellite2.SetPropagatorType(4)  # ePropagatorSGP4
#propagator = satellite2.Propagator
#propagator.EphemerisInterval.SetImplicitInterval(
#    root.CurrentScenario.Vgt.EventIntervals.Item("AnalysisInterval"))  # Link to scenario period
#propagator.CommonTasks.AddSegsFromOnlineSource('25544')  # International Space Station
#propagator.AutoUpdateEnabled = True
#propagator.Propagate()

