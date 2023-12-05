import serial
import matplotlib.pyplot as plt
import time as t
porta = 'COM3'
bauds = 9600

eixo_t = [0.0] 
eixo_v = [0.0]

T_seg = 6 #em segundos

grafPrint = 0 #vira 1 dps que o gráfico já fora feito

def addEixo(nv_valor, nv_tempo): #0 para t, 1 para v
    global eixo_t
    global eixo_v
    
    eixo_v.append(nv_valor)
    eixo_t.append(nv_tempo)
            


ardReads = serial.Serial(porta, bauds)
ardReads.setDTR(False)
t.sleep(1)
ardReads.flushInput()
ardReads.setDTR(True)



while (not grafPrint):
    try:
        ardData = ardReads.readline()
        ardData = ardData.decode("utf-8").strip(' \r\n')
        nv_v = float(ardData[0] + ardData[1] + ardData[2] + ardData[3])
        nv_t = ardData.replace(str(nv_v), '')
        nv_t = (float(nv_t.replace(' ', ''))) / 1000.0
        
        addEixo(nv_v, nv_t)
        
        print(eixo_t[len(eixo_t) - 1], eixo_v[len(eixo_v) - 1])
        
        
    except:
        print("informação perdida...\n")
    
    print(len(eixo_t))

    if ((eixo_t[len(eixo_t) - 1] >= T_seg)):

        print(eixo_t)
        plt.plot(eixo_t, eixo_v)
        plt.xlabel("Tempo em Segundos")
        plt.ylabel("Tensão em Volts")
        plt.title("Capacitor: carga e descarga")
        #plt.savefig('plot.png', dpi=300, bbox_inches='tight')
        plt.show(block= False)
        plt.pause(130)
        
        grafPrint = 1


t.sleep(30)
        