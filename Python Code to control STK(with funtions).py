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
