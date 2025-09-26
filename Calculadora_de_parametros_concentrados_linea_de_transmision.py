#Importacion de librerias
import numpy as np    #para todo jajajaj
import cmath    #para trabajar con los numeros complejos
import matplotlib.pyplot as plt   #para las graficas
#Importacion de librerias




#-----------------------
#DEFINICION DE FUNCIONES
#-----------------------
#Funciones exactas
#Resistencia
def resistencia(r,resistividad_conductor,longitud_conductor): #calculara la resistencia de un conductor segun el radio, la longitud y la resistividad del mismo. Es decir, calcula los [Ohm/m] y los [Ohm]
  area_transversal=(np.pi)*r**2   #formula
  resistencia_metro=resistividad_conductor/area_transversal  #formula. Resistencia por metro [Ohm/m]
  resistencia_final=resistencia_metro*longitud_conductor #multiplica la resistencia por metro de un conductor, por la longitud total de la linea de transmision [Ohm]
  return resistencia_metro, resistencia_final

#Inductancia
def inductancia(r1,r2,mu_medio,mu_conductor,distancia_conductores,longitud_conductor): #calculara la inductancia del conductor segun el flujo magnetico y la corriente. Tambien suma la inductancia interna [H/m]
  inductancia_interna=mu_conductor/(8*np.pi)  #formula. Se considera que se esta trabajando a baja frecuencia, para que no se tenga lugar a un efecto piel considerable
  inductancia_metro=((mu_medio*np.log((distancia_conductores-r1)*(distancia_conductores-r2)/(r1*r2)))/(2*np.pi))+inductancia_interna  #formula. Inductancia por metro [H/m]
  inductancia_final=(inductancia_metro*longitud_conductor) #simplemente multiplica la inductancia por metro, por la longitud total de la linea de transmision [H]
  return inductancia_metro, inductancia_final

#Capacitancia
def capacitancia(r1,r2,epsilon_medio,distancia_conductores,longitud_conductor):
  capacitancia_metro=(2*np.pi*epsilon_medio)/(np.log(((distancia_conductores-r1)*(distancia_conductores-r2))/(r1*r2)))   #formula. Capacitancia por metro [F/m]
  capacitancia_final=capacitancia_metro*longitud_conductor  #simplemente multiplica la capcitancia por metro, por la longitud total de la linea de transmision [F]
  return capacitancia_metro, capacitancia_final

#Conductancia
def conductancia(sigma_medio,epsilon_medio,capacitancia_metro,longitud_conductor):
  conductancia_metro=(sigma_medio/epsilon_medio)*capacitancia_metro   #formula. Conductancia por metro [S/m]
  conductancia_final=conductancia_metro*longitud_conductor
  return conductancia_metro,conductancia_final
#funciones exactas


#Funciones aproximadas
#Inductancia aproximada
def inductancia_aprox(r,mu_medio,mu_conductor,distancia_conductores,longitud_conductor): #calculara la inductancia del conductor segun el flujo magnetico y la corriente. Tambien suma la inductancia interna [H/m]
  inductancia_interna=mu_conductor/(8*np.pi)  #formula. Se considera que se esta trabajando a baja frecuencia, para que no se tenga lugar a un efecto piel considerable
  inductancia_metro_aprox=((mu_medio*np.log((distancia_conductores/r)))/(np.pi))+inductancia_interna  #formula aproximada. Inductancia por metro [H/m]
  inductancia_final_aprox=(inductancia_metro_aprox*longitud_conductor) #simplemente multiplica la inductancia por metro, por la longitud total de la linea de transmision [H]
  return inductancia_metro_aprox, inductancia_final_aprox

#Capacitancia aproximada
def capacitancia_aprox(r,epsilon_medio,distancia_conductores,longitud_conductor):
  capacitancia_metro_aprox=(np.pi*epsilon_medio)/(np.log(distancia_conductores/r))   #formula aproximada. Capacitancia por metro [F/m]
  capacitancia_final_aprox=capacitancia_metro_aprox*longitud_conductor  #simplemente multiplica la capcitancia por metro, por la longitud total de la linea de transmision [F]
  return capacitancia_metro_aprox, capacitancia_final_aprox

#Conductancia aproximada
def conductancia_aprox(sigma_medio,epsilon_medio,capacitancia_metro_aprox,longitud_conductor):
  conductancia_metro_aprox=(sigma_medio/epsilon_medio)*capacitancia_metro_aprox   #formula. Conductancia por metro [S/m]
  conductancia_final_aprox=conductancia_metro_aprox*longitud_conductor
  return conductancia_metro_aprox,conductancia_final_aprox
#Funciones aproximadas


#Error relativo y porcentual
def error(valor_exacto,valor_aproximado): 
  error_absoluto=abs(valor_aproximado-valor_exacto)   #formula del error absoluto
  error_porcentual=(error_absoluto/valor_exacto)*100   #formula del error porcentual
  return error_absoluto,error_porcentual
#Error relativo y porcentual


#Voltaje y corriente de la impedancia de carga de la linea de transmision
def voltajeYcorriente(impedancia_de_carga,voltaje_fuente,resistencia_circuito,w,inductancia_circuito,conductancia_circuito,capacitancia_circuito):
  vl = (impedancia_de_carga * voltaje_fuente) / (
    impedancia_de_carga
    + (resistencia_circuito + 1j * w * inductancia_circuito)
    * (1 + impedancia_de_carga * (conductancia_circuito + 1j * w * capacitancia_circuito))
  )   #esta es la expresion que se encontro en el analisis circuital
  il=vl/impedancia_de_carga

  vl_fasorial=cmath.polar(vl) #pasa de la forma rectangular a la forma polar del numero complejo
  il_fasorial=cmath.polar(il) #pasa de la forma rectangular a la forma polar del numero complejo
  return vl_fasorial, il_fasorial
#Voltaje y corriente de la impedancia de carga de la linea de transmision


#Calculos para pasar del dominio de la frecuencia al dominio del tiempo
def frecuenciaAtiempo(vl_fasorial,il_fasorial,w,t):
  vl_magnitud,vl_fase=vl_fasorial  #extraer los valores de la tupla
  il_magnitud,il_fase=il_fasorial  #extraer los valores de la tupla

  vl_tiempo=vl_magnitud*np.sin(w*t+vl_fase)
  il_tiempo=il_magnitud*np.sin(w*t+il_fase)
  return vl_tiempo, il_tiempo
#Calculos para pasar del dominio de la frecuencia al dominio del tiempo


#Funcion para graficar
def graficar2ConjuntosDeDatos(t,conjuntoDatosExactos,conjuntoDatosAproximados,tituloX,tituloY,tituloGrafica,dato,unidad):
  plt.figure(figsize=(8, 5))
  plt.plot(t,conjuntoDatosExactos,color="red",label="Exacta")
  plt.plot(t,conjuntoDatosAproximados,color="blue",label="Aproximada")
  plt.xlabel(tituloX)
  plt.ylabel(tituloY)
  plt.title(f"{tituloGrafica} {dato} [{unidad}]")
  plt.grid(True)
  plt.legend()
  plt.tight_layout()
  plt.show()
#Funcion para graficar
#-----------------------
#DEFINICION DE FUNCIONES
#-----------------------




#-------------------------------------------------------------
#MENU DE INICIO, DIGITACION DE PARAMETROS Y CALCULOS INICIALES
#-------------------------------------------------------------
#Menu inicial
menu="""Bienvenido a la calculadora de parametros concentrados y muchas cosas mas
Se asume que se trabajara con medios homogeneos, cables NO trenzados cilindricos circulares, temperatura constante, ambos conductores son del mismo material, tiempo de viaje de la onda electromagnetica extremadamente bajo.
A continuacion ingrese los parametros del problema:
"""
print(menu)
r1=float(input("Radio del conductor 1 en [m]: "))
r2=float(input("Radio del conductor 2 en [m]: "))
distancia_conductores=float(input("Distancia entre conductores [m]: "))
longitud_conductor=float(input("Longitud de la linea de transmision [m]: "))
epsilon_r_medio=float(input("Permitividad relativa del medio circundante de la linea de transmision (epsilon_r) [adimensional]: ")) 
mu_r_medio=float(input("Permeabilidad relativa del medio circundante de la linea de transmision (mu_r) [adimensional]: ")) 
sigma_medio=float(input("Conductividad del medio circundante de la linea de transmision [S/m]: "))
epsilon_r_conductor=float(input("Permitividad relativa del conductor de la linea de transmision (epsilon_r) [adimensional]: ")) 
mu_r_conductor=float(input("Permeabilidad relativa del conductor de la linea de transmision (mu_r) [adimensional]: "))
resistividad_conductor=float(input("Resistividad de los conductores [Ohm*m]: "))
voltaje_fuente=float(input("Voltaje de la fuente [V]: "))
frecuencia=float(input("Frecuencia de la fuente de voltaje [Hz]: "))
impedancia_de_carga=complex(input("Impedancia de carga de la linea (si tiene componente imaginaria ingresarla de la forma a+bj) [Ohm]: "))  #se tiene que calcular TENIENDO en cuenta la frecuencia que se digito anteriormente
#Menu inicial


#Calculos preeliminares
epsilon_0=8.854e-12 #epsilon_0=8.854e-12 [F/m]
mu_0=(np.pi)*4e-7 #mu_0=1.2566e-6 [H/m]
epsilon_medio=epsilon_r_medio*epsilon_0   #epsilon medio absoluto
mu_medio=mu_r_medio*mu_0   #mu medio absoluto
epsilon_conductor=epsilon_r_conductor*mu_0   #epsilon conductor absoluto
mu_conductor=mu_r_conductor*mu_0  #mu conductor absoluto
w=2*np.pi*frecuencia  #valor de w para j(w*Xl) y 1/j(w*Xc)
#Calculos preeliminares
#-------------------------------------------------------------
#MENU DE INICIO, DIGITACION DE PARAMETROS Y CALCULOS INICIALES
#-------------------------------------------------------------



#----------------------------------
#CALCULO DE PARAMETROS CONCENTRADOS
#----------------------------------
#Resistencia
resistencia_metro1,resistencia_final1=resistencia(r1,resistividad_conductor,longitud_conductor)
resistencia_metro2,resistencia_final2=resistencia(r2,resistividad_conductor,longitud_conductor)
resistencia_circuito=resistencia_final1+resistencia_final2

#Inductancia
inductancia_metro,inductancia_final=inductancia(r1,r2,mu_medio,mu_conductor,distancia_conductores,longitud_conductor)

#Capacitancia
capacitancia_metro, capacitancia_final=capacitancia(r1,r2,epsilon_medio,distancia_conductores,longitud_conductor)

#Conductancia
conductancia_metro,conductancia_final=conductancia(sigma_medio,epsilon_medio,capacitancia_metro,longitud_conductor)

#Visualizacion de resultados
pregunta0=str(input("\n"+"\nDesea visualizar en pantalla los calculos de los parametros concentrados (digite SI o NO): "))
if pregunta0=="SI":
  print("Los parametros obtenidos para el circuito son (ecuaciones exactas):")

  #Resistencia
  print(f"Resistencia por metro conductor 1: {resistencia_metro1} [ohm/m]")
  print(f"Resistencia por metro conductor 2: {resistencia_metro2} [ohm/m]")
  print(f"La resistencia del circuito es: {resistencia_circuito} [Ohms]"+"\n")

  #Inductancia
  print(f"Inductancia por metro: {inductancia_metro} [H/m]")
  print(f"La inductancia del circuito es: {inductancia_final} [H]"+"\n")

  #Capacitancia
  print(f"Capacitancia por metro: {capacitancia_metro} [F/m]")
  print(f"La capacitancia del circuito es: {capacitancia_final} [F]"+"\n")

  #Conductancia
  print(f"Conductancia por metro: {conductancia_metro} [S/m]")
  print(f"La conductancia del circuito es: {conductancia_final} [S]"+"\n")
else:
  pass
#----------------------------------
#CALCULO DE PARAMETROS CONCENTRADOS
#----------------------------------




#-----------------------------------------------------
#CALCULO DE PARAMETROS CONCENTRADOS POR APROXIMACIONES
#-----------------------------------------------------
#Inductancia
inductancia_metro_aprox, inductancia_final_aprox=inductancia_aprox(r1,mu_medio,mu_conductor,distancia_conductores,longitud_conductor) #esta aproximacion considera que ambos conductores tienen radio parecido a r1

#Capacitancia
capacitancia_metro_aprox, capacitancia_final_aprox=capacitancia_aprox(r1,epsilon_medio,distancia_conductores,longitud_conductor)  #esta aproximacion considera que ambos conductores tienen radio parecido a r1

#Conductancia
conductancia_metro_aprox, conductancia_final_aprox=conductancia_aprox(sigma_medio,epsilon_medio,capacitancia_metro_aprox,longitud_conductor)  #esta aproximacion considera que ambos conductores tienen radio parecido a r1

pregunta1=str(input("\nDesea mostrar en pantalla los resultados por medio de las aproximaciones (digite SI o NO): "))
if pregunta1=="SI":
  print("Los parametros obtenidos para el circuito son (aproximaciones):")
  print(f"Inductancia: {inductancia_metro_aprox} [H/m], el circuito tendra {inductancia_final_aprox} [H]"+"\n")
  print(f"Capacitancia: {capacitancia_metro_aprox} [F/m], el circuito tendra {capacitancia_final_aprox} [F]"+"\n")
  print(f"Conductancia: {conductancia_metro_aprox} [S/m], el circuito tendra {conductancia_final_aprox} [S]"+"\n")
else:
  pass
#-----------------------------------------------------
#CALCULO DE PARAMETROS CONCENTRADOS POR APROXIMACIONES
#-----------------------------------------------------




#---------------------------------------------------------
#CALCULO DE ERRORES ENTRE ECUACIONES EXACTAS Y APROXIMADAS
#---------------------------------------------------------
#Inductancia
porcentaje_error_inductancia=error(inductancia_metro,inductancia_metro_aprox)[1]

#Capacitancia
porcentaje_error_capacitancia=error(capacitancia_metro,capacitancia_metro_aprox)[1]

#Conductancia
porcentaje_error_conductancia=error(conductancia_metro,conductancia_metro_aprox)[1]

pregunta1=str(input("\nDesea mostrar en pantalla los errores porcentuales entre las formulas exactas y las aproximaciones (comparacion de parametros por unidad de longitud) (digite SI o NO): "))
if pregunta1=="SI":
  print(f"Inductancia (aproximacion respecto a exacta): {porcentaje_error_inductancia}%"+"\n")
  print(f"Capacitancia (aproximacion respecto a exacta): {porcentaje_error_capacitancia}%"+"\n")
  print(f"Conductancia (aproximacion respecto a exacta): {porcentaje_error_conductancia}%"+"\n")
else:
  pass
#---------------------------------------------------------
#CALCULO DE ERRORES ENTRE ECUACIONES EXACTAS Y APROXIMADAS
#---------------------------------------------------------




#---------------------------------------------------------
#ANALISIS DEL CIRCUITO APARTIR DE LOS PARAMETROS DIGITADOS
#---------------------------------------------------------
#Forma fasorial
vl_fasorial_exacta,il_fasorial_exacta=voltajeYcorriente(impedancia_de_carga,voltaje_fuente,resistencia_circuito,w,inductancia_final,conductancia_final,capacitancia_final)   #usa los valores calculados con las formulas exactas
vl_fasorial_aprox,il_fasorial_aprox=voltajeYcorriente(impedancia_de_carga,voltaje_fuente,resistencia_circuito,w,inductancia_final_aprox,conductancia_final_aprox,capacitancia_final_aprox)  #usa los valores calculados con las formulas aproximadas

#Cantidad de puntos para el muestreo
num_ciclos = 5   #define cuantos puntos de muestreo usar (tamaño del ndarray t)
T = 1 / frecuencia  # periodo de la señal
t = np.linspace(0, num_ciclos * T, 1000)  # 1000 puntos en 5 ciclos

#Forma en el dominio del tiempo
vl_tiempo_exacta,il_tiempo_exacta=frecuenciaAtiempo(vl_fasorial_exacta,il_fasorial_exacta,w,t)
vl_tiempo_aprox,il_tiempo_aprox=frecuenciaAtiempo(vl_fasorial_aprox,il_fasorial_aprox,w,t)

pregunta2=str(input("\nDesea visualizar en pantalla los calculos y graficos para el circuito electrico (digite SI o NO): "))
if pregunta2=="SI":
  #Muestra resultados del circuito
  print("Voltaje y corriente en la impedancia de carga en forma fasorial (fromulas exactas):")
  print(f"El voltaje en la impedancia de carga Zl es (r,phi): {vl_fasorial_exacta} [V]")
  print(f"La corriente en la impedancia de carga Zl es (r,phi): {il_fasorial_exacta} [A]"+"\n")
  #Muestra resultados del circuito


  #Muestra resultados del circuito
  print("Voltaje y corriente en la impedancia de carga en forma fasorial (fromulas aproximadas):")
  print(f"El voltaje en la impedancia de carga Zl es (r,phi): {vl_fasorial_aprox} [V]")
  print(f"La corriente en la impedancia de carga Zl es (r,phi): {il_fasorial_aprox} [A]"+"\n")
  #Muestra resultados del circuito


  #Error porcentual entre la magnitud del calculo exacto y de la aproximacion
  print("\nError porcentual de la corriente y el voltaje entre la aproximacion y la formula exacta:")
  #Voltaje
  vl_error_porcentual=error(vl_fasorial_exacta[0],vl_fasorial_aprox[0])[1]
  print(f"Voltaje: {vl_error_porcentual}%"+"\n")

  #Corriente
  il_error_porcentual=error(il_fasorial_exacta[0],il_fasorial_aprox[0])[1]
  print(f"Corriente:{il_error_porcentual}%"+"\n")
  #Error porcentual entre la magnitud del calculo exacto y de la aproximacion


  #Graficas de corriente y voltaje
  #Voltaje
  graficar2ConjuntosDeDatos(t,vl_tiempo_exacta,vl_tiempo_aprox,"t (s)","Voltaje [V]","Voltaje en la impedancia de carga de",impedancia_de_carga,"Ohm")
  
  #Corriente
  graficar2ConjuntosDeDatos(t,il_tiempo_exacta,il_tiempo_aprox,"t (s)","Corriente [A]","Corriente en la impedancia de carga de",impedancia_de_carga,"Ohm")
  #Graficas de corriente y voltaje
else:
  pass
#---------------------------------------------------------
#ANALISIS DEL CIRCUITO APARTIR DE LOS PARAMETROS DIGITADOS
#---------------------------------------------------------




#------------------------------------------------------
#CALCULO DE PARAMETROS PARA UN ANALISIS DE SENSIBILIDAD
#------------------------------------------------------
pregunta3=str(input("\nDesea realizar y visualizar en pantalla un analisis de sensibilidad con respecto a la distancia de los conductores (digite SI o NO): "))
if pregunta3=="SI":
  #Calculo de ndarrays con las funciones
  radio_sensibilidad=float(input("Digite el radio apartir del cual quiere realizar el analisis de sensibilidad de la distancia de los conductores, este radio sera r1 (2*r1 hasta 1e5*r1) [m]: "))  #apartir de este radio se cambiara la distancia entre conductores, el resto de datos se tomaran de los que ya se digitaron en el menu de inicio
  radio_fijo_sensibilidad=float(input("Digite el radio del segundo conductor para obtener un correcto analisis de sensibilidad, este sera r2, procurar que sea muy diferente a r1 para notar mas la variacion de los parametros concentrados (especialmente de la capacitancia, y por ende de la conductancia) [m]: "))   #Este valor es necesario, ya que si no se genera un analisis de sensibilidad poco util
  distancia_conductores_sensibilidad=np.linspace(2*radio_sensibilidad,1e5*radio_sensibilidad,10)

  #Formulas exactas
  inductancia_sensibilidad_metro=inductancia(radio_sensibilidad,radio_fijo_sensibilidad,mu_medio,mu_conductor,distancia_conductores_sensibilidad,longitud_conductor) [0] #se toma que los 2 radios son iguales para poder realizar una correcta comparacion con las aproximaciones
  capacitancia_sensibilidad_metro=capacitancia(radio_sensibilidad,radio_fijo_sensibilidad,epsilon_medio,distancia_conductores_sensibilidad,longitud_conductor)[0]  #Se pone [0] porque solo se va a hacer la comparacion con respecto al valor por metro. De esta forma solo se extrae el primer valor de la tupla
  conductancia_sensibilidad_metro=conductancia(sigma_medio,epsilon_medio,capacitancia_sensibilidad_metro,longitud_conductor)[0]

  #Aproximaciones
  inductancia_sensibilidad_apox_metro=inductancia_aprox(radio_sensibilidad,mu_medio,mu_conductor,distancia_conductores_sensibilidad,longitud_conductor)[0]
  capacitancia_sensibilidad_apox_metro=capacitancia_aprox(radio_sensibilidad,epsilon_medio,distancia_conductores_sensibilidad,longitud_conductor)[0]
  conductancia_sensibilidad_apox_metro=conductancia_aprox(sigma_medio,epsilon_medio,capacitancia_sensibilidad_apox_metro,longitud_conductor)[0]
  #Calculo de ndarrays con las funciones


  #Graficas comparativas entre aproximaciones y funciones exactas (la resistencia no tiene aproximacion)
  #Inductancia
  graficar2ConjuntosDeDatos(distancia_conductores_sensibilidad,inductancia_sensibilidad_metro,inductancia_sensibilidad_apox_metro,"Distancia entre conductores [m]","Inductancia por metro [H/m]","Inductancia por metro de la linea de transmision, con conductores separados de",str(2*radio_sensibilidad)+"-"+str(1e5*radio_sensibilidad),"m")

  #Capacitancia
  graficar2ConjuntosDeDatos(distancia_conductores_sensibilidad,capacitancia_sensibilidad_metro,capacitancia_sensibilidad_apox_metro,"Distancia entre conductores [m]","Capacitancia por metro [F/m]","Capacitancia por metro de la linea de transmision, con conductores separados de",str(2*radio_sensibilidad)+"-"+str(1e5*radio_sensibilidad),"m")

  #Conductancia
  graficar2ConjuntosDeDatos(distancia_conductores_sensibilidad,conductancia_sensibilidad_metro,conductancia_sensibilidad_apox_metro,"Distancia entre conductores [m]","Conductancia por metro [S/m]","Conductancia por metro de la linea de transmision, con conductores separados de",str(2*radio_sensibilidad)+"-"+str(1e5*radio_sensibilidad),"m")
  #Graficas comparativas entre aproximaciones y funciones exactas (la resistencia no tiene aproximacion)
else:
  pass
#------------------------------------------------------
#CALCULO DE PARAMETROS PARA UN ANALISIS DE SENSIBILIDAD
#------------------------------------------------------