from proceso import Proceso
import os
import time
import random
import msvcrt
import sys

cont_global = 0
nuevos = [] #cola de nuevos
listos = [] #cola de listos
terminados = [] #cola de terminados
ejecucion = [] #cola de ejecucion
bloqueados = [] #cola de bloqueados

quantum = 0

def definir(cantidad_procesos, tiempo):

    global quantum
    quantum = tiempo
    
    for i in range(0,cantidad_procesos):
        llenadoAutomatico(i)

    mostrar()

    imprimirTablaProcesos()

def llenadoAutomatico(i):
    id = i
    num1 = random.randint(0, 10)
    num2 = random.randint(0, 10)
    operacion = random.randint(1, 6)
    tme = random.randint(6, 16) #generamos una cantidad aleatoria de tiempo de ejecucion

    pro = Proceso(id,operacion,tme,num1,num2)
    nuevos.append(pro)

def mostrar():
    cont_ext = 0

    cantidad_procesos = len(nuevos)
    i = 0
    
    cont = 0 #NUEVO

    esprimero = True
    while(i<cantidad_procesos):
        if (i == cont_ext + 3): # si ya se han mostrado 3 procesos
            procesar()
            cont_ext = 3 # reiniciamos el contador de procesos mostrados
            if (len(nuevos) > 0 and esprimero): # si hay procesos nuevos y es el primer ciclo
                nuevos[0].tllegada = cont_global # asignamos el tiempo de llegada del primer proceso
                listos.append(nuevos[0])
                nuevos.remove (nuevos[0])
                listos[0].trespuesta = cont_global
                esprimero = False
            if (len(listos) == 1):
                #listos[0].trespuesta = cont_global
                ejecucion.append(listos[0])
                listos.remove(listos[0])
                imprimirEjecucion()

        else: # si son menos de 3 procesos
            while (cont < 3):
                if (len(nuevos) > 0):
                    nuevos[0].tllegada = cont_global
                    listos.append(nuevos[0])
                    nuevos.remove(nuevos[0])
                cont += 1
            #procesar()
            #cont_ext = 3
            procesar()
            cont_ext += 3
            if (len(nuevos) > 0 and esprimero):
                nuevos[0].tllegada = cont_global
                listos.append(nuevos[0])
                nuevos.remove(nuevos[0])
                #listos[0].trespuesta = cont_global
                #esprimero = False
        i+=1  

def procesar(): #procesar los procesos que estan en la cola de listos

    i = 0
    long = len(nuevos)+len(listos)+len(ejecucion)
    while (len(listos)>0): 
        ejecucion.append(listos[0])
        listos.remove(listos[0])
        imprimirEjecucion()
        if (len(ejecucion)>0): # si hay procesos en ejecucion
            ejecucion[0].tfinalizacion = cont_global # asignamos el tiempo de finalizacion del proceso
            terminados.append(ejecucion[0])
            if (len(nuevos) > 0):
                nuevos[0].tllegada = cont_global
                listos.append(nuevos[0])
                nuevos.remove(nuevos[0])
            ejecucion.remove(ejecucion[0])
            i+=1
        

def imprimirEjecucion():
    
    global cont_global
    global quantum

    if ejecucion[0].tquantum == 0:
        ejecucion[0].tquantum = quantum

    if len(listos) >= 0:
        tt = ejecucion[0].tt
        if tt == 0:
            ejecucion[0].trespuesta = cont_global
            #Tiempo transcurrido en 1 para los procesos menos el primero
            if cont_global > 0:
                ejecucion[0].tt = 1

        #while(tt<=ejecucion[0].tme):

        while(tt<ejecucion[0].tme and ejecucion[0].tquantum >= 0):
            if ejecucion[0].tquantum == 0:
                listos.append(ejecucion[0])
                ejecucion.remove(ejecucion[0])
                break
            
            if(msvcrt.kbhit()):
                key = msvcrt.getwch()
                #69 = E key y 101 = e key
                if(key == chr(101) or key == chr(69)):
                    if len(listos) > 0 and len(bloqueados) < 3:        
                        bloqueados.append(ejecucion[0])
                        ejecucion.remove(ejecucion[0])
                        ejecucion.append(listos[0])
                        listos.remove(listos[0])
                        imprimirEjecucion()
                    break
                #87 = W key y 119 = w key
                elif(key == chr(87) or key == chr(119)):
                    ejecucion[0].tme = 0
                    ejecucion[0].error = 1
                    break
                # 80= P key y 112 = p key
                elif(key == chr(80) or key == chr(112)):
                    print("******************************************")
                    print("Contador Global: " + str(cont_global))
                    print("******************************************\n")
                    print("******************************************")
                    print("***              Nuevos                ***")
                    print("******************************************")
                    print("ID    |Tiempo Maximo Estimado")
                    if len(nuevos) > 0:
                        #lote en Listos
                        for proc in nuevos:
                            print(str(proc.id) + "\t\t" + str(proc.tme))
                    print("\n********************************************")
                    print("***               Listos                 ***")
                    print("********************************************")
                    print("ID|Tiempo Maximo Estimado|Tiempo Transcurrido")

                    #lote en Listos
                    for lote in listos:
                        if (lote != ejecucion[0]):
                            print(str(lote.id) + "\t\t" + str(lote.tme)+ "\t\t" + str(lote.tt))

                    #Proceso en ejecucion
                    if len(ejecucion) > 0 and ejecucion[0].error != 1:
                        print("\n******************************************")
                        print("***    Proceso en ejecución            ***" )
                        print("******************************************")
                        print("Id: " + str(ejecucion[0].id))
                        print("Operación: " + str(realizarOperacionAntes(ejecucion[0])))
                        print("Tiempo Maximo Estimado: " + str(ejecucion[0].tme))
                        print("Tiempo Transcurrido: " + str(tt))
                        print("Tiempo Restante: " + str(ejecucion[0].tme-tt))
                    cont_global += 1
                    ejecucion[0].tquantum -= 1

                    #Procesos bloqueados
                    print("\n******************************************")
                    print("***         Procesos Bloqueados        ***")
                    print("******************************************")
                    print("ID  |Tiempo Transcurrido en Bloqueado")
                    if(len(bloqueados) > 0):
                        for lote in bloqueados:
                            if lote.ttb <= 7:
                                print(str(lote.id) + "\t\t" + str(lote.ttb))
                                lote.ttb += 1
                            else:
                                lote.ttb = 0
                                listos.append(lote)
                                bloqueados.remove(lote)
                                
                    tt += 1
                    ejecucion[0].tt = tt

                    print("\n******************************************")
                    print("***        Procesos Terminados         ***")
                    print("******************************************\n")
                    print("ID  |Operacion y Resultado" )
                    for terminado in terminados:
                        if(terminado.error == 0):
                            print(str(terminado.id) +  "   | " + str(realizarOperacion(terminado)))
                        elif(terminado.error == 1):
                            print(str(terminado.id) +  "   | ERROR ")

                    time.sleep(1)

                    if(len(ejecucion) == 1 and tt>ejecucion[0].tme and ejecucion[0].error == 0):
                        print(str(ejecucion[0].id) + "\t\t\t| " + str(realizarOperacion(ejecucion[0])))
                        #os.system("pause")
                    elif((len(ejecucion) == 1 and tt>ejecucion[0].tme and ejecucion[0].error != 0)):
                        print(str(ejecucion[0].id) +  "\t\t\t| ERROR ")
                        #os.system("pause")
                    
                    while(True):
                        c = input("Proceso pausado, ¿Quieres continuar? (c/C)")
                        if(c == "c" or c == "C"):
                            break
                    break


                #78 = N key y 110 = n key
                # Agregar nuevo proceso
                elif(key == chr(78) or key == chr(110)):
                    llenadoAutomatico(len(nuevos)+len(terminados)+len(listos)+len(ejecucion)+len(bloqueados))
                    nuevos[len(nuevos)-1].tllegada = cont_global
                    # añadir a listos si hay menos de dos procesos en listos y 0 en bloqueados
                    if(len(listos) < 2) and len(bloqueados) == 0:
                        listos.append(nuevos[len(nuevos)-1])
                        nuevos.remove(nuevos[len(nuevos)-1])

                #66 = B key y 98 = b key
                elif(key == chr(66) or key == chr(98)):
                    while(True):

                        imprimirTablaProcesos()

                        c = input("¿Quieres continuar con el proceso? (c/C)")
                        if(c == "c" or c == "C"):
                            break
                sys.stdout.flush()
           
            
            print("******************************************")
            print("Contador Global: " + str(cont_global))
            print("******************************************\n")
            print("******************************************")
            print("***              Nuevos                ***")
            print("******************************************")
            print("ID    |Tiempo Maximo Estimado")
            if len(nuevos) > 0:
                #lote en Listos
                for proc in nuevos:
                    print(str(proc.id) + "\t\t" + str(proc.tme))
            print("\n********************************************")
            print("***               Listos                 ***")
            print("********************************************")
            print("ID|Tiempo Maximo Estimado|Tiempo Transcurrido")

            #lote en Listos
            for lote in listos:
                if (lote != ejecucion[0]):
                    print(str(lote.id) + "\t\t" + str(lote.tme)+ "\t\t" + str(lote.tt))

            #Proceso en ejecucion
            if len(ejecucion) > 0 and ejecucion[0].error != 1:
                print("\n******************************************")
                print("***    Proceso en ejecución            ***" )
                print("******************************************")
                print("Id: " + str(ejecucion[0].id))
                print("Operación: " + str(realizarOperacionAntes(ejecucion[0])))
                print("Tiempo Maximo Estimado: " + str(ejecucion[0].tme))
                print("Tiempo Transcurrido: " + str(tt))
                print("Tiempo Restante: " + str(ejecucion[0].tme-tt))

            
            cont_global += 1            
            ejecucion[0].tquantum -= 1

            #Procesos bloqueados
            print("\n******************************************")
            print("***         Procesos Bloqueados        ***")
            print("******************************************")
            print("ID  |Tiempo Transcurrido en Bloqueado")
            if(len(bloqueados) > 0):
                for lote in bloqueados:
                    if lote.ttb <= 7:
                        print(str(lote.id) + "\t\t" + str(lote.ttb))
                        lote.ttb += 1
                    else:
                        lote.ttb = 0
                        listos.append(lote)
                        bloqueados.remove(lote)
                        
            tt += 1
            ejecucion[0].tt = tt

            print("\n******************************************")
            print("***        Procesos Terminados         ***")
            print("******************************************\n")
            print("ID  |Operacion y Resultado" )
            for terminado in terminados:
                if(terminado.error == 0):
                    print(str(terminado.id) +  "   | " + str(realizarOperacion(terminado)))
                elif(terminado.error == 1):
                    print(str(terminado.id) +  "   | ERROR ")

            time.sleep(1)

            if(len(ejecucion) == 1 and tt>ejecucion[0].tme and ejecucion[0].error == 0):
                print(str(ejecucion[0].id) + "\t\t\t| " + str(realizarOperacion(ejecucion[0])))
                #os.system("pause")
            elif((len(ejecucion) == 1 and tt>ejecucion[0].tme and ejecucion[0].error != 0)):
                print(str(ejecucion[0].id) +  "\t\t\t| ERROR ")
                #os.system("pause")

            clearConsole()

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

def realizarOperacion(lote):
    num1 = lote.num1
    num2 = lote.num2
    operacion = lote.operacion
    resultado = 0
    operando = ""

    if(operacion == 1):
        resultado = num1 + num2
        operando = "+"
    elif(operacion == 2):
        resultado = num1 - num2
        operando = "-"
    elif (operacion == 3):
        resultado = num1 * num2
        operando = "*"
    elif (operacion == 4):
        if(num2 == 0):
            resultado = "No se puede dividir entre 0"
            operando = "/"
        else:
            resultado = round(num1 / num2, 2)
            operando = "/"
    elif (operacion == 5):
        if(num2 == 0):
            resultado = "No se puede dividir entre 0"
            operando = "%"
        else:
            #Residuo con dos decimales
            resultado = round(num1 % num2, 2)
            operando = "%"
    elif (operacion == 6):
        resultado = num1 ** num2
        operando = "**"

    res = str(num1) + " " + str(operando) + " " + str(num2) + " = " + str(resultado)

    return res


def realizarOperacionAntes(lote):
    num1 = lote.num1
    num2 = lote.num2
    operacion = lote.operacion
    resultado = 0
    operando = ""
    if(operacion == 1): #Condicinal para la Suma
        resultado = num1 + num2
        operando = "+"
    elif(operacion == 2): #Condicinal para la Resta
        resultado = num1 - num2
        operando = "-"
    elif (operacion == 3): #Condicinal para la Multiplicacion
        resultado = num1 * num2
        operando = "*"
    elif (operacion == 4): #Condicinal para la Division
        if(num2 == 0): #Error, division entre 0
            resultado = "No se puede dividir entre 0"
            operando = "/"
        else:
            resultado = num1 / num2
            operando = "/"
    elif (operacion == 5):#Condicinal para el Residuo
        if(num2 == 0): #Error, division entre 0
            resultado = "No se puede dividir entre 0"
            operando = "%" #Residuo
        else:
            resultado = num1 % num2
            operando = "%"
    elif (operacion == 6): #Condicional para la potencia
        resultado = num1 ** num2
        operando = "**"
    res = str(num1) + " " + str(operando) + " " + str(num2)

    return res

def soloResultado(lote):
    num1 = lote.num1
    num2 = lote.num2
    operacion = lote.operacion
    resultado = 0
    operando = ""
    if(operacion == 1): #Condicinal para la Suma
        resultado = num1 + num2
        operando = "+"
    elif(operacion == 2): #Condicinal para la Resta
        resultado = num1 - num2
        operando = "-"
    elif (operacion == 3): #Condicinal para la Multiplicacion
        resultado = num1 * num2
        operando = "*"
    elif (operacion == 4): #Condicinal para la Division
        if(num2 == 0): #Error, division entre 0
            resultado = "No se puede dividir entre 0"
            operando = "/"
        else:
            #resultado con dos decimales
            resultado = round(num1 / num2, 2)
            operando = "/"
    elif (operacion == 5):#Condicinal para el Residuo
        if(num2 == 0): #Error, division entre 0
            resultado = "No se puede dividir entre 0"
            operando = "%" #Residuo
        else:
            #Residuo con dos decimales
            resultado = round(num1 % num2, 2)
            operando = "%"
    elif (operacion == 6): #Condicional para la potencia
        resultado = num1 ** num2
        operando = "**"
    res = str(resultado)

    return res
    
#Imprimir tabla durante y al final
def imprimirTablaProcesos():
    print("ID\t  T. Llegada\t T. Restante\t T. Finalizacion\t  T.Retorno\t   T. Respuesta\t  T. Espera \tT. Servicio \tOperacion\tResultado \t Estado")
    
    for i in range(0, len(terminados)):
        terminados[i].espera = terminados[i].tfinalizacion - terminados[i].tt - terminados[i].tllegada
        terminados[i].tretorno = terminados[i].tfinalizacion - terminados[i].tllegada

        if terminados[i].error == 0:
            print(str(terminados[i].id) +"\t\t"+ str(terminados[i].tllegada) +"\t\t" + str(terminados[i].tme-terminados[i].tt) +"\t\t" + str(terminados[i].tfinalizacion) 
            +"\t\t\t"+ str(terminados[i].tretorno) +"\t\t"+ str(terminados[i].trespuesta) +"\t\t"+ str(terminados[i].espera)
            +"\t \t"+ str(terminados[i].tt)+ "\t" + str(realizarOperacionAntes(terminados[i])) + "\t      \t" + str(soloResultado( terminados[i])) +"\t\t" + "E.Terminado")
        elif terminados[i].error == 1:
            print(str(terminados[i].id) +"\t\t"+ str(terminados[i].tllegada) +"\t\t" + "0" +"\t\t" + str(terminados[i].tfinalizacion) 
            +"\t\t\t"+ str(terminados[i].tretorno) +"\t\t"+ str(terminados[i].trespuesta) +"\t\t"+ str(terminados[i].espera)
            +"\t \t"+ str(terminados[i].tt)+ "\t" + str(realizarOperacionAntes( terminados[i])) + "\t      \t" "¡Error!" "\t\t" + "E.Terminado")

    for i in range(0, len(ejecucion)):
        print(str(ejecucion[i].id) +"\t\t"+ str(ejecucion[i].tllegada) +"\t\t" + str(ejecucion[i].tme-ejecucion[i].tt) +"\t\t" + str(ejecucion[i].tfinalizacion) 
        +"\t\t\t"+ str(ejecucion[i].tretorno) +"\t\t"+ str(ejecucion[i].trespuesta) +"\t\t"+ str(ejecucion[i].espera)
        +"\t \t"+ str(ejecucion[i].tt)+ "\t" + str(realizarOperacionAntes(ejecucion[i])) + "\t\tNONE\t\t" + "E.Ejecucion")

    for i in range(0, len(bloqueados)):
        print(str(bloqueados[i].id) +"\t\t"+ str(bloqueados[i].tllegada) +"\t\t" + str(bloqueados[i].tme-bloqueados[i].tt) +"\t\t" + str(bloqueados[i].tfinalizacion) 
        +"\t\t\t"+ str(bloqueados[i].tretorno) +"\t\t"+ str(bloqueados[i].trespuesta) +"\t\t"+ str(bloqueados[i].espera)
        +"\t \t"+ str(bloqueados[i].tt)+ "\t" + str(realizarOperacionAntes(bloqueados[i])) + "\t\tNONE\t\t" + "E.Bloqueado")

    for i in range(0, len(listos)):
        print(str(listos[i].id) +"\t\t"+ str(listos[i].tllegada) +"\t\t" + str(listos[i].tme-listos[i].tt) +"\t\t" + str(listos[i].tfinalizacion) 
        +"\t\t\t"+ str(listos[i].tretorno) +"\t\t"+ str(listos[i].trespuesta) +"\t\t"+ str(listos[i].espera)
        +"\t \t"+ str(listos[i].tt)+ "\t" + str(realizarOperacionAntes(listos[i])) + "\t\tNONE\t\t" + "E.Listo")
        
    for i in range(0, len(nuevos)):
        print(str(nuevos[i].id) +"\t\t" + "Null" + "\t\t" + "Null" +"\t\t" + "Null"
        +"\t\t\t"+ "Null" +"\t\t"+ "Null" +"\t\t"+ "Null"
        +"\t \t"+ "Null"+ "\t" + "Null" + "\t  \t" + "Null" +"\t\t" + "E.Nuevo")