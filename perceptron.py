
import numpy as np
import matplotlib.pyplot as plt 
#Ingresar los pesos
entradas = []
patrones_n = np.array([])
patrones = {}
w = []

patrones_v = [int(input("Ingrese el valor del patron: ")) for l in range(int(input("Ingrese la cantidad de patrones: " ))*2)] #Entrada de patrones
patron =np.reshape(patrones_v, (int(len(patrones_v)/2), 2)) #Redimensiona la lista

estados_finales = np.array([int(input("Ingrese el estado final: ")) for l in range(int(patron.shape[0]))]) #.shape obtiene la dimension del array y obtencion de estados finales

pesos = np.array([float(input("Ingrese el peso: ")) for l in range(2)], dtype='f') #Obtencion de pesos
print(pesos)

b = float(input("Ingrese la ganancia: ")) #Ingresa la ganancia

errores = [] #Lista en la que se guaradaran los errores

hardlim_hardlims = np.sort(np.unique(estados_finales))

i = 0 #Reinicia el bucle en caso de ser necesario, ya que con la estructura for no se logra reiniciar
vueltas = 1
while i < int(patron.shape[0]): #Mientras sea menor al numero de patrones ingresados (P1, p2 .... P+n)
    #suma_vectores = np.dot(pesos,patron[i])
    multiplica_vectores = np.dot(pesos,patron[i]) #Multiplica los vectores (W(0)Pa)
    a = multiplica_vectores + b #Se suma la multiplicacion mas la ganacia para obtener a
    print(f"PARA PATRON P{i+1} iteracion {vueltas}")
    print("a: ", a) #Modificar ya sea para hardlim o hardlims
    
    if np.allclose(hardlim_hardlims, [0,1]) == True:
        if a >= 0:
            a = 1
        if a < 0:
            a = 0
    else:
        if a < 0:
            a = -1
        else:
            a = 1
    #np.append(errores, estados_finales[i] - a)
    errores.append(estados_finales[i] - a) #Se obtiene el error y se guarda en una lista
    print("errores:", errores)
    if errores[i]!=0:                             #Se reajustan los valores de los pesos y la ganacia en caso de que el error sea diferente de 0
        patron_t = np.transpose(patron[i]) * errores[i]
        pesos = np.add(pesos, patron_t)   #Nuevos pesos
        b = b + errores[i]
    #print("iteracion: " , i)
    print("pesos: " , pesos)
    print("b: ", b)
    i+=1 
    #En caso de que la lista de errores tenga tamaño 4(indicaria que ya se iteraron por completo los patrones) y dentro de esta se encuentre algun error diferente de cero se reiniciara el bucle 
    if len(errores) == 4 and np.array_equal(np.array(errores),np.zeros(int(patron.shape[0])))==False: 
        errores.clear()
        i = 0
        vueltas += 1
        #print("Vuelta: ", vueltas) #Lleva el numero de iteraciones
        #print("si entro")
    print("-----------------------------------------------------")

traza_x = -b/pesos[0]
traza_y = -b/pesos[1]
print("DATOS FINALES")
print(f"x: {traza_x}, y: {traza_y}")
print("Numero de iteraciones: " , vueltas)
print("Pesos: ", pesos)
print("Ganacia: ", b)

x, y = patron.T
plt.scatter(x,y)
plt.plot([traza_x,0], [0,traza_y], linewidth=2)

plt.show()
