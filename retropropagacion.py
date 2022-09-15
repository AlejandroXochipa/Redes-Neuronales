# -*- coding: utf-8 -*-
"""
Created on Mon May  9 23:08:24 2022

@author: xochi
"""

import numpy as np
import math
import matplotlib.pyplot as plt 
import pandas as pd 

class NeuronaOculta:
    def __init__(self, w, b, funcion_activacion, p):
        self.w = w
        self.b = b
        self.funcion_activacion = funcion_activacion
        self.p = p
    
    def getW(self):
        return self.w
    def getB(self):
        return self.b
    def getfuncionActivacion(self):
        return self.funcion_activacion
    def getP(self):
        return self.p
    def setW(self, w):
        self.w = w
    def setB(self, b):
        self.b = b  
    def setP(self, p):
        self.p = p  
    def setfuncionActiacion(self, funcion_activacion):
        self.funcion_activacion = funcion_activacion


class NeuronaSalida:
    def __init__(self, w, b, funcion_activacion, p):
        self.w = w
        self.b = b
        self.funcion_activacion = funcion_activacion
        self.p = p
    
    def getW(self):
        return self.w
    def getB(self):
        return self.b
    def getfuncionActivacion(self):
        return self.funcion_activacion
    def getP(self):
        return self.p
    def setW(self, w):
        self.w = w
    def setB(self, b):
        self.b = b  
    def setP(self, p):
        self.p = p 
    def setfuncionActiacion(self, funcion_activacion):
        self.funcion_activacion = funcion_activacion

def abrirExcel():
    #Lee los exceles
    df = pd.read_excel(r"C:\Users\xochi\Downloads\Base_Datos_FallasElectricas.xlsx")
    df2 = pd.read_excel(r"C:\Users\xochi\Downloads\Base_Datos_SinFallasElectricas.xlsx")
    return df,df2



df,df2 = abrirExcel()
#print(type(np.array(df["Tiempo (s)"])), np.shape(np.array(df[["Corriente ia","Corriente ib","Corriente ic"]])))



"""datos = df[["Corriente ia","Corriente ib","Corriente ic"]].to_numpy().flatten()
resultado = pd.DataFrame(datos[datos != None])
resultado = np.array(resultado)
print((np.shape(np.array(resultado))))"""



#Se compara el excel con fallas electricas respecto al excel sin fallas electricas 
tiempo = []
datos2 = []
contador = 0
for i in df.columns.values:
    if i == df.columns.values[0]:
        continue
    else:
        contador += 1
        datos2.append(np.array(df[i]))
        tiempo.append(np.array([df2[df2.columns.values[contador]]]))
        
    
tiempo = np.resize(np.array(tiempo), (9003,1)) #Mover a la dimension que tenga la tabla
datos2 = np.resize(np.array(datos2), (9003,1))
concatenacion = np.concatenate((tiempo, datos2), axis = 1)

prueba = concatenacion[:,1]

patrones_depurados = np.array([np.array([t,d]) for t,d in zip(concatenacion[:,0],concatenacion[:,1]) if t >= -1 and t <= 1])
patrones_sinclase = np.array([np.array([t,d]) for t,d in zip(concatenacion[:,0],concatenacion[:,1]) if t <= -1 or t >= 1])
print((patrones_depurados))
estados = np.array([1 if l >=0 else -1 for l in patrones_depurados[:,1]])
print(estados)




def neuronaOculta(w,b,funcion_activacion, p):
    a = w*p + b 
    if funcion_activacion == "tansig":
        a[0] = (math.exp(a[0]) - math.exp(-1*a[0])) / (math.exp(a[0]) + math.exp(-1*a[0]))
        a[1] = (math.exp(a[1]) - math.exp(-1*a[1])) / (math.exp(a[1]) + math.exp(-1*a[1])) 
    if funcion_activacion == "logsig":
        a[0] = 1 / 1 + math.exp(-a[0])
        a[1] = 1 / 1 + math.exp(-a[1])  
    if funcion_activacion == "purelin":
        a = a
    print("a oculta: ", a)
    return a
    
def neuronaSalida(w,b,funcion_activacion, p, t):
    a = np.dot(w,p) + b 
    if funcion_activacion == "tansig":
        a = (math.exp(a) - math.exp(-1*a)) / (math.exp(a) + math.exp(-1*a))
        #a[1] = (math.exp(a[1]) - math.exp(-1*a[1])) / (math.exp(a[1]) + math.exp(-1*a[1]))  
    if funcion_activacion == "logsig":
        a = 1 / 1 + math.exp(-a)
    if funcion_activacion == "purelin":
        a = a
    error = t - a
    return a, error

def actualizacionPesosS(funcion_activacion, error, a_salida, w, b, alpha,a_oculta):
    sensitividad = 0
    if funcion_activacion == "purelin":
       sensitividad = -2*1*error
    if funcion_activacion == "tansig":
       sensitividad = -2*(1 - (np.power(a_salida,2)))*error
    if funcion_activacion == "logsig":
        sensitividad = -2*(a_salida*(1-a_salida))*error
    w = w - alpha*sensitividad*a_oculta
    b = b - alpha*sensitividad
    return w, b, sensitividad

def actualizacionPesosO( a, w_salida, b, s, alpha, patron, w_oculta):
    sensitividad = np.zeros([2,2], dtype=float)
    print("Pesos salida: ", w_salida)
    sensitividad[0][0] = 1 - np.power(a[0], 2)
    sensitividad[1][1] = 1 - np.power(a[1], 2)
    sensitividad = np.dot(sensitividad, w_salida) * s
    print("sensitividad oculta: ", sensitividad)
    print("--------------------------------")
    w = w_oculta - alpha * sensitividad * patron
    b = b - alpha * sensitividad
    return w, b

    
   
    
#patrones = np.array([float(input("Ingrese el valor del patron: ")) for l in range(int(input("Ingrese el numero de patrones: ")))])
#estados_finales = np.array([float(input("Ingrese el valor del estado final del patron: ")) for l in range(len(patrones))])

patrones = patrones_depurados
estados_finales = estados


#neuronas_capa_oculta = int(input("Ingrese el numero de neuronas de capa oculta: "))
w_oculta = np.array([float(input("Ingrese el valor del peso en capa oculta: ")) for l in range(2)])
b_oculta = np.array([float(input("Ingrese el valor de la ganancia en capa oculta: ")) for l in range(2)])


#neuronas_capa_salida = int(input("Ingrese el numero de neuronas de capa de salida: "))
w_salida = np.array([float(input("Ingrese el valor del peso en capa salida: ")) for l in range(2)])
b_salida = float(input("Ingrese el valor de la ganacia en capa salida: "))
alpha = float(input("Ingrese el valor de alpha: "))


n1 = NeuronaOculta(w_oculta, b_oculta, "tansig", patrones[0])
ns = NeuronaSalida(w_salida, b_salida, "purelin", 1)
sensitividad_s = 0
iteraciones = 1
i = 0
errores = []
errores_finales = []
errores_anteriores = []
while(i < len(patrones)):
    n1.setP(patrones[i])
    n1.setB(b_oculta)
    n1.setfuncionActiacion("tansig")   #Aqui se cambia la funcion de activacion de capa oculta
    n1.setW(w_oculta)
    print("Pesos a presentar oculta", n1.getW())
    print("ganacia a presentar oculta", n1.getB())
    a_oculta =  neuronaOculta(n1.getW(),n1.getB(),n1.getfuncionActivacion(), n1.getP())
    ns.setP(a_oculta)
    ns.setB(b_salida)
    ns.setfuncionActiacion("purelin") #Aqui se cambia la funcion de activacion de capa oculta
    ns.setW(w_salida)
    a_salida, error = neuronaSalida(ns.getW(),ns.getB(),ns.getfuncionActivacion(), ns.getP(), estados_finales[i])
    print("a salida: ", a_salida)
    errores.append(error)
    w_salida, b_salida, sensitividad_s = actualizacionPesosS(ns.getfuncionActivacion(), error, a_salida, ns.getW(), ns.getB(), alpha, a_oculta)
    print("sensitividad salida: ", sensitividad_s)
    w_oculta , b_oculta = actualizacionPesosO( a_oculta, ns.getW(), n1.getB(), sensitividad_s, alpha, n1.getP(), n1.getW())
    
    
    
    
    
    
    if len(errores) == len(patrones):
        errores_finales.append(errores[-1])
        errores_anteriores.extend(errores)
    
    #print()
    if len(errores) == len(patrones) and len(errores_finales) >= 2:
        #print(errores_anteriores)
        #print(errores_finales, "Hoplo")
        #print(errores[i])
        
        gradiente_error = abs(errores_finales[-2]  - errores[i])
        print((gradiente_error))
        if ((gradiente_error) > 0.01) == False or (set(errores_anteriores[-(len(patrones))*2:-len(patrones)])==set(errores))==True:
            print("SE PARO")
            break
    
    if errores[i] == 0:
        print("Se paro con:", errores[i])
        break
    i+=1 
    if len(errores) == len(patrones) and np.array_equal(np.array(errores),np.zeros((len(patrones))))==False: 
        
            
        errores.clear()
        i = 0
    iteraciones+=1
    
    
    
    
print("Iteraciones", iteraciones/len(patrones))   
    
    

traza_x = -ns.getB()/ns.getW()[0]
traza_y = -ns.getB()/ns.getW()[1]
x = patrones[:,0].T
y = patrones[:,1].T
x1 = patrones_sinclase[:,0].T
y1 = patrones_sinclase[:,1].T


#x = patrones.T
#y = estados_finales.T

plt.scatter(x,y, c='green')
plt.scatter(x1,y1, c='red')
plt.title("Separacion Lineal")
plt.plot([traza_x,0],[0,traza_y],linewidth=2)
plt.show()

plt.ylabel('Error', fontsize=12)
plt.xlabel('Iteraciones',fontsize=12)
plt.title("Retropropagacion")
x = np.arange(len(errores_finales))
plt.plot([x],[errores_finales],'m->')
plt.legend(loc='upper right')
plt.show()















