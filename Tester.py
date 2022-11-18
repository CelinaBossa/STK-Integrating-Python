import pandas as pd

def get_data(path):
    dataStr = ['Access Number', 'Azimuth (deg)','Elevation (deg)','Range (km)','x (km)',
               'y (km)','z (km)','xVel (km/sec)','yVel (km/sec)',
               'zVel (km/sec)','RelSpeed (km/sec)','Prop Loss (dB)',
               'EIRP (dBW)','Rcvd. Frequency (GHz)',
               'Freq. Doppler Shift (GHz)','Bandwidth Overlap (dB)',
               'Rcvd. Iso. Power (dBW)','Flux Density (dBW/m^2)',
               'g/T (dB/K)','C/No (dB*MHz)','Bandwidth (MHz)',
               'C/N (dB)','Spectral Flux Density (dBW*m^-2*Hz^-1)',
               'Eb/No (dB)','BER']
#    data_rows = []
#    for i in range(b):
#        if i>= a:
#            data_rows.append(i)
    with open(path, newline='') as File:
        data = pd.read_csv(File,delimiter=",",usecols=dataStr)
    return data
    
def get_error(ReporteMartin, ReporteMio, col):
    array_a = []
    array_b = []
    for i in range(len(ReporteMio)):
        array_a.append(ReporteMio.iloc[i][col])
        array_b.append(ReporteMartin.iloc[i][col])
    def get_error_rel(a, b): return ((abs(a-b)/a)*100 if a != 0 else 0)
    resultado = list(map(get_error_rel, array_a, array_b))
    return resultado
def get_promedio(array):
    promedio = 0
    for i in range(len(array)):
        promedio = promedio + array[i]
    promedio = promedio/len(array)
    return promedio

DemOptions              = ['QPSK','8PSK','16PSK','QAM16','QAM32']
ElvOptions              = [-65,-32.5,0,32.5,65]
    
def error_report(ReporteOriginal, ReporteCopia):
    for i in range(len(ReporteOriginal)):
        Report = ReporteCopia[i]
        Report_M = ReporteOriginal[i]
        Elv = ElvOptions[i]
        
        ReporteMio = get_data(Report)
        ReporteMartin = get_data(Report_M)
        
        AzimuthError = get_error(ReporteMartin,ReporteMio,'Azimuth (deg)')
        ElevationError = get_error(ReporteMartin,ReporteMio,'Elevation (deg)')
        RangeError = get_error(ReporteMartin,ReporteMio,'Range (km)')
        xError = get_error(ReporteMartin,ReporteMio,'x (km)')
        yError = get_error(ReporteMartin,ReporteMio,'y (km)')
        zError = get_error(ReporteMartin,ReporteMio,'z (km)')
        xVelError = get_error(ReporteMartin,ReporteMio,'xVel (km/sec)')
        yVelError = get_error(ReporteMartin,ReporteMio,'yVel (km/sec)')
        zVelError = get_error(ReporteMartin,ReporteMio,'zVel (km/sec)')
        RelSpeedError = get_error(ReporteMartin,ReporteMio,'RelSpeed (km/sec)')
        PropLossError = get_error(ReporteMartin,ReporteMio,'Prop Loss (dB)')
        EIRPError = get_error(ReporteMartin,ReporteMio,'EIRP (dBW)')
        RcvdFrequencyError = get_error(ReporteMartin,ReporteMio,'Rcvd. Frequency (GHz)')
        FreqDopplerShiftError = get_error(ReporteMartin,ReporteMio,'Freq. Doppler Shift (GHz)')
        BandwidthOverlapError = get_error(ReporteMartin,ReporteMio,'Bandwidth Overlap (dB)')
        RcvdIsoPowerError = get_error(ReporteMartin,ReporteMio,'Rcvd. Iso. Power (dBW)')
        FluxDensityError = get_error(ReporteMartin,ReporteMio,'Flux Density (dBW/m^2)')
        gTError = get_error(ReporteMartin,ReporteMio,'g/T (dB/K)')
        CNoError = get_error(ReporteMartin,ReporteMio,'C/No (dB*MHz)')
        BandwidthError = get_error(ReporteMartin,ReporteMio,'Bandwidth (MHz)')
        CNError = get_error(ReporteMartin,ReporteMio,'C/N (dB)')
        SpectralFluxDensityError = get_error(ReporteMartin,ReporteMio,'Spectral Flux Density (dBW*m^-2*Hz^-1)')
        EbNoError = get_error(ReporteMartin,ReporteMio,'Eb/No (dB)')
        BERError = get_error(ReporteMartin,ReporteMio,'BER')
        
        AzimuthError.append(get_promedio(AzimuthError))
        ElevationError.append(get_promedio(ElevationError))
        RangeError.append(get_promedio(RangeError))
        xError.append(get_promedio(xError))
        yError.append(get_promedio(yError))
        zError.append(get_promedio(zError))
        xVelError.append(get_promedio(xVelError))
        yVelError.append(get_promedio(yVelError))
        zVelError.append(get_promedio(zVelError))
        RelSpeedError.append(get_promedio(RelSpeedError))
        PropLossError.append(get_promedio(PropLossError))
        EIRPError.append(get_promedio(EIRPError))
        RcvdFrequencyError.append(get_promedio(RcvdFrequencyError))
        FreqDopplerShiftError.append(get_promedio(FreqDopplerShiftError))
        BandwidthOverlapError.append(get_promedio(BandwidthOverlapError))
        RcvdIsoPowerError.append(get_promedio(RcvdIsoPowerError))
        FluxDensityError.append(get_promedio(FluxDensityError))
        gTError.append(get_promedio(gTError))
        CNoError.append(get_promedio(CNoError))
        BandwidthError.append(get_promedio(BandwidthError))
        CNError.append(get_promedio(CNError))
        SpectralFluxDensityError.append(get_promedio(SpectralFluxDensityError))
        EbNoError.append(get_promedio(EbNoError))
        BERError.append(get_promedio(BERError))
        
        
        tabla = {
                            	   'Azimuth (deg)': AzimuthError,
                                   'Elevation (deg)': ElevationError,
                            	   'Range (km)': RangeError,
                                   'x (km)': xError,
                                   'y (km)': yError,
                                   'z (km)': zError,
                                   'xVel (km/sec)': xVelError,
                                   'yVel (km/sec)': yVelError,
                                   'zVel (km/sec)': zVelError,
                                   'RelSpeed (km/sec)': RelSpeedError,
                                   'Prop Loss (dB)': PropLossError,
                                   'EIRP (dBW)': EIRPError,
                                   'Rcvd. Frequency (GHz)': RcvdFrequencyError,
                                   'Freq. Doppler Shift (GHz)': FreqDopplerShiftError,
                                   'Bandwidth Overlap (dB)': BandwidthOverlapError,
                                   'Rcvd. Iso. Power (dBW)': RcvdIsoPowerError,
                                   'Flux Density (dBW/m^2)': FluxDensityError,
                                   'g/T (dB/K)': gTError,
                                   'C/No (dB*MHz)': CNoError,
                                   'Bandwidth (MHz)': BandwidthError,
                                   'C/N (dB)': CNError,
                                   'Spectral Flux Density (dBW*m^-2*Hz^-1)': SpectralFluxDensityError,
                                   'Eb/No (dB)': EbNoError,
                                   'BER': BERError,          
        }
                    
        reporte = pd.DataFrame(tabla)
        reporte.to_csv("Error_QAM32_"+str(Elv)+".csv")
        reporte.to_excel("Error_QAM32_"+str(Elv)+".xlsx")

Reporte4PSK     = ["Reporte_QPSK_-65.csv","Reporte_QPSK_-32.5.csv","Reporte_QPSK_0.csv",
                  "Reporte_QPSK_32.5.csv","Reporte_QPSK_65.csv"]
Reporte8PSK     = ["Reporte_8PSK_-65.csv","Reporte_8PSK_-32.5.csv","Reporte_8PSK_0.csv",
                  "Reporte_8PSK_32.5.csv","Reporte_8PSK_65.csv"]
Reporte16PSK    = ["Reporte_16PSK_-65.csv","Reporte_16PSK_-32.5.csv","Reporte_16PSK_0.csv",
                  "Reporte_16PSK_32.5.csv","Reporte_16PSK_65.csv"]
ReporteQAM16    = ["Reporte_QAM16_-65.csv","Reporte_QAM16_-32.5.csv","Reporte_QAM16_0.csv",
                  "Reporte_QAM16_32.5.csv","Reporte_QAM16_65.csv"]
ReporteQAM32    = ["Reporte_QAM32_-65.csv","Reporte_QAM32_-32.5.csv","Reporte_QAM32_0.csv",
                  "Reporte_QAM32_32.5.csv","Reporte_QAM32_65.csv"]
ReportesMartin  = ["Degree-65 Facility-CordBS-Receiver-Receiver2-To-Satellite-Saocom-1-B-Transmitter-Transmitter3 paper-data-report.csv",
                  "Degree-32_5 Facility-CordBS-Receiver-Receiver2-To-Satellite-Saocom-1-B-Transmitter-Transmitter3 paper-data-report.csv",
                  "Degree0 Facility-CordBS-Receiver-Receiver2-To-Satellite-Saocom-1-B-Transmitter-Transmitter3 paper-data-report.csv",
                  "Degree32_5 Facility-CordBS-Receiver-Receiver2-To-Satellite-Saocom-1-B-Transmitter-Transmitter3 paper-data-report.csv",
                  "Degree65 Facility-CordBS-Receiver-Receiver2-To-Satellite-Saocom-1-B-Transmitter-Transmitter3 paper-data-report.csv"]

error_report(ReporteQAM32,ReportesMartin)
