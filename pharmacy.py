from pyscipopt import Model
import numpy as np

model = Model("pharmacy")
remedios = []
remedios2 = []
cant_necesaria = []
drogas = []
r = {}
cantidades = [[]]
def readFiles():
    #farmacia = input("Ingrese el nombre del archivo y su extensión. Por ejemplo: farma01.in.\n")
    #remedio = input("Ingrese el nombre del archivo del nuevo remedio y su extensión. Por ejemplo: remedio01.in.\n")
    farmacia = "farma01.in"
    remedio = "remedio01.in"
    Coctel(farmacia, remedio)

def readTxtPharmacy(file):
    try:
        with open(file, 'r') as archivo:
                lines = archivo.readlines()
                passDrougs = False
                tupla = []
                for line in lines:
                    if 'REMEDIOS' in line:
                        passDrougs = True
                    if not '#' in line and ':' in line and passDrougs == False and not 'DROGAS' in line:
                        linea = line.rstrip('\n')
                        split = linea.split(":")
                        drogas.append(split[0])
                        cant_necesaria.append(float(split[1].strip()))
                    else:
                        if not '#' in line and passDrougs == True and not 'REMEDIOS' in line:
                            linea = line.rstrip('\n')
                            split = linea.split(":")
                            remedio = split[0]
                            remedios.append(remedio)
                            drougs = split[1].rstrip('\n')
                            split2 = drougs.split(",")
                            for cantDroug in split2:
                                linea3 = cantDroug.strip()
                                split3 = linea3.split(" ")
                                A = np.array([remedio, split3[0], float(split3[1])])
                                tupla.append(A) 
                
                cantidades = np.zeros((len(remedios),len(drogas))).astype(float)
                for i in range(len(tupla)):
                    cantidades[remedios.index(tupla[i][0])][drogas.index(tupla[i][1])] = tupla[i][2] # m remedios (filas) y n drogas (columnas)
                
                #addVarConstraints(cantidades)
    except IOError:
        print ("No existe el archivo", archivo)

    finally:
        archivo.close()

def addVarConstraints():
    for i in range(len(remedios)):
        r[i] = model.addVar(vtype='C', name='%s'%(remedios[i]))

    for j in range(len(drogas)):
        model.addCons((sum(r[t]*cantidades[t][j] for t in range(len(remedios))) >= cant_necesaria[j])      ) 

    for t in range(len(remedios)):
        model.addCons(r[t] >= 0)
    
def optimize():
    model.setObjective(sum(r[i] for i in range(len(remedios))), "minimize")

    model.hideOutput()
    model.optimize()

def printSolution():
    print("\n******************************* SOLUCIÓN *******************************")
    print("\nRemedios que van a ser utilizados:\n")
    print ("{:<10} {:<20}".format('Remedio','Cantidad'))
    for i in range(len(r)):
        print("{:<10} {:<20}".format(r[i].name, model.getVal(r[i])))
    print("\n")
    print("La cantidad de remedios distintos utilizados:", model.getObjVal())

def readTxtRemedio(file):
    passDrougs = False
    remedios2 = []
    r2 = {}
    tupla2 = []
    try:
        with open(file, 'r') as archivo:
                lines = archivo.readlines()

                for line in lines:
                    if 'REMEDIOS' in line:
                        passDrougs = True
                    if not '#' in line and passDrougs == True and not 'REMEDIOS' in line:
                            linea = line.rstrip('\n')
                            split = linea.split(":")
                            remedio = split[0]
                            remedios2.append(remedio)
                            drougs = split[1].rstrip('\n')
                            split2 = drougs.split(",")
                            for cantDroug in split2:
                                linea3 = cantDroug.strip()
                                split3 = linea3.split(" ")
                                A = np.array([remedio, split3[0], float(split3[1])])
                                tupla2.append(A) 
                #cantidades2 = np.zeros((len(remedios2),len(drogas))).astype(float)
                print(cantidades)
                #for i in range(len(tupla2)):
                   # cantidades[remedios2.index(tupla2[i][0])][drogas.index(tupla2[i][1])] = tupla2[i][2] # m remedios (filas) y n drogas (columnas)
    except IOError:
        print ("No existe el archivo", file)

    finally:
        archivo.close()

def optimizeNewRemedio():
    model.freeTransform()
    
    tamanio = len(r)
    for i in range(len(remedios2)):
        r[i+tamanio] = model.addVar(vtype='C', name='%s'%(remedios2[i]))

# variables = model.getVars()
# nvars = model.getNVars()

# sol = model.createSol(None)

# for i in range(len(variables)):
#    sol[variables[i]] = model.getSolVal(variables[i], variables[i])


# tamanio = len(r)
# for i in range(len(remedios2)):
#    r[i+tamanio] = model.addVar(vtype='C', name='%s'%(remedios2[i]))


def Coctel(farmacia, remedio):
    readTxtPharmacy(farmacia)
    
    readTxtRemedio(remedio)

