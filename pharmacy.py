from pyscipopt import Model
import numpy as np

model = Model("pharmacy")
remedios = []
remedios2 = []
drogas = []
cant_necesaria = []
r = {}
constraints = []

def readFiles():
    #farmacia = input("Ingrese el nombre del archivo y su extensión. Por ejemplo: farma01.in.\n")
    #remedio = input("Ingrese el nombre del archivo del nuevo remedio y su extensión. Por ejemplo: remedio01.in.\n")
    farmacia = "farma03.in"
    remedio = "remedio03.in"
    Coctel(farmacia, remedio)

def Coctel(farmacia, remedio):
    readTxtPharmacy(farmacia)   
    readTxtRemedio(remedio)

def readTxtPharmacy(file):
    try:
        with open(file, 'r') as archivo:
            print("Leyendo archivo " + file + "...\n")

            lines = archivo.readlines()
            passDrugs = False
            tupla = []

            for line in lines:
                if 'REMEDIOS' in line:
                  passDrugs = True
                  
                if not '#' in line and ':' in line and passDrugs == False and not 'DROGAS' in line:
                  linea = line.rstrip('\n')
                  split = linea.split(":")
                  drogas.append(split[0])
                  cant_necesaria.append(float(split[1].strip()))
                else:
                    if not '#' in line and passDrugs == True and not 'REMEDIOS' in line:
                      linea = line.rstrip('\n')
                      split = linea.split(":")
                      remedio = split[0]
                      remedios.append(remedio)
                      drugs = split[1].rstrip('\n')
                      split2 = drugs.split(",")
                      for cantDrug in split2:
                        linea3 = cantDrug.strip()
                        split3 = linea3.split(" ")
                        A = np.array([remedio, split3[0], float(split3[1])])
                        tupla.append(A) 
                          
            cantidades = np.zeros((len(remedios),len(drogas))).astype(float)
            for i in range(len(tupla)):
              cantidades[remedios.index(tupla[i][0])][drogas.index(tupla[i][1])] = tupla[i][2] # m remedios (filas) y n drogas (columnas)

            printDrugs(drogas, cant_necesaria)
            printRemedies(tupla)
            optimize(cantidades)

    except IOError:
        print ("No existe el archivo", archivo)

    finally:
        archivo.close()

def optimize(cantidades):
    for i in range(len(remedios)):
      r[i] = model.addVar(vtype='C', name='%s'%(remedios[i]))

    for j in range(len(drogas)):
      constraints.append(model.addCons(sum(r[t]*cantidades[t][j] for t in range(len(remedios))) >= cant_necesaria[j], name="restric", separate=False, modifiable = True))  

    for t in range(len(remedios)):
      model.addCons(r[t] >= 0)
    

    model.setObjective(sum(r[i] for i in range(len(remedios))), "minimize")

    model.hideOutput()
    model.optimize()

    printSolution()


def readTxtRemedio(file):
    try:
        with open(file, 'r') as archivo:
            print("\nLeyendo archivo " + file + "...\n")
            lines = archivo.readlines()
            passDrugs = False
            tupla2 = []
            for line in lines:
              if 'REMEDIOS' in line:
                passDrugs = True

              if not '#' in line and passDrugs == True and not 'REMEDIOS' in line:
                linea = line.rstrip('\n')
                split = linea.split(":")
                remedio = split[0]
                remedios2.append(remedio)
                drugs = split[1].rstrip('\n')
                split2 = drugs.split(",")
                for cantDrug in split2:
                  linea3 = cantDrug.strip()
                  split3 = linea3.split(" ")
                  A = np.array([remedio, split3[0], float(split3[1])])
                  tupla2.append(A) 
            
            cantidades2 = np.zeros((len(remedios2),len(drogas))).astype(float)
            for i in range(len(tupla2)):
              cantidades2[remedios2.index(tupla2[i][0])][drogas.index(tupla2[i][1])] = tupla2[i][2] # m remedios (filas) y n drogas (columnas)
                      
            print("Se agregan nuevos remedios...\n")
            printRemedies(tupla2)
            optimizeNewRemedy(cantidades2)

    except IOError:
        print ("No existe el archivo", archivo)

    finally:
        archivo.close()

def optimizeNewRemedy(cantidades2):
    model.freeTransform()
    tamanio = len(r)
    for i in range(len(remedios2)):
      r[i+tamanio] = model.addVar(vtype='C', name='%s'%(remedios2[i]))

    for t in range(len(constraints)):
      for i in range(len(remedios2)):
        model.addConsCoeff(constraints[t],r[i+tamanio],cantidades2[i][t])
  
    for t in range(len(remedios2)):
      model.addCons(r[t+tamanio] >= 0)
    
    model.setObjective(sum(r[i] for i in range(len(remedios) + len(remedios2))), "minimize")

    model.hideOutput()
    model.optimize()
    
    printSolution()

def printDrugs(drogas, cant_necesaria):
    print("Se obtiene las drogas y las cantidades necesarias\n")
    print ("{:<20} {:<20}".format('Droga','Cantidad necesaria'))
    for i in range(len(drogas)):
      print("{:<20} {:<20}".format(drogas[i], cant_necesaria[i]))
    print("\n")

def printRemedies(t_remedios):
    print("Se obtiene los remedios y su contenido\n")

    print ("{:<20} {:<20} {:<20}".format('Remedio', 'Droga', 'Cantidad'))
    for i in range(len(t_remedios)):
      print("{:<20} {:<20} {:<20}".format(t_remedios[i][0], t_remedios[i][1], t_remedios[i][2]))
              
    print("\n")

def printSolution():
    print("\n************************** SOLUCIÓN **************************")

    print("\nRemedios que van a ser utilizados:\n")
    print ("{:<20} {:<20}".format('Remedio','Cantidad'))
    for i in range(len(r)):
      print("{:<20} {:<20}".format(r[i].name, model.getVal(r[i])))
    print("\n")
    print("La cantidad de remedios distintos utilizados:", model.getObjVal())
    print("\n***************************************************************\n")

  
if __name__ == '__main__':
    readFiles()
