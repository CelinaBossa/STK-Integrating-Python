### Set the variables

#   Scenrio Properties
ScenarioName  = 'Paper'
InicialTime   =  '01 Sep 2022 12:00:00.000'
FinalTime     = '+5 days'
StepTime      = 8

#   Ground Starion Properties
GroundStationName   = 'CordBS'
GroundStationLatitude = -31.4343
GroundStationLongitude = -64.2672
GroundStationAltitude = 0
GroundStationName2   = 'polarBS'
GroundStationLatitude2 = -90
GroundStationLongitude2 = -90
GroundStationAltitude2 = 0


#   Receptor Properties
CbaReceiverName = 'Receiver2'
CbaReciverType = 'Simple Receiver Model'
PolarReceiverName = 'Receiver3'

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
scenario      = root.CurrentScenario

##    2. Set the analytical time period.

scenario2     = scenario.QueryInterface(STKObjects.IAgScenario)
scenario2.SetTimePeriod(InicialTime,FinalTime)
scenario2.Animation.AnimStepValue = StepTime

##    3. Reset the animation time.
root.Rewind();



######################################
##    Task 3
##    1. Add a facility object to the scenario

## CORDOBA'S GROUND STATION
groundStation = root.CurrentScenario.Children.New(8, GroundStationName)
groundStation2 = groundStation.QueryInterface(STKObjects.IAgFacility)
root.UnitPreferences.Item('LatitudeUnit').SetCurrentUnit('deg')
root.UnitPreferences.Item('LongitudeUnit').SetCurrentUnit('deg')
groundStation2.UseTerrain = False #buscar el help -> Opt whether to set altitude automatically by using terrain data.
groundStation2.Position.AssignGeodetic(GroundStationLatitude, GroundStationLongitude, GroundStationAltitude)

## POLAR'S GROUND STATION
groundStation3 = root.CurrentScenario.Children.New(8, GroundStationName2)
groundStation4 = groundStation3.QueryInterface(STKObjects.IAgFacility)
root.UnitPreferences.Item('LatitudeUnit').SetCurrentUnit('deg')
root.UnitPreferences.Item('LongitudeUnit').SetCurrentUnit('deg')
groundStation4.UseTerrain = False
groundStation4.Position.AssignGeodetic(GroundStationLatitude2, GroundStationLongitude2, GroundStationAltitude2)



##    2. Add a Receptor object to the facility

# CORDOBA'S RECEPTOR (cambiar nombre)
receiver    = groundStation.Children.New(17, CbaReceiverName)  # eReceiver
receiver2   = receiver.QueryInterface(STKObjects.IAgReceiver)
# POLAR'S RECEPTOR
receiver3    = groundStation3.Children.New(17, PolarReceiverName)  # eReceiver
receiver4   = receiver3.QueryInterface(STKObjects.IAgReceiver)

# Modify Receiver Type
receiver2.SetModel(CbaReciverType) #CORDOBA
receiver4.SetModel(CbaReciverType) #POLAR

# Modify Receiver Demodulator Properties
# CORDOBA'S RECEPTOR
recModel = receiver2.Model
recModel2 = recModel.QueryInterface(STKObjects.IAgReceiverModelSimple)
recModel2.AutoSelectDemodulator = False  
recModel2.SetDemodulator(Dem) 
# POLAR'S RECEPTOR    
recModel3 = receiver4.Model
recModel4 = recModel3.QueryInterface(STKObjects.IAgReceiverModelSimple)
recModel4.AutoSelectDemodulator = False  
recModel4.SetDemodulator(Dem)  



##    3. Add a Satellite object to the scenario

satellite   = root.CurrentScenario.Children.New(18, SatelliteName)  # eSatellite
satellite2  = satellite.QueryInterface(STKObjects.IAgSatellite)
satellite2.SetPropagatorType(STKObjects.ePropagatorSGP4)

# Set satellite propagator to SGP4 and propagate
#satellite2.SetPropagatorType(4)  # ePropagatorSGP4
propagator = satellite2.Propagator
propagator2 = propagator.QueryInterface(STKObjects.IAgVePropagatorSGP4)
propagator2.EphemerisInterval.SetImplicitInterval(root.CurrentScenario.Vgt.EventIntervals.Item("AnalysisInterval"))  # Link to scenario period
propagator2.Step = StepTime
propagator2.CommonTasks.AddSegsFromOnlineSource('46265')  # Cambiar a TLE
propagator2.AutoUpdateEnabled = True
propagator2.Propagate()

#Set satellite attitude basic spinning ## me lo va a dar el TLE
basic = satellite2.Attitude
basic2 = basic.QueryInterface(STKObjects.IAgVeOrbitAttitudeStandard)
basic3= basic2.Basic
basic3.SetProfileType(6)
basic4 = basic3.Profile
basic5 = basic4.QueryInterface(STKObjects.IAgVeProfileFixedInAxes)
#basic6 = satellite2.Attitude.QueryInterface(STKObjects.IAgVeAttitudeRealTime)
#basic6.AddYPR('YPR',0,60,0)
## !! FALTA CAMBIAR LOS VALORES DE YAW Y ROLL(AddYPR) <------------------------

#basic5.Body.AssignXYZ(0, 0, 1)
#basic5.Inertial.AssignXYZ(0, 1, 0)
#basic5.Rate = 6

##    4. Add a Transmiter object to the satellite
transmitter     = satellite.Children.New(24, TransmitterName)  # eTransmitter
transmitter2    = transmitter.QueryInterface(STKObjects.IAgTransmitter)


# Modify Transmitter Modulator Properties #cambiar a tipo complejo
txModel = transmitter2.Model
txModel2    = txModel.QueryInterface(STKObjects.IAgTransmitterModelSimple)
txModel2.SetModulator(Dem)
txModel2.Modulator.AutoScaleBandwidth = True

#Modifico masa a satellite
#'Value 0 kg is invalid. Value range is 0.00100000 kg to 1000000000.00000000 kg'
mass = satellite2.MassProperties
mass.Mass = 0.00100000

######################################
##    Task 4
##    1. Retrive and view the access data in Phyton

# You now have a scenario with a Target object and a Satelite object. Determine when the Satelite object ...

# 1. Browsw to the STK Programming Interface help files.
# 2. Locate and manual enter code into MATLAB to compute an access between two STK Objects using the ...

# HINT: If you cannot located the code, axpand the following paragraph:

access = receiver.GetAccessToObject(transmitter)
access.ComputeAccess()
accessDP        = access.DataProviders.Item('Access Data')
accessDP2       = accessDP.QueryInterface(STKObjects.IAgDataPrvInterval)
results         = accessDP2.Exec(scenario2.StartTime, scenario2.StopTime)
accessStartTime = results.DataSets.GetDataSetByName('Start Time').GetValues()
accessStopTime  = results.DataSets.GetDataSetByName('Stop Time').GetValues()
print(accessStartTime, accessStopTime)

######################################
##    Task 5
##    2. Retrive and view the altitud of the satellite during an access interval.

receiverDP       = receiver.DataProviders.Item('Basic Properties')
receiverDP2      = receiverDP.QueryInterface(STKObjects.IAgDataPrvFixed)
rptElements       = ['Cable Receiver - BER', 'Gain']
receiverDPElements = receiverDP2.ExecElements(rptElements)
receiverModulation = receiverDPElements.DataSets.GetDataSetByName('Cable Receiver - BER').GetValues()
print(receiverModulation)

transmitterDP       = transmitter.DataProviders.Item('Basic Properties')
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

