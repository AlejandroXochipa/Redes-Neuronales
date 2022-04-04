
from pickletools import uint8
import numpy as np
import matplotlib.pyplot as plt 
#Ingresar los pesos


patrones_v = [float(input("Ingrese el valor del patron: ")) for l in range(int(input("Ingrese la cantidad de patrones: " ))*2)] #Entrada de patrones
patron =np.reshape(patrones_v, (int(len(patrones_v)/2), 2)) #Redimensiona la lista

estados_finales = np.array([float(input("Ingrese el estado final: ")) for l in range(int(patron.shape[0]))]) #.shape obtiene la dimension del array y obtencion de estados finales

pesos = np.array([float(input("Ingrese el peso: ")) for l in range(2)], dtype='f') #Obtencion de pesos
print(pesos)

b = float(input("Ingrese la ganancia: ")) #Ingresa la ganancia
alpha = float(input("Ingrese alpha: "))
errores = [] #Lista en la que se guaradaran los errores

hardlim_hardlims = np.sort(np.unique(estados_finales))
errores_finales = []
errores_anteriores = []
total_E = []
gradiente_error = 0
purelin = False
i = 0 #Reinicia el bucle en caso de ser necesario, ya que con la estructura for no se logra reiniciar
iteracion_vuelta = 0
suma = 0
vueltas = 1

E =1 # Error de salida
E_ac = 0 # error actual
Error_prev = 0 # error anterior
Ew = 0 # Error cuadratico medio
E_total = 0 # error total




while i < int(patron.shape[0]): #Mientras sea menor al numero de patrones ingresados (P1, p2 .... P+n)
    #suma_vectores = np.dot(pesos,patron[i])
    multiplica_vectores = np.dot(pesos,patron[i]) #Multiplica los vectores (W(0)Pa)
    a = multiplica_vectores + b #Se suma la multiplicacion mas la ganacia para obtener a
    #a = multiplica_vectores
    Error_prev = Ew
    print(f"PARA PATRON P{i+1} iteracion {vueltas}")
    print("a: ", a) #Modificar ya sea para hardlim o hardlims
    
    if np.allclose(hardlim_hardlims, [0,1]) == True:
        print("Entre a hardlim")
        if a >= 0:
            a = 1
        if a < 0:
            a = 0
    if np.allclose(hardlim_hardlims, [-1,1]) == True:
        print("Entre a hardlims")
        if a < 0:
            a = -1
        else:
            a = 1
    if np.allclose(hardlim_hardlims, [0,1]) == False and np.allclose(hardlim_hardlims, [-1,1]) == False:
        print("Entre a purelin")
        purelin = True
        a = a
    #np.append(errores, estados_finales[i] - a)
    errores.append(estados_finales[i] - a) #Se obtiene el error y se guarda en una lista
    print("errores:", errores)
    if errores[i]!=0:                             #Se reajustan los valores de los pesos y la ganacia en caso de que el error sea diferente de 0
        patron_t = np.transpose(patron[i]) * (errores[i] * alpha * 2)
        pesos = np.add(pesos, patron_t)   #Nuevos pesos
        b = b + (errores[i] * 2 * alpha)
        E_total = E_total + ((errores[i])**2)
        #patron_t = np.transpose(patron[i])*
    
     # Error de la red con pureline
    if purelin == True and len(errores) == 4:
        Ew = ((1/4) * (E_total))
        E = (Ew - Error_prev)
        total_E.append(np.abs(E))
        errores_anteriores.extend(errores)
        if (np.abs(E) > 0.01) == False or (set(errores_anteriores[-8:-4])==set(errores))==True:
            break
    
    print("pesos: " , pesos)
    print("b: ", b)
    i+=1 
    #print("ESTE ES A:", a)
    #a = 0
    #En caso de que la lista de errores tenga tamaño 4(indicaria que ya se iteraron por completo los patrones) y dentro de esta se encuentre algun error diferente de cero se reiniciara el bucle 
    if len(errores) == 4:
        errores_finales.append(np.array(errores[-1]))
    
    
    
    if len(errores) == 4 and np.array_equal(np.array(errores),np.zeros(int(patron.shape[0])))==False: 
        
            
        errores.clear()
        i = 0
        vueltas += 1
        iteracion_vuelta += 1
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
plt.title("Separacion Lineal")
plt.plot([traza_x,0], [0,traza_y], linewidth=2)

plt.show()

if purelin == True:
    plt.ylabel('Error',fontsize = 12)
    plt.xlabel('Iteraciones',fontsize = 12)
    plt.title("ADALINE")
    x = np.arange(vueltas)
    plt.plot(x,total_E,'m->',label="Error cuadratico")
    plt.legend(loc='upper right')
    plt.show()
else:
    print(len(errores_finales))
    plt.ylabel('Error',fontsize = 12)
    plt.xlabel('Iteraciones',fontsize = 12)
    plt.title("ADALINE")
    x = np.arange(vueltas)
    plt.plot([x],[errores_finales],'m->', label="Error cuadratico")
    plt.legend(loc='upper right')
    plt.show()
