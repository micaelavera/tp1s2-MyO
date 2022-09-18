from pyscipopt import Model
import numpy as np

model = Model("pharmacy")
#file = input("Ingrese el nombre del archivo y su extensión. Por ejemplo: farma01.in\n")
file = "farma01.in"
drogas = []
cant_necesaria = []
remedios = []
passDrugs = False
tupla = []

try:
    with open(file, 'r') as archivo:
            lines = archivo.readlines()

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
                    
except IOError:
    print ("No existe el archivo", file)

finally:
    archivo.close()

#### VARIABLES ####
# Remedios
r = {}
for i in range(len(remedios)):
    r[i] = model.addVar(vtype='C', name='%s'%(remedios[i]))

#### RESTRICCIONES ####
for j in range(len(drogas)):
  model.addCons(sum(r[t]*cantidades[t][j] for t in range(len(remedios))) >= cant_necesaria[j])       

for t in range(len(remedios)):
  model.addCons(r[t] >= 0)
 
#### FUNCIÓN OBJETIVO ####
model.setObjective(sum(r[i] for i in range(len(remedios))), "minimize")

model.hideOutput()
model.optimize()

print("\n******************************* SOLUCIÓN *******************************")

print("Remedios que van a ser utilizados:\n")
print ("{:<10} {:<20}".format('Remedio','Cantidad'))
for i in range(len(r)):
  print("{:<10} {:<20}".format(r[i].name, model.getVal(r[i])))



print("\n")
print("La cantidad de remedios distintos utilizados:", model.getObjVal())
#sol = model.getSolVal()
#othermodel = Model("pharmacy")#
#newvariables = model.getVars()
#vars = model.getNVars()
#print(sol)
#newsol = model.createSol()

#for i in range(vars):
 #  newsol[newvariables[i]] = othermodel.setSolVal(sol, newvariables[i])
#print(accepted)
