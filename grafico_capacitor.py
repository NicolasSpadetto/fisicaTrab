import serial
import matplotlib.pyplot as plt
import matplotlib.animation as ani
import time as t

porta = 'COM3'
bauds = 9600
cap = 0.0001
eixo_t = [0.0] 
eixo_Q = [0.0]
eixo_B = [0.0]
eixo_EM = [0.0]
T_seg = 6 #em segundos

grafico = plt.figure()
eixos = grafico.add_subplot()

ardReads = serial.Serial(porta, bauds)
ardReads.setDTR(False)
t.sleep(1)
ardReads.flushInput()
ardReads.setDTR(True)

grafPrint = 0 #vira 1 dps que o gráfico já fora feito

def addEixo(nv_carga, nv_tempo, nv_campo): #0 para t, 1 para v
    global eixo_t
    global eixo_Q
    global eixo_B

    eixo_Q.append(nv_carga)
    eixo_t.append(nv_tempo)
    eixo_B.append(nv_campo)
    #eixo_R.append(5.0 - nv_valor)
    #eixo_Q.append(nv_valor * cap)       

def animar(i):
    global ardReads
    global eixos
    global cap
    global eixo_EM
    ardData = ardReads.readline()
    ardData = ardData.decode("utf-8").strip(' \r\n')
    ardData = ardData.split(" ")
    nv_q = (float(ardData[0])) * cap
    print(ardData)
    nv_t = (float(ardData[2])) / 1000.0
    nv_b = (float(ardData[1])) / 250

    eixo_EM.append(nv_q + nv_b)

    addEixo(nv_q, nv_t, nv_b)
    
    eixos.clear()

    eixos.plot(eixo_t, eixo_Q, eixo_t, eixo_B)
    eixos.plot(eixo_t, eixo_EM)
    
    #plt.plot(eixo_t, eixo_Q)
    #plt.plot(eixo_t, eixo_R)
    plt.xlabel("Tempo em Segundos")
    plt.ylabel("energias")
    plt.title("RLC: carga e descarga")
    #plt.savefig('plot.png', dpi=300, bbox_inches='tight')

resultado = ani.FuncAnimation(grafico, animar, interval= 1, cache_frame_data=False)

plt.show()


        